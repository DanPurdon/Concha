# Concha

---DOCKER---

GETTING STARTED:
In command prompt (with docker installed)
docker pull danpurdon/concha-web

CONTAINER FOR TESTS
docker run --name conchatests -p 8000:8000 -d danpurdon/concha-web python manage.py test
-- automatically runs all included unit tests, log in terminal

CONTAINER FOR SERVER
docker run --name conchaserver -p 8000:8000 -d danpurdon/concha-web python manage.py runserver 0.0.0.0:8000

With the server running, you can test API calls using Postman or a similar tool to ensure authentication is working correctly. Use the following information:

http://localhost:8000 (url options are /audio or /users)
Content-Type application/json
Authorization Token fa2eba9be8282d595c997ee5cd49f2ed31f65bed


GET QUERIES

GET User(single):
http://localhost:8000/users/(user ID#)
GET Users(list):
http://localhost:8000/users
GET Users(searchQ)
http://localhost:8000/users?(parameter)=(query)
Valid query parameters include id, firstname, lastname, email, and address 

GET Audio(single):
http://localhost:8000/audio/(session ID#)
GET Audio(list):
http://localhost:8000/audio
GET Audio(searchQ)
http://localhost:8000/audio?id=(session ID#)
Only valid query for audio is ID #


POST AND UPDATE OPERATIONS

USERS:
Required format: 
{
    "username": "iceman5003",
    "password": "wizardsrule",
    "email": "iceking@ooo.com",
    "first_name": "Ice",
    "last_name": "King",
    "address": "Ice Kingdom, Ooo",
    "image": "https://www.looper.com/img/gallery/why-ice-king-is-the-most-tragic-character-in-adventure-time/intro-1619451691.webp"
}
POST User:
http://localhost:8000/users
New audiouser and linked user account created

UPDATE User:
http://localhost:8000/users/(user ID)
Update any of the above information

AUDIO:
Required format:
{
    "step_count": 3,
    "ticks": [-99.99, -98.33, -97.47, -89.03999999999999, -84.61, -80.18, -75.75, -71.32, -66.89, -62.46, -58.03, -53.6, -49.17, -44.74, -39.31],
    "selected_tick": 7,
    "session_id": 100
}
POST Audio:
http://localhost:8000/audio
IF Session ID does not already exist, new Session with associated Step will be created. If it does exist, new Step entry will be created for that session. (Max 10 Steps per session, step_count can be 0-9 with no duplicates allowed.)

UPDATE Audio:
http://localhost:8000/audio(STEP ID #)
Note that the STEP ID must be used in the URL to update audio entry


DELETE OPERATIONS

DELETE User:
http://localhost:8000/users/(user ID#)

DELETE Audio (Session and ALL associated steps)
http://localhost:8000/audio/(session ID#)

DELETE Single Step
http://localhost:8000/steps/(step ID#)