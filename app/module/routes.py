from flask import request, jsonify, make_response
from app import app
from .models import *
from .schema import *
from .const import HttpStatus
import bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps


# --------------------- WRAPPER CLASS FOR COOKIE-------------------------------

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        print(request.headers)
        if 'auth-token' in request.cookies:
            token = request.cookies['auth-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
            print(data)
            current_user = Users.query.filter_by(userId=data['userId']).first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated


# --------------------- DIVISIONS ENDPOINTS -------------------------

@app.route("/divisions", methods=['GET'])
def getDivisions():
    all_divisions = Division.query.all()
    results = divisions_schema.dump(all_divisions)
    return jsonify(results)


@app.route("/divisions/<dcode>", methods=['GET'])
def getDivisionByCode(dcode):
    division = Division.query.filter(Division.divisionCode == dcode).first()
    return division_schema.jsonify(division)


@app.route("/divisions/add", methods=['POST'])
def addDivision():
    divisionName = request.json.get('divisionName')
    technical = request.json.get('technical')
    divisionCode = request.json.get('divisionCode')
    division = Division(divisionName, technical, divisionCode)
    db.session.add(division)
    db.session.commit()
    return division_schema.jsonify(division)


@app.route("/divisions/update/<dcode>", methods=['PUT'])
def updateDivision(dcode):
    division = Division.query.filter(Division.divisionCode == dcode).first()
    divisionName = request.json.get('divisionName')
    divisionCode = request.json.get('divisionCode')
    technical = request.json.get('technical')

    division.divisionName = divisionName
    division.divisionCode = divisionCode
    division.technical = technical

    db.session.commit()
    return division_schema.jsonify(division)


@app.route("/divisions/delete/<dcode>", methods=['DELETE'])
def deleteDivision(dcode):
    division = Division.query.filter(Division.divisionCode == dcode).first()
    db.session.delete(division)
    db.session.commit()
    return division_schema.jsonify(division)

# ---------------------- USER ENDPOINTS -----------------------


@app.route("/register", methods=['POST'])
def registerUser():
    username = request.json.get('username')
    password = request.json.get('password')
    emailId = request.json.get('emailId')
    divisionId = request.json.get('division')
    firstName = request.json.get('firstName')
    lastName = request.json.get('lastName')
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))
    user = Users(username, password, emailId, divisionId,
                 firstName=firstName, lastName=lastName)
    db.session.add(user)
    db.session.commit()
    return "User registered Successfully", 200


@app.route("/users", methods=['GET'])
@token_required
def getUsers():
    users = Users.query.all()
    return users_schema.jsonify(users)


@app.route("/login", methods=['POST'])
def loginUser():
    username = request.json.get('username')
    user = Users.query.filter(Users.username == username).first()
    print(user.userId)
    if not user:
        return "Username Not Found", 403
    else:
        password = request.json.get('password')
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            token = jwt.encode({
                'userId': user.userId,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, app.config['SECRET_KEY'], algorithm="HS256")
            print("here")
            resp = make_response(user_schema.jsonify(user), 201)
            resp.set_cookie("auth-token", token, httponly=True)
            return resp
        else:
            return "Invalid Password", 403


@app.route("/users/update/<username>", methods=['PUT'])
@token_required
def updateUser(username):
    user = Users.query.filter(Users.username == username).first()
    if not user:
        return "User Not Found", 500
    else:
        emailId = request.json.get('emailId')
        divisionId = request.json.get('divisionId')
        user.emailId = emailId
        user.divisionId = divisionId
        db.session.commit()
        return "User Details Updated", 200


@app.route("/users/delete/<username>", methods=['DELETE'])
@token_required
def deleteUser(username):
    user = Users.query.filter(Users.username == username).first()
    if not user:
        return "User Not Found", 500
    else:
        db.session.delete(user)
        db.session.commit()
        return "User Deleted Successfully", 200


# ------------------ JOBS CONTROLLER---------------------


@app.route("/jobs/add", methods=['POST'])
@token_required
def addJobs():
    jobTitle = request.json.get('jobTitle')
    postedBy = request.json.get('postedBy')
    isOpen = True
    jobDescription = request.json.get('jobDescription')
    requirements = request.json.get('requirements')
    salary = int(request.json.get('salary'))
    lastDateToApply = request.json.get('lastDateToApply')
    divisionId = request.json.get('division')

    job = Jobs(jobTitle, postedBy, isOpen, jobDescription,
               requirements, salary, lastDateToApply, divisionId)
    db.session.add(job)
    db.session.commit()

    return "Job Added Successfully", 200


@app.route("/jobs/delete/<jobId>", methods=['DELETE'])
@token_required
def deleteJob(jobId):
    job = Jobs.query.filter(Jobs.jobId == jobId).first()
    if not job:
        return "Job Not Found", 500
    else:
        db.session.delete(job)
        db.session.commit()
        return "Job Deleted Successfully", 200


@app.route("/jobs", methods=['GET'])
def getJobs():
    jobs = Jobs.query.all()
    return jobsSchema.jsonify(jobs)


@app.route("/jobs/update/<jobId>", methods=['PUT'])
@token_required
def updateJobs(jobId):
    job = Jobs.query.filter(Jobs.jobId == jobId).first()
    if not job:
        return "Job Not Found", 500
    else:
        emailId = request.json.get('emailId')
        divisionId = request.json.get('divisionId')
        job.emailId = emailId
        job.divisionId = divisionId
        db.session.commit()
        return "Job Details Updated", 200


@app.route("/jobs/<jobId>", methods=['GET'])
def getJobById(jobId):
    job = Jobs.query.filter(Jobs.jobId == jobId).first()
    return jobSchema.jsonify(job)
