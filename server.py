############### Les imports #################
from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId
############### l'application #################
app = Flask(__name__)

################################
try:
    # essayer de se connecter a la DB
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    # déclenchement une exception s'il ne se connecte pas a la db
    db = mongo.company
    mongo.server_info()
except:
    print("Erreur, Ne peut pas se connecter a la DB")



############## La fonction qui cree un utilisateur ##################
@app.route("/users", methods=["POST"])
def create_user():
    try:
        user = {
            "nom":request.form["nom"], 
            "prenom":request.form["prenom"]}
        dbResponse = db.users.insert_one(user)        
        #for attr in dir(dbResponse):
        #    print(attr)
        print(dbResponse.inserted_id)
        return Response(
            response= json.dumps(
                {"message":"utilisateur cree",
                 "id":f"{dbResponse.inserted_id}"
                 }),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print("****************")
        print(ex)
        print("****************")

############## La fonction qui fait la lecture des utilisateurs ##################
@app.route("/users", methods=["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(
            response= json.dumps(data),
            status=500,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message":"incapable de lire l'utilisateur"}),
            status=500,
            mimetype="application/json"
        )

############## la fonction qui fait la mise a jour ##################
@app.route("/users/<id>",methods=["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
           {"_id":ObjectId(id)},
           {"$set":{"nom":request.form["nom"]}}
        )
        # for attr in dir(dbResponse):
        #     print(f"***********{attr}**********")
        if dbResponse.modified_count == 1:
            return Response(
                response= json.dumps({"message":"mise a jour du nom de l'utilisateur effectue"}),
                status=200,
                mimetype="application/json"
            )
        return Response(
                response= json.dumps({"message":"rien a mettre a jour "}),
                status=200,
                mimetype="application/json"
            )

    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message":"incapable de mettre a jour  l'utilisateur"}),
            status=500,
            mimetype="application/json"
        )
    
############### La fonction aui supprime l'utilisateur #################
@app.route("/users/<id>",methods=["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id":ObjectId(id)})
        # for attr in dir(dbResponse):
        #     print(f"***********{attr}**********")
        if dbResponse.deleted_count == 1:
            return Response(
                    response= json.dumps(
                        {"message":"Utilisateur supprime","id":f"{id}"}),
                    status=200,
                    mimetype="application/json"
                )
        return Response(
                    response= json.dumps(
                        {"message":"Utilisateur introuvable","id":f"{id}"}),
                    status=200,
                    mimetype="application/json"
                )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message":"incapable de supprimer  l'utilisateur"}),
            status=500,
            mimetype="application/json"
        )
############### La fonction Principale #################
if __name__ == "__main__":
    app.run(port=80, debug=True)