from app import db


class Division(db.Model):
    divisionId = db.Column(db.Integer, primary_key=True)
    divisionName = db.Column(db.String(45))
    technical = db.Column(db.Boolean)
    divisionCode = db.Column(db.String(50))

    def __init__(self, divisionName, technical, code):
        self.divisionName = divisionName
        self.divisionCode = code
        self.technical = technical

    def __repr__(self):
        return "<Division Id: {}, DivisionName: {}, Technical: {}, DivisionCode: {}>".format(self.divisionId, self.divisionName, self.technical, self.divisionCode)


class Users(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45))
    password = db.Column(db.String(200))
    emailId = db.Column(db.String(100))
    divisionId = db.Column(db.Integer)
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
    jobId = db.Column(db.Integer, primary_key=True)
    jobTitle = db.Column(db.String(100))
    postedBy = db.Column(db.Integer)
    isOpen = db.Column(db.Boolean)
    jobDescription = db.Column(db.String(10000))
    requirements = db.Column(db.String(1000))
    salary = db.Column(db.Integer)
    lastDateToApply = db.Column(db.Date)
    divisionId = db.Column(db.Integer)

    def __init__(self, jobTitle, postedBy, isOpen, jobDescription, requirements, salary, lastDateToApply, divisionId):
        self.jobTitle = jobTitle
        self.postedBy = postedBy
        self.isOpen = isOpen
        self.jobDescription = jobDescription
        self.requirements = requirements
        self.salary = salary
        self.lastDateToApply = lastDateToApply
        self.divisionId = divisionId
