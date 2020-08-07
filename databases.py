import pymongo as PM
import subprocess


### Maybe change the design to be more application specific

class MongoHandler:
    def __init__(self):
        self.client = None
        self.db = None
        self.last_collection = None
    
    @classmethod
    def init_std(cls, ip, port):
        inst = cls()
        inst.connect(ip, port)
        return inst
        
    @classmethod
    def init_cred(cls, ip, port, user, pwd, auth_src):
        inst = cls()
        inst.connect_w_creds(ip, port, user, pwd, auth_src)
        return inst
        

    # ip + port => no authentication
    def connect(self, ip, port):
        ''' conncection with no credentials required: used for quick testing \n (ip, port)->pymongo.mongo_client.MongoClient '''
        self.client = PM.MongoClient(fr"mongodb://{ip}:{port}")
        return self.client

    # ip + port + user + pwd => w/ authentication
    def connect_w_creds(self, ip, port, user, pwd, auth_src):
        ''' use crdentials for an authenticated connection \n (ip, port, user, password, authentication_database)->pymongo.mongo_client.MongoClient '''
        self.client = PM.MongoClient(fr"mongodb://{user}:{pwd}@{ip}:{port}/?authSource={auth_src}")
        return self.client
    # connection string
    def connect_w_string(self, con_str):
        ''' use a connection string to connect to mongodb server \n(connection_string)->pymongo.mongo_client.MongoClient \nExample \ncon.connect_w_string("mongodb://user:pass@localhost:port/db?authSource=info") '''
        self.client = PM.MongoClient(self, con_str)
        return self.client

    def get_database(self, db_name="test"):
        cl = self.client
        if cl == None:
            print('no connection exits yet')
            return None
        self.db = cl[f'{db_name}']
        return self.db

    def get_collection(self, col_name="uncategorized"):
        self.last_collection = self.db[f"{col_name}"]
        return self.last_collection

    def insert_documents(self,docs_list, col=''):
        try:
            collection = self.get_collection() if not col else self.get_collection(col)
            self.last_inserts = collection.insert_many(docs_list)
        except Exception as e:
            print(e)

    ## no connection closure
    # def close(self):
    #     self.db.close()

    ###
