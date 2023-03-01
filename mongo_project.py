import os
import pymongo
if os.path.exists("env.py"):
    import env


MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "database0"  # on cluster0
COLLECTION = "humans"   # humans or celebrities


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e


def show_menu():
    print("")
    print("1. Add a record")
    print("2. Find a record by name")
    print("3. Edit a record")
    print("4. Delete a record")
    print("5. Exit")

    option = input("Enter option: ")
    return option


def get_record():
    """
    Helper file
    """
    print("")
    first = input("Enter first name > ")
    last = input("Enter last name > ")

    try:
        doc = coll.find_one({"first": first.lower(), "last": last.lower()})
    except:
        print("")
        print("Error! No results found")  # if an empty doc is found

    if not doc:
        print("")
        print("Error! No results found.")

    return doc


def add_record():
    """
    Insert records into the collection
    """
    print("")
    first = input("Enter first name > ")
    last = input("Enter last name > ")
    dob = input("Enter date of birth > ")
    gender = input("Enter gender > ")
    speciality = input("Enter speciality > ")
    occupation = input("Enter occupation > ")
    nationality = input("Enter nationality > ")

    new_doc = {
        "first": first.lower(),
        "last": last.lower(),
        "dob": dob,
        "gender": gender,
        "speciality": speciality,
        "occupation": occupation,
        "nationality": nationality
    }

    try:
        coll.insert_one(new_doc)
        print("")
        print("Document inserted")
    except:
        print("Error accessing the database")


def find_record():
    doc = get_record()
    if doc:
        print("")
        for k, v in doc.items():     # iterate over key-value pairs in document
            if k != "_id":           # MongoDB object id
                print(k.capitalize() + ": " + v.capitalize())


def edit_record():
    doc = get_record()
    if doc:
        update_doc = {}                # dictionary
        print("")

        for k, v in doc.items():
            if k != "_id":
                update_doc[k] = input(k.capitalize() + " [" + v + "] > ")
                # Shows current value in [] e.g.  Occupation [researcher] >
                if update_doc[k] == "":     # if not updated
                    update_doc[k] = v       # keep original value

        try:
            coll.update_one(doc, {"$set": update_doc})
            print("Document updated")
        except:
            print("Error accessing the database")


def delete_record():
    doc = get_record()
    if doc:
        update_doc = {}                # dictionary
        print("")

        for k, v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())
                # defensive programming - make sure we delete the correct record

        print("")
        confirmation = input("Is this the document you want to delete?\nY or N > ")
        print("")

        if confirmation.lower() == "y":
            try:
                coll.delete_one(doc)
                print("Document deleted!")
            except:
                print("Error accessing the database")
        else:
            # if y/n not entered
            print("Document not deleted")

\
def main_loop():
    while True:
        option = show_menu()
        if option == "1":
            add_record()
        elif option == "2":
            find_record()
        elif option == "3":
            edit_record()
        elif option == "4":
            delete_record()
        elif option == "5":
            conn.close()  # close the DB connection
            break
        else:
            print("Invalid option")
        print("")


conn = mongo_connect(MONGO_URI)
coll = conn[DATABASE][COLLECTION]
main_loop()
