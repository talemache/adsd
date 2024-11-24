from pprint import pprint
import mongita

from mongita import MongitaClientDisk
from bson.objectid import ObjectId

client = MongitaClientDisk()

pets_db = client.pets_db

def create_database():
    pets_db = client.pets_db
    pets_db.drop_collection("kind_collection")
    kind_collection = pets_db.kind_collection
    kind_collection.insert_many([
        {
            "kind_name":'Dog', 
            "food":'Dog food', 
            "noise":'Bark'
        },
        {
            "kind_name":'Cat', 
            "food":'Cat food', 
            "noise":'Meow'
        },
        {
            "kind_name":'Fish', 
            "food":'Fish flakes', 
            "noise":'Blub'
        }
    ])
    kinds = list(kind_collection.find())
    pets_db.drop_collection("pet_collection")
    pet_collection = pets_db.pet_collection
    pets = [
        {'name':'Suzy', 'age':3, "kind_name":"Dog", 'owner':'Greg'},
        {'name':'Sandy', 'age':2, "kind_name":"Cat", 'owner':'Steve'},
        {'name':'Dorothy', 'age':1, "kind_name":"Dog", 'owner':'Elizabeth'},
        {'name':'Heidi', 'age':4, "kind_name":"Dog",'owner':'David'}
    ]
    for pet in pets:
        for kind in kinds:
            if kind["kind_name"] == pet["kind_name"]:
                pet["kind_id"] = kind["_id"]
        del pet["kind_name"]
        assert "kind_id" in pet.keys()

    pet_collection.insert_many(pets)
    
import json
import csv

def export_to_json_and_csv():
    # Connect to collections
    kind_collection = pets_db.kind_collection
    pet_collection = pets_db.pet_collection

    # Export 'kind' collection to JSON
    kinds = list(kind_collection.find())
    with open("kinds.json", "w") as kind_file:
        json.dump(kinds, kind_file, indent=4, default=str)  # default=str for ObjectId serialization

    # Export 'pet' collection to JSON
    pets = list(pet_collection.find())
    with open("pets.json", "w") as pet_file:
        json.dump(pets, pet_file, indent=4, default=str)

    # Export 'kind' collection to CSV
    with open("kinds.csv", "w", newline='') as kind_file:
        writer = csv.DictWriter(kind_file, fieldnames=["_id", "kind_name", "food", "noise"])
        writer.writeheader()
        writer.writerows(kinds)

    # Export 'pet' collection to CSV
    with open("pets.csv", "w", newline='') as pet_file:
        writer = csv.DictWriter(pet_file, fieldnames=["_id", "name", "age", "kind_id", "owner"])
        writer.writeheader()
        writer.writerows(pets)

    print("Exported pets and kinds to JSON and CSV.")


if __name__ == "__main__":
    create_database()
    export_to_json_and_csv()  # Export data to files
    print("done.")

