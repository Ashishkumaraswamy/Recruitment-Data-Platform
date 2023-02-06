from app import ma


class DivisionSchema(ma.Schema):
    class Meta:
        fields = ('divisionId', 'divisionName', 'technical', 'divisionCode')


division_schema = DivisionSchema()
divisions_schema = DivisionSchema(many=True)


class UsersSchema(ma.Schema):
    class Meta:
        fields = ('userId', 'username', 'password', 'emailId',
                  'divisionId', 'firstName', 'lastName')


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)


class JobSchema(ma.Schema):
    class Meta:
        fields = ('jobId', 'jobTitle', 'postedBy', 'isOpen', 'jobDescription',
                  'requirements', 'salary', 'lastDateToApply', 'divisionId')


jobSchema = JobSchema()
jobsSchema = JobSchema(many=True)
