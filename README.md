# Recruitment-Data-Platform
Flask based backend application for providing endpoints to a Recruitment Data Platform

# Team Members:

```
19PD06 - ASHISH K
19PD22 - MOHAMMED HAFIZ
19PD07 - BALA VIGNESH SM
19PD21 - MAADHAV K
19PD27 - HARIHARAN S
```

# How to Set up on Local

1. Clone this repository to your local machine
2. Go to MySQl Workbench or any other RDBMS and create a database named RDP
3. Create a *.env* file with the following variables
```
MYSQL_USERNAME=//your mysql username
MYSQL_PASSWORD=//your mysql password
DB_NAME=rdp
```
4. Run `pip install -r requirements.txt`
5. Run `python run.py`

### You could check the various API endpoints using Postman

# Tech-Stack

```
Flask
MySQL Database
SQL Alchemy
```

# Features provided

1. CRUD operations for recruitment data platfrom
2. JWT cookie based autorization
3. Validations to handle Edge cases

# List of Endpoints 

### Division Endpoints
1. GET http://127.0.0.1:8800/divisions (Get all divisions)
2. GET http://127.0.0.1:8800/divisions/<dcode> (Get details about the division with the given dcode)
3. POST http://127.0.0.1:8800/divisions/add (Add a division) <br/>
Payload
```
{
    "divisionName": "Division Name",
    "technical": true,
    "divisionCode": "Division Code"
}
```
4. PUT http://127.0.0.1:8800/divisions/update/<dcode> (Update details of the division with the given dcode)<br/>
Payload
```
{
    "divisionName": "Division Name",
    "technical": true,
    "divisionCode": "Division Code"
}
```
5. DELETE http://127.0.0.1:8800/divisions/delete/<dcode> (Delete details of the division with the given dcode)


### User Endpoints
1. GET http://127.0.0.1:8800/users (Get all users)
2. POST http://127.0.0.1:8800/users/register (Register a user to the Recruitment Data Platform) <br/>
Payload
```
{
    "username":"<usename>",
    "password":"<password>",
    "emailId":"<emailid>",
    "divisionId":1,
    "firstName":"<first_name>",
    "lastName":"<last_name>"
}
```
3. POST http://127.0.0.1:8800/users/login (Add a division) <br/>
Payload
```
{
    "username": "<Registered Username>",
    "password": "<Password set during regitser>",
}
```
<mark> Note: On successfull login the server sends an auth-token cookie in the response headers which is used for authorization </mark> <br/>
4. PUT http://127.0.0.1:8800/users/update/<username> (Update details of the user with the given username)<br/>
Payload
```
{
    "username":"ashish1",
    "emailId":"ashish.kumaraswamy@outlook.com",
    "divisionId":1,
    "firstName":"Ashish",
    "lastName":"K"
}
```
5. DELETE http://127.0.0.1:8800/users/delete/<username> (Delete details of the user with the given username)


### Jobs Endpoints
1. GET http://127.0.0.1:8800/jobs (Get all jobs)
2. GET http://127.0.0.1:8800/jobs/<jobId> (Get details about the job with the given jobId)
3. POST http://127.0.0.1:8800/jobs/add (Add a new job) <br/>
Payload
```
{
    "jobTitle": "<Job Title>",
    "postedBy": <User ID of the user posting the job>,
    "isOpen": <true/false>,
    "jobDescription": "<Job Description>",
    "requirements": "<requirements>",
    "salary": <salary integer value>,
    "lastDateToApply": "<date object for date>",
    "divisionId": <division id associated to this job>
}
```
4. PUT http://127.0.0.1:8800/jobs/update/<jobId> (Update details of the job with the given jobId)<br/>
Payload
```
{
    "jobTitle": "<Job Title>",
    "postedBy": <User ID of the user posting the job>,
    "isOpen": <true/false>,
    "jobDescription": "<Job Description>",
    "requirements": "<requirements>",
    "salary": <salary integer value>,
    "lastDateToApply": "<date object for date>",
    "divisionId": <division id associated to this job>
}
```
5. DELETE http://127.0.0.1:8800/jobs/delete/<jobId> (Delete job with the given jobId)



# Screenshots

## Database Tables

#### Jobs
![jobs](https://user-images.githubusercontent.com/64360092/217289916-88962e5b-0c89-45bb-b817-85702ec71346.png)

#### Users
![users](https://user-images.githubusercontent.com/64360092/217289998-d884a0cd-9417-4c08-b380-91d83263f753.png)

#### Division
![division](https://user-images.githubusercontent.com/64360092/217290043-00b7a05b-ca15-4467-832b-439a8e2492d7.png)

## Postman Screenshots

1. Register Endpoint

![register endpoint](https://user-images.githubusercontent.com/64360092/217297537-b004faee-f898-4f5d-a774-3ed7a99d6034.png)

2. Login Endpoint

![login endpoint](https://user-images.githubusercontent.com/64360092/217298279-8b7289e0-5ade-42fc-8035-c9a48e9d8a69.png)

<br/> Login Endpoint Auth cookie in response header

![auth cookie](https://user-images.githubusercontent.com/64360092/217298469-c3e13f93-1172-46e6-bef1-d810f474754d.png)

3. Adding Jobs

![add jobs](https://user-images.githubusercontent.com/64360092/217299654-7b4775c4-d0df-426e-83f1-baa8a1ca2698.png)

4.
<br/> Delete Jobs Unuathorized (ie. trying to delete jobs posted by other users)

![unauthorized delete](https://user-images.githubusercontent.com/64360092/217299844-f7ab09c0-4b99-4afb-95be-1b4845985da6.png)

<br/> Delete Jobs Authorized (ie. trying to delete jobs posted by the same user)

![authorized delete](https://user-images.githubusercontent.com/64360092/217299996-4a53bb66-568a-4d99-92db-0d739176b1a5.png)



