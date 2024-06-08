# Full-Stack Web Application with GraphQL and ReactJS

Application handles user authentication, registration, and sign-in counting functionality with real-time updates.


### Setup and Installation (Local)

1. Clone the repository:
```
git clone https://github.com/qildeli/sign-in-tracker.git
cd sign-in-tracker
```

2. Start the application using Docker Compose:
```
docker-compose up --build
```

3. Access the application:
- Backend API: `http://localhost:8000`
- Frontend: `http://localhost:3000`

### Testing Locally with Postman

#### 1. Register a User:

- Open your browser and register a new user at `http://localhost:3000/register`.
https://github.com/Qildeli/sign-in-tracker/assets/64167139/2e6f2c2e-c8b0-4cec-832b-b7f93c2a3ec3



#### 2. Get Access Token:

- Open Postman and create a new HTTP request to log in with the registered user.
Use the endpoint POST `http://localhost:8000/graphql` with the user's credentials. Choose body and type GraphQL.
    ```
    mutation {
      login(input: { email: "example@example.com", password: "securepassword" }) {
        user {
          id
          email
          signInCount
        }
        accessToken
      }
    }
    ```

Copy the access token from the response.
    
#### 3. WebSocket Connection:

- In Postman, create a new WebSocket request to `ws://localhost:8000/ws`.
- Add the access token to the WebSocket message as it is protected and send request.
    ```
    {
      "type": "authenticate",
      "token": "jwt_access_token_example"
    }
    ```

#### Login Again:

- Try to log in again with the same user in Postman using the same endpoint and credentials.
- Observe the updates in the browser and in Postman as the personal and sign-in counts are updated live.


Video Demonstration

