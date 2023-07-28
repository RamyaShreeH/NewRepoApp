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

class Comment(db.Document):
    _id = db.SequenceField(primary_key = True)
    application_id = db.StringField(required = True)
    comment_description = db.StringField()
    created_at = db.DateTimeField(default = datetime.datetime.now)
    created_by = db.StringField()
    updated_at = db.DateTimeField()
    updated_by = db.StringField()
    deleted_at = db.DateTimeField()
    deleted_by = db.StringField()
    
class Application(db.Document):
    
    _id = db.SequenceField(primary_key = True)
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

class Accused(db.Document):
    _id = db.SequenceField(primary_key=True)
    name = db.StringField()
    designation = db.StringField()
    department = db.StringField()
    application_id = db.IntField()
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
    created_at = db.DateTimeField(default = datetime.datetime.now)
    created_by = db.StringField()
    updated_at = db.DateTimeField()
    updated_by = db.StringField()
    deleted_at = db.DateTimeField()
    deleted_by = db.StringField()



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

@app.route('/applications/<id>', methods=['PUT'])
def update_application(id):
    json = request.json
    print("Id",id)
    submitter_id = json['submitter_id']
    description = json['description']
    #application_id = id
    application_id = id
    application = Application.objects.get_or_404(_id=id)
    print("Application:",application)
    application.update(description = description, updated_at = datetime.datetime.now, updated_by = submitter_id)
    Action(application_id = application_id, action = "Updated the application", updated_at = datetime.datetime.now,  updated_by = submitter_id).save()
    return jsonify({"message":"Updated successfully."}), 200


@app.route('/applications/<id>', methods=['DELETE'])
def delete_application(id):
    json = request.json
    application_id = id
    submitter_id = json['submitter_id']
    application = Application.objects.get_or_404(_id=id)
    print("Appl:",application)
    application.update(deleted_at = datetime.datetime.now, deleted_by = submitter_id)
    Action(application_id = application_id, action = "Deleted the application", deleted_at = datetime.datetime.now, deleted_by = submitter_id).save()
    return jsonify({"message":"Deleted successfully."}), 200

#Comment apis

@app.route('/comments', methods=["POST"])
def add_comments():
    data = request.json
    application_id = data.get('application_id')
    comment_description = data.get('comment_description')

        #Todo should get application id
        #submitter_id = data.get('submitter_id') 
        #print("Submitter Id:", submitter_id)

    submitter_id = "XYZ"
    comments = Comment(application_id = application_id, comment_description = comment_description, created_by = submitter_id).save()
    #Action(application_id = 100, action = "Added the application", created_at = datetime.datetime.now).save()
    return  jsonify(comments), 201
        

@app.route('/comments', methods = ['GET'])
def  get_comments():
    page = int(request.args.get('page',1))
    limit = int(request.args.get('limit',10))
    offset = (page - 1) * limit
    list = Comment.objects.skip(offset).limit(limit)
    return  jsonify(list), 200


@app.route('/comments/<id>', methods = ['GET'])
def get_one_comment(id):
    print("Id:",id)
    comment = Comment.objects(_id=id).first_or_404()
    return jsonify(comment), 200

#Incomplete
@app.route('/comments/applications/<application_id>', methods = ['GET'])
def get_comment_by_application_id(application_id):
    print("Application Id:",application_id)
    
    comment = Comment.objects(application_id = application_id).get_or_404()
    return jsonify(comment), 200

    
@app.route('/comments/<id>', methods=['PUT'])
def update_comment(id):
    json = request.json
    print("Id",id)
    #application_id = json['application_id']
    comment_description = json['comment_description']
    submitter_id = "CDE"
    comment = Comment.objects.get_or_404(_id=id)
    comment.update(comment_description = comment_description, updated_at = datetime.datetime.now, updated_by = submitter_id)
    #Action(application_id = application_id, action = "Updated the application", updated_at = datetime.datetime.now,  updated_by = submitter_id).save()
    return jsonify({"message":"Updated successfully."}), 200


@app.route('/comments/<id>', methods=['DELETE'])
def delete_comment(id):
    json = request.json
    #application_id = json['application_id']
    submitter_id = "CDE"
    comment = Comment.objects.get_or_404(_id=id)
    comment.update(deleted_at = datetime.datetime.now, deleted_by = submitter_id)
    #Action(application_id = application_id, action = "Deleted the application", deleted_at = datetime.datetime.now, deleted_by = submitter_id).save()
    return jsonify({"message":"Deleted successfully."}), 200

#Accused apis

@app.route('/accused', methods=["POST"])
def add_accuse():
    data = request.json
    application_id = data.get('application_id')
    name = data.get('name')
    designation = data.get('designation')
    department = data.get('department')

        #Todo should get application id
        #submitter_id = data.get('submitter_id') 
        #print("Submitter Id:", submitter_id)

    submitter_id = "XYZ"
    accused = Accused(application_id = application_id, name = name, designation = designation, department = department, created_by = submitter_id).save()
    #Action(application_id = 100, action = "Added the application", created_at = datetime.datetime.now).save()
    return  jsonify(accused), 201
        

@app.route('/accused', methods = ['GET'])
def  get_accused():
    page = int(request.args.get('page',1))
    limit = int(request.args.get('limit',10))
    offset = (page - 1) * limit
    list = Accused.objects.skip(offset).limit(limit)
    return  jsonify(list), 200


@app.route('/accused/<id>', methods = ['GET'])
def get_one_accused(id):
    print("Id:",id)
    accused = Accused.objects(_id=id).first_or_404()
    return jsonify(accused), 200

    
@app.route('/accused/<id>', methods=['PUT'])
def update_accused(id):
    data = request.json
    print("Id",id)
    #application_id = json['application_id']
    name = data.get('name')
    designation = data.get('designation')
    department = data.get('department')
   
    submitter_id = "ABC"
    accused = Accused.objects.get_or_404(_id=id)
    accused.update(name = name, designation = designation, department = department, updated_at = datetime.datetime.now, updated_by = submitter_id)
    #Action(application_id = application_id, action = "Updated the application", updated_at = datetime.datetime.now,  updated_by = submitter_id).save()
    return jsonify({"message":"Updated successfully."}), 200


@app.route('/accused/<id>', methods=['DELETE'])
def delete_accused(id):
    #json = request.json
    #application_id = json['application_id']
    submitter_id = "ABC"
    accused = Accused.objects.get_or_404(_id=id)
    accused.update(deleted_at = datetime.datetime.now, deleted_by = submitter_id)
    #Action(application_id = application_id, action = "Deleted the application", deleted_at = datetime.datetime.now, deleted_by = submitter_id).save()
    return jsonify({"message":"Deleted successfully."}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message":"Not Found!."}),404

if __name__ =='__main__': 
    app.run(debug = True)