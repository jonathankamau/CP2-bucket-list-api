## Checkpoint 2: Bucket List API using flask

[![Build Status](https://travis-ci.org/andela-brotich/CP2-bucket-list-api.svg?branch=develop)](https://travis-ci.org/andela-brotich/CP2-bucket-list-api)  [![Codacy Badge](https://api.codacy.com/project/badge/Grade/315e022d5cb24679bcbba37e27b6b5bd)](https://www.codacy.com/app/brian-rotich/CP2-bucket-list-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andela-brotich/CP2-bucket-list-api&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/315e022d5cb24679bcbba37e27b6b5bd)](https://www.codacy.com/app/brian-rotich/CP2-bucket-list-api?utm_source=github.com&utm_medium=referral&utm_content=andela-brotich/CP2-bucket-list-api&utm_campaign=Badge_Coverage)

This API enables the user to create bucketlist and list of items in the bucketlist. The items can be marked as `done` when completed.

#### URL endpoints

| URL Endpoint | HTTP Methods | Summary |
| -------- | ------------- | --------- |
| `/api/v1/auth/register/` | `POST`  | Register a new user|
|  `/api/v1/auth/login/` | `POST` | Login and retrieve token|
| `/api/v1/bucketlists/` | `POST` | Create a new Bucketlist |
| `/api/v1/bucketlists/` | `GET` | Retrieve all bucketlists for user |
| `/api/v1/bucketlists/?limit=2&page=1` | `GET` | Retrieve one bucketlist per page |
| `/api/v1/bucketlists/<id>/` | `GET` |  Retrieve bucket list details |
| `/api/v1/bucketlists/<id>/` | `PUT` | Update bucket list details |
| `/api/v1/bucketlists/<id>/` | `DELETE` | Delete a bucket list |
| `/api/v1/bucketlists/<id>/items/` | `POST` |  Create items in a bucket list |
| `/api/v1/bucketlists/<id>/items/<item_id>/` | `DELETE`| Delete a item in a bucket list|
| `/api/v1/bucketlists/<id>/items/<item_id>/` | `PUT`| update a bucket list item details|

### Installation
1. create a working directory

	      $ mkdir -p work-dir
	      $ cd workdir


2. clone this repo to local
    - Via SSH

          	git clone git@github.com:andela-brotich/CP2-bucket-list-api.git

    - via HTTPS

          	git clone https://github.com/andela-brotich/CP2-bucket-list-api.git
          
3. Navigate to project directory
    
    
      		$ cd CP2-bucket-list-api
      		$ git checkout develop
      
4. (Recommended)Create virtual environment 


      	$ virtualenv bucketlist-venv
      	$ source bucketlist-venv/bin/activate
          
5. Set up the development environment for the project 


          $ pip install -r requirements.txt
          $ python manage.py db init 
          $ python manage.py db migrate 
          $ python manage.py db upgrade

6. run server    

       	$ python run.py 
          Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
         
    The API server is accessible on `http://0.0.0.0:5000/` 
### Sample API Use Case
Access the endpoints using your preferred client e.g Postman

- POST `http://0.0.0.0:5000/auth/login/`
   register new user providing username and password
 
    body: 
    
    ```
    username: brian2
    password: password
    ```
    _response_:
    
	    {
	        "message": "new user created successfully",
	        "username": "brian2"
	    }
 - POST `http://0.0.0.0:5000/auth/login/`
  login a user and get the token
    body: 
    
        username: brian2
        password: password
    
    _response_:
    
		 {
			"message": "new user created successfully",
			"username": "brian2"
		 }
  
- POST `http://localhost:5000/bucketlists/`
  create a new bucket list
  
  headers:

       	Authorization: Token brian2.C1Y5JA.fXefAieGzWOviHlh3lYYLJphk98
       
  body:
    
        bucket_name: Christmas
    
   _response_:
    
		 {
		  "data": {
		    "created_by": 1,
		    "date_created": "Tue, 10 Jan 2017 10:17:41 GMT",
		    "date_modified": "Tue, 10 Jan 2017 10:17:41 GMT",
		    "id": 1,
		    "name": "Christmas"
		  }
		  }
		  
- GET `http://localhost:5000/bucketlists/`
gets bucketlist for the user with the token supplied
  
  headers:

       	Authorization: Token brian2.C1Y5JA.fXefAieGzWOviHlh3lYYLJphk98
       	
   _response_:
   		
		{
		  "data": [
			    {
			      "created_by": 1,
			      "date_created": "Tue, 10 Jan 2017 10:17:41 GMT",
			      "date_modified": "Tue, 10 Jan 2017 10:17:41 GMT",
			      "id": 1,
			      "name": "Christmas"
			    }
			  ],
		   "next": null,
		   "prev": null
		}
		   
