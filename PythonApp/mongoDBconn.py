# import required module
import pymongo

myclient = None

# establish a connection
def connect():
    global myclient
    myclient = pymongo.MongoClient()
    myclient.admin.command('ismaster')

# create function to view collections within mongo database
def view_collections():
    # connect and provide database and collections
    if (not myclient):
        connect()

    mydb = myclient["movieScriptsDB"]
    docs = mydb["movieScripts"]
    # iterate through the collections and print by id in ascending order
    coll_entries = docs.find().sort("_id", 1 ) 
    for coll in coll_entries:
        print(coll)


def movie_subtitle(sub_lang):
    # connect and provide database and collections
    if (not myclient):
        connect()
    # creation of a list
    movie_id = []

    mydb = myclient["movieScriptsDB"]
    docs = mydb["movieScripts"]
    query7 = {"subtitles": {"$regex": sub_lang, "$options": "i"}}

    # iterate through the database based on query specifications
    subtitles = docs.find(query7)
    for sub in subtitles:
        # add the ids to the created list
        movie_id.append(sub["_id"])

    # iterate through the list, change it to a string and remove the comma at the end
    ids = ""
    for id in movie_id:
        ids += str(id) + ","
    ids = ids[0:len(ids)-1]
    return(ids)


def movie_script(film_id, keywords, sub_langs):
    # connect and provide database and collections
    if (not myclient):
        connect()

    mydb = myclient["movieScriptsDB"]
    docs = mydb["movieScripts"]
    query8 = {"_id": film_id, "keywords": keywords, "subtitles": sub_langs}
    # an addition is made to the mongo database, based on user input i.e., filmid, keywords and subtitle languages
    docs.insert(query8)


def delete_db_entry(film_id):
    # connect and provide database and collections
    if (not myclient):
        connect()

    mydb = myclient["movieScriptsDB"]
    docs = mydb["movieScripts"]
    query10 = {"_id": film_id}
    # A entry is deleted from the database based on the user input i.e., filmid
    docs.delete_one(query10)

# when main is executed try exec. the functions created above
def main():
    if (not myclient):
        try:
            connect()
            movie_subtitle()
            movie_script()
            delete_db_entry()
            view_collections()
        # provide an error if functions cannot be executed
        except Exception as e:
            print("Error", e)

if __name__ == "__main__":
    # execute only if run as a script
    main()