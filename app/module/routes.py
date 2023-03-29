from flask import request, jsonify, make_response, render_template
from app import app
from .models import *
from .schema import *
from .const import *
import bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps


# --------------------- WRAPPER CLASS FOR COOKIE-------------------------------

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # token = None
        # # jwt is passed in the request header
        # if 'auth-token' in request.cookies:
        #     token = request.cookies['auth-token']
        # # return 401 if token is not passed
        # if not token:
        #     return response('Token is missing !!',
        #                     HttpStatus.UNAUTHORIZED)
        # try:
        #     # decoding the payload to fetch the stored details
        #     data = jwt.decode(
        #         token, app.config['SECRET_KEY'], algorithms=["HS256"])
        #     current_user = Users.query.filter_by(userId=data['userId']).first()
        # except:
        #     return response('Auth Token is Invalid!',
        #                     HttpStatus.UNAUTHORIZED)
        # # returns the current logged in users contex to the routes
        # return f(current_user, *args, **kwargs)
        pass
    return decorated

# --------------------- HOME PAGE -------------------------


@app.route("/")
def home():
    return render_template('home.html')

# --------------------- DIVISIONS ENDPOINTS -------------------------


@app.route("/divisions", methods=['GET'])
def getDivisions():
    all_divisions = Division.query.all()
    results = divisions_schema.dump(all_divisions)
    return make_response(jsonify(results),
                         HttpStatus.OK)


@app.route("/divisions/<dcode>", methods=['GET'])
def getDivisionByCode(dcode):
    division = Division.query.filter(Division.divisionCode == dcode).first()
    if not division:
        return response("Invalid Division Code Specified!", HttpStatus.INTERNAL_SERVER_ERROR)
    return make_response(division_schema.jsonify(division),
                         HttpStatus.OK)


@app.route("/divisions/add", methods=['POST'])
def addDivision():
    divisionName = request.json.get('divisionName')
    technical = request.json.get('technical')
    divisionCode = request.json.get('divisionCode')
    try:
        division = Division(divisionName, technical, divisionCode)
        db.session.add(division)
        db.session.commit()
        return make_response(division_schema.jsonify(division),
                             HttpStatus.CREATED)
    except Exception as e:
        return response("Invalid Input Payload Supplied", HttpStatus.INTERNAL_SERVER_ERROR)


@app.route("/divisions/update/<dcode>", methods=['PUT'])
def updateDivision(dcode):
    division = Division.query.filter(Division.divisionCode == dcode).first()
    divisionName = request.json.get('divisionName')
    divisionCode = request.json.get('divisionCode')
    technical = request.json.get('technical')

    division.divisionName = divisionName
    division.divisionCode = divisionCode
    division.technical = technical
    try:
        db.session.commit()
        return make_response(division_schema.jsonify(division),
                             HttpStatus.OK)
    except Exception as e:
        return response("Invalid Input Payload Supplied", HttpStatus.INTERNAL_SERVER_ERROR)


@app.route("/divisions/delete/<dcode>", methods=['DELETE'])
def deleteDivision(dcode):
    division = Division.query.filter(Division.divisionCode == dcode).first()
    if not division:
        return response("Invalid Division Code Specified", HttpStatus.INTERNAL_SERVER_ERROR)
    db.session.delete(division)
    db.session.commit()
    return make_response(division_schema.jsonify(division),
                         HttpStatus.OK)

# ---------------------- USER ENDPOINTS -----------------------


@app.route("/users", methods=['GET'])
# @token_required
def getUsers(current_user):
    users = Users.query.all()
    return make_response(users_schema.jsonify(users), HttpStatus.OK)


@app.route("/users/register", methods=['POST'])
def registerUser():
    username = request.json.get('username')
    password = request.json.get('password')
    emailId = request.json.get('emailId')
    divisionId = request.json.get('divisionId')
    firstName = request.json.get('firstName')
    lastName = request.json.get('lastName')
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))
    user = Users(username, password, emailId, divisionId,
                 firstName=firstName, lastName=lastName)
    db.session.add(user)
    try:
        db.session.commit()
        return response(
            'User Registered Successfully',
            HttpStatus.OK
        )
    except Exception as e:
        return response("Invalid Input Payload Supplied", HttpStatus.INTERNAL_SERVER_ERROR)


