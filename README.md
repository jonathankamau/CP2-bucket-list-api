## Checkpoint 2: Bucket List API using flask

[![Build Status](https://travis-ci.org/andela-brotich/CP2-bucket-list-api.svg?branch=develop)](https://travis-ci.org/andela-brotich/CP2-bucket-list-api)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/315e022d5cb24679bcbba37e27b6b5bd)](https://www.codacy.com/app/brian-rotich/CP2-bucket-list-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andela-brotich/CP2-bucket-list-api&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/315e022d5cb24679bcbba37e27b6b5bd)](https://www.codacy.com/app/brian-rotich/CP2-bucket-list-api?utm_source=github.com&utm_medium=referral&utm_content=andela-brotich/CP2-bucket-list-api&utm_campaign=Badge_Coverage)

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