from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Division(db.Model):
    __tablename__ = 'Division'
    __table_args__ = {'extend_existing': True}

    divisionId = db.Column(db.Integer, primary_key=True)
    divisionName = db.Column(db.String(45), unique=True)
    technical = db.Column(db.Boolean)
    divisionCode = db.Column(db.String(50), unique=True)

    def __init__(self, divisionName, technical, code):
        self.divisionName = divisionName
        self.divisionCode = code
        self.technical = technical

    def __repr__(self):
        return "<Division Id: {}, DivisionName: {}, Technical: {}, DivisionCode: {}>".format(self.divisionId, self.divisionName, self.technical, self.divisionCode)


class Users(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {'extend_existing': True}

    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(200))
    emailId = db.Column(db.String(100))
    divisionId = db.Column(db.Integer, db.ForeignKey('Division.divisionId'))
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))

    def __init__(self, username, password, emailId, divisionId, firstName, lastName):
        self.username = username
        self.password = password
        self.emailId = emailId
        self.divisionId = divisionId
        self.firstName = firstName
        self.lastName = lastName


class Jobs(db.Model):
    __tablename__ = 'Jobs'
    __table_args__ = {'extend_existing': True}

    jobId = db.Column(db.Integer, primary_key=True)
    jobTitle = db.Column(db.String(100))
    postedBy = db.Column(db.Integer, db.ForeignKey('Users.userId'))
    isOpen = db.Column(db.Boolean)
    jobDescription = db.Column(db.String(10000))
    requirements = db.Column(db.String(1000))
    salary = db.Column(db.Integer)
    lastDateToApply = db.Column(db.Date)
    divisionId = db.Column(db.Integer, db.ForeignKey('Division.divisionId'))

    def __init__(self, jobTitle, postedBy, isOpen, jobDescription, requirements, salary, lastDateToApply, divisionId):
        self.jobTitle = jobTitle
        self.postedBy = postedBy
        self.isOpen = isOpen
        self.jobDescription = jobDescription
        self.requirements = requirements
        self.salary = salary
        self.lastDateToApply = lastDateToApply
        self.divisionId = divisionId