@app.route("/users/login", methods=['POST'])
def loginUser():
    username = request.json.get('username')
    user = Users.query.filter(Users.username == username).first()
    if not user:
        return response("Username Not Found",
                        HttpStatus.INTERNAL_SERVER_ERROR)
    else:
        password = request.json.get('password')
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            token = jwt.encode({
                'userId': user.userId,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, app.config['SECRET_KEY'], algorithm="HS256")
            resp = make_response(user_schema.jsonify(user),
                                 HttpStatus.OK)
            resp.set_cookie("auth-token", token, httponly=True)
            return resp
        else:
            return response("Invalid Password",
                            HttpStatus.FORBIDDEN)


@app.route("/users/update/<username>", methods=['PUT'])
# @token_required
def updateUser(current_user, username):
    user = Users.query.filter(Users.username == username).first()
    if not user:
        return response("Username Not Found", HttpStatus.INTERNAL_SERVER_ERROR)
    elif current_user.userId != user.userId:
        return response('User not Authorized to update Information', HttpStatus.UNAUTHORIZED)
    else:
        username = request.json.get('username')
        emailId = request.json.get('emailId')
        divisionId = request.json.get('divisionId')
        firstName = request.json.get('firstName')
        lastName = request.json.get('lastName')

        user.username = username
        user.firstName = firstName
        user.lastName = lastName
        user.emailId = emailId
        user.divisionId = divisionId

        db.session.commit()
        return response("User Details Updated",
                        HttpStatus.OK)


@app.route("/users/delete/<username>", methods=['DELETE'])
# @token_required
def deleteUser(current_user, username):
    user = Users.query.filter(Users.username == username).first()
    if not user:
        return response("Username Not Found",
                        HttpStatus.INTERNAL_SERVER_ERROR)
    else:
        db.session.delete(user)
        db.session.commit()
        return response("User Deleted Successfully",
                        HttpStatus.OK)


# ------------------ JOBS CONTROLLER---------------------


@app.route("/jobs/add", methods=['POST'])
def addJobs():
    jobTitle = request.json.get('jobTitle')
    postedBy = request.json.get('postedBy')
    isOpen = True
    jobDescription = request.json.get('jobDescription')
    requirements = request.json.get('requirements')
    salary = int(request.json.get('salary'))
    lastDateToApply = request.json.get('lastDateToApply')
    divisionId = request.json.get('divisionId')

    job = Jobs(jobTitle, postedBy, isOpen, jobDescription,
               requirements, salary, lastDateToApply, divisionId)
    db.session.add(job)
    try:
        db.session.commit()
        return response("Job Added Successfully",
                        HttpStatus.CREATED)
    except Exception as e:
        return response("Invalid Input Payload Supplied",
                        HttpStatus.INTERNAL_SERVER_ERROR)


@app.route("/jobs/delete/<jobId>", methods=['DELETE'])
# @token_required
def deleteJob(current_user, jobId):
    job = Jobs.query.filter(Jobs.jobId == jobId).first()
    if not job:
        return response("Job Not Found",
                        HttpStatus.INTERNAL_SERVER_ERROR)
    elif current_user.userId != job.postedBy:
        return response('User is Not Authorized to delete this job',
                        HttpStatus.UNAUTHORIZED)
    else:
        db.session.delete(job)
        db.session.commit()
        return response("Job Deleted Successfully",
                        HttpStatus.OK)


@app.route("/jobs", methods=['GET'])
# @token_required
def getJobs(current_user):
    jobs = Jobs.query.all()
    return make_response(jobsSchema.jsonify(jobs), HttpStatus.OK)


@app.route("/jobs/update/<jobId>", methods=['PUT'])
# @token_required
def updateJobs(current_user, jobId):
    job = Jobs.query.filter(Jobs.jobId == jobId).first()
    if not job:
        return response("Job Not Found", HttpStatus.INTERNAL_SERVER_ERROR)
    elif current_user.userId != job.postedBy:
        return response('User is Not Authorized to delete this job',
                        HttpStatus.UNAUTHORIZED)
    else:
        jobTitle = request.json.get('jobTitle')
        postedBy = request.json.get('postedBy')
        isOpen = True
        jobDescription = request.json.get('jobDescription')
        requirements = request.json.get('requirements')
        salary = int(request.json.get('salary'))
        lastDateToApply = request.json.get('lastDateToApply')
        divisionId = request.json.get('divisionId')

        job.jobTitle = jobTitle
        job.postedBy = postedBy
        job.isOpen = isOpen
        job.jobDescription = jobDescription
        job.requirements = requirements
        job.salary = salary
        job.lastDateToApply = lastDateToApply
        job.divisionId = divisionId

        db.session.commit()
        return response("Job Details Updated", HttpStatus.OK)


@app.route("/jobs/<jobId>", methods=['GET'])
# @token_required
def getJobById(jobId, current_user):
    job = Jobs.query.filter(Jobs.jobId == jobId).first()
    return make_response(jobSchema.jsonify(job), HttpStatus.OK)
