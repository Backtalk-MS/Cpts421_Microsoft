import pymongo, os, json, time

uri = ""
client = pymongo.MongoClient(uri)
db = client['admin']
collection = db['posts']
print(db.command("collStats","posts"))
 def batch_iter(iterable, batch_size=1):
     size = len(iterable)
     for index in range(0,size,batch_size):
         yield iterable[index:min(index+batch_size,size)]

 count = 0

 path = "..\\Test_Mongoose\\json"
 for file in os.listdir(path):
     with open(path + "\\" + file) as json_file:
         json_doc = json.load(json_file)
         for batch in batch_iter(json_doc,20):
             count+=20
             print(count)
             collection.insert_many(batch)
             time.sleep(0.05)
