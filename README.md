# Flask-SocketIO Chat Backend

## Installation

Both Docker and docker-compose should be installed.

```
git clone https://github.com/Telichkin/simple_chat.git
cd simple_chat
docker-compose build
docker-compose up
```

Application will run on http://localhost:8000


## API

### User creation:
```
POST /users/
Content-Type: application/json

{"username": "newUser", "password": "Weak!"}
```

### Authentication:
```
POST /auth/
Content-Type: application/json

{"username": "matureUser", "password": "Strong?"}
```

Both creation and authentication methods return token in response body.


### Backend can get events:

#### /socket.io/
event | required payload fields
 --- | ----- 
"auth" | "token"
"send private message" | "message", "to"
"broadcast" | "message"
"connect" | None
"disconnect" | None

Before start to use other events you need to authenticate through "auth" event with token.

#### /socket.io/active-users
event | required payload fields
 --- | ----- 
"connect" | None
"disconnect" | None


### Backend can send events:

#### /socket.io/
event | data
 --- | ----- 
"send private message" | {"message": .., "author": .., "to": ..}
"broadcast" | {"message": .., "author": .., "to": None}
"private history" | list with messages from "send private message" 
"broadcast history" | list with messages from "broadcast"
"error" | error message

#### /socket.io/active-users
event | data
 --- | ----- 
"update" | list with user names of active users