from pymongo import MongoClient

#Base de datos local
# db_client = MongoClient().local 

#Base de datos remota
db_client = MongoClient('mongodb+srv://alejohdz412_db_user:Alejohdz005@cluster0.jhj66k6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0').db
