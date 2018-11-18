import pymongo, os, json, time

uri = "mongodb://aminich:5WOXsas5o8bQVSIapi3i4fH6jAZGD7hSu2EvmjqP0HbxlB0PFXRK1OnKihWu26YHltGxkXfQSVasw4hFaLp9xw==@aminich.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
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