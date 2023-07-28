from flask import Flask, jsonify, request
from flask_mongoengine import MongoEngine
import datetime

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db':'Application',
    'host':'localhost',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)

class comment(db.Document):
    id = db.SequenceField(primary_key = True)
    comment_description = db.StringField()
    
class Application(db.Document):
    
    _id = db.SequenceField()
    submitter_id = db.StringField(required = True)
    description = db.StringField(required = True)
    state = db.StringField()
    owner = db.StringField()
    created_at = db.DateTimeField(default = datetime.datetime.now)
    created_by = db.StringField()
    updated_at = db.DateTimeField()
    updated_by = db.StringField()
    deleted_at = db.DateTimeField()
    deleted_by = db.StringField()

class Action(db.Document):
    id = db.SequenceField(primary_key=True)
    action = db.StringField()
    application_id = db.IntField()
    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()
    deleted_at = db.DateTimeField()

@app.route('/applications', methods=["POST"])
def add_application():
    #data = request.get_json()
    data = request.json
    submitter_id = data.get('submitter_id')

    #Todo should get application id
    #application_id = data.get('application_id') 
    #print("Application Id:", application_id)

    applications = Application(submitter_id = submitter_id, description = data.get('description'), state = 'new', owner = ' ', created_by = submitter_id).save()
    Action(application_id = 100, action = "Added the application", created_at = datetime.datetime.now).save()
    return  jsonify(applications), 201

@app.route('/applications', methods = ['GET'])
def  get_applications():
    '''applications = application.objects()
    return  jsonify(applications), 200'''

    page = int(request.args.get('page',1))
    limit = int(request.args.get('limit',10))
    offset = (page - 1) * limit
    list = Application.objects.skip(offset).limit(limit)
    return  jsonify(list), 200


@app.route('/applications/<id>', methods = ['GET'])
def get_one_application(id):
    print("Id:",id)
    application = Application.objects(_id=id).first_or_404()
    return jsonify(application), 200

#Incomplete
@app.route('/applications/<id>', methods=['PUT'])
def update_application(id):
    json = request.json
    print("Id",id)
    submitter_id = json['submitter_id']
    description = json['description']
    #application_id = id
    application_id = 100
    application = Application.objects.get_or_404(_id=id)
    print("Application:",application)
    application.update(description = description , updated_at = datetime.datetime.now, updated_by = submitter_id)
    Action(application_id = application_id, action = "Updated the application", updated_at = datetime.datetime.now,  updated_by = submitter_id).save()
    return jsonify({"message":"Updated successfully."}), 200


@app.route('/application/<id>', methods=['DELETE'])
def delete_application(id):
    application_id = id
    one_application = application.objects.get_or_404(id=id)
    one_application.update(isDeleted = 'True', deleted_time = datetime.datetime.now)
    action(application_id = application_id, action = "Deleted the application", deleted_time = datetime.datetime.now).save()
    return jsonify({"message":"Deleted successfully."}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message":"Not Found!."}),404

if __name__ =='__main__': 
    app.run(debug = True)