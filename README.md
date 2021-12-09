## Requirements

 * setup mongodb 
 * `python3 -m pip install -r requirements.txt`

## Run project
 * mkdir -p db/{db,logs}
 * mongod -f mongod.conf
 * mongo localhost:27000 create_db.js
 * flask run -p 8000
