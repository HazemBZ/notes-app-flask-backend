from flask_app import app
from flask import render_template, jsonify, request # templating uses jinja2
from flask_app.databases import MongoHandler
from flask_cors import CORS
from flask import Flask

from bson.objectid import ObjectId
from pymongo.results import InsertManyResult
from pymongo.results import DeleteResult
from pymongo.collection import Collection
from typing import List

con = MongoHandler.init_cred("localhost", 27000, "notes_db_owner", "notes_db_owner", "admin")
notes = con.get_database("notes")
terms_collection:Collection = con.get_collection("terms")


app = Flask(__name__, template_folder="templates")
cors = CORS(app)    


#--------BACKEND

def adapt(x):
    x['_id'] = str(x["_id"])
    return x

def getTerm(id):
    return adapt(terms_collection.find_one({"_id": ObjectId(id)}))

def getTerms(nbr=10):
    nbr = nbr if nbr<10 else 10
    pipeline = [
        # {"$project": {"_id":1}},
        {"$limit": nbr}
    ]
    terms = map(adapt, terms_collection.aggregate(pipeline))
    return list(terms)

def getTermsLike(term):
    pipeline = [
        {
            "$match": 
                {"term":{"$regex": ".*%s.*" % term}}
        },
        # {
        #     "$project": {"_id":0}
        # } 
        ]
    res = [] 
    try:
        res = terms_collection.aggregate(pipeline) 
    except Exception as e:
        print(e)
    terms = map(adapt, res)
    return list(terms)


def insertTerms(terms)->InsertManyResult:
    res = terms_collection.insert_many(terms)
    return res

def update(term):
    # print(term['tags'])
    res = terms_collection.update_one(
        {"_id": ObjectId(term['_id'])}, 
        {"$set": {"term": term['term'], "desc": term['desc'], "tags": term['tags']}}
        )
    return res


#-----------------ROUTING



@app.route('/')
@app.route('/index')
def index():
    user = {'username': "dude"}
    return render_template("index.html", user=user, title="home page", terms=getTerms());

@app.route('/terms', methods=["GET"])
def terms():
    if request.args.get("term"):
        return jsonify(getTermsLike(request.args.get("term")))
    return jsonify(getTerms())

@app.route('/term')
def term():
    id = request.args.get('id')
    return jsonify(getTerm(id))

# @app.route('/terms', methods=["GET"])
# def termsLike():
#     return jsonify(getTermsLike(request.args.get("term")))

@app.route('/terms/add', methods=['POST'])
def addTerms():
    # verify post data format
    # add post data
    # send back add response
    print(request.json)
    res = insertTerms(request.json)
    return jsonify({
        "aknowledged":res.acknowledged, 
        "inserted_ids":list(map(lambda x: str(x), res.inserted_ids))
        })

@app.route('/term/delete/<term_id>', methods=["delete"])
def deleteTerm(term_id):
    print("DeleteTrem:%s" %term_id)
    resp = terms_collection.delete_one({"_id": ObjectId(term_id)})
    return jsonify(resp.raw_result)

@app.route('/term/patch', methods=["PATCH"])
def updateTerm():
    res = update(request.json)
    return jsonify(res.raw_result)