
# Full-Stack Web Application with GraphQL and ReactJS

Application handles user authentication, registration, and sign-in counting functionality with real-time updates.

## Access the Application
- You can access the application here: http://18.185.46.107:3000/register You can test the application using the same logic as for local testing.

- Backend hosted API: http://18.185.46.107:8000/graphql

### Important Note: 
If you encounter any issues, please try clearing your browser cache.

### Environment Setup

For this test project, the `.env` file is included directly in the repository for easy setup. 

**Note:** In a real-world project, sensitive configuration values should not be committed to the repository. Use a pattern file like `.env.pattern` and add the actual `.env` file to `.gitignore`.

## Setup and Installation (Local)

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

## Testing Locally with Postman

### 1. Register a User:

- Open your browser and register a new user at `http://localhost:3000/register`.

### 2. Get Access Token:

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

- Copy the access token from the response.

    <img width="606" alt="Screenshot 2024-06-08 at 17 01 20" src="https://github.com/Qildeli/sign-in-tracker/assets/64167139/fbf37c95-8f18-4181-bfb3-93e26150d7ce">


    
### 3. WebSocket Connection:


- In Postman, create a new WebSocket request to `ws://localhost:8000/ws`.
- Add the access token to the WebSocket message as it is protected and send request.
    ```
    {
      "type": "authenticate",
      "token": "jwt_access_token_example"
    }
    ```

    <img width="606" alt="Screenshot 2024-06-08 at 17 00 42" src="https://github.com/Qildeli/sign-in-tracker/assets/64167139/eb88e781-9829-42f3-aef4-dd612348aa63">


### 4. Login Again:

- Try to log in again with the same user in Postman using the same endpoint and credentials or register with a new user.
- Observe the updates in the browser and in Postman how personal and public sign-in counts are updated live.

    https://github.com/Qildeli/sign-in-tracker/assets/64167139/50cdb661-4594-421c-b514-504f7044acf9

- You can test it by logging in two different browser also:
  
    <img width="1111" alt="Screenshot 2024-06-08 at 17 19 46" src="https://github.com/Qildeli/sign-in-tracker/assets/64167139/7ecc9789-1823-4f7d-a79f-9fa9b182a75d">


