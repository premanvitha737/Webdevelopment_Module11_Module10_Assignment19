# Webdevelopment_Module11_Module10_Assignment19
**JWT Authentication System**
This is a simple Flask-based application that demonstrates how to implement JWT Authentication with registration, login, token refresh, and role-based access control. The app includes endpoints for user registration, login, refreshing tokens, and accessing role-specific data (Admin and Test Taker).

**Features**
User Registration: Allows users to register with an email, password, and role.

Login: Authenticates users and returns a JWT token.

Token Refresh: Allows users to refresh their JWT token when it's expired.

Role-based Access:

Admin users can access admin-only routes.

Test taker users can access test-taker-only routes.

JWT Authentication: Secure access to the routes using JWT tokens.

Installation
Prerequisites
Python 3.x

Flask

PyJWT

Any IDE or terminal to run the application.

Steps to Set Up
Clone the Repository (or just copy the files):

bash
Copy
Edit
git clone <repository-url>
Install Dependencies:
Navigate to the project directory and install the required Python packages:

bash
Copy
Edit
pip install -r requirements.txt
Set up Configuration:

Create a file named config.py in the root directory of the project.

Add the following line to configure the SECRET_KEY:

python
Copy
Edit
SECRET_KEY = 'your_secret_key'
Run the Application:
To run the Flask app, execute the following command in the terminal:

bash
Copy
Edit
python app.py
This will start the application on http://127.0.0.1:5000/.

API Endpoints
1. POST /register
Registers a new user with the following JSON body:

json
Copy
Edit
{
  "email": "user@example.com",
  "password": "userpassword",
  "role": "admin"  // or "test_taker"
}
Response:

201: User registered successfully.

400: Missing required fields or user already exists.

2. POST /login
Login with email and password. Returns a JWT token upon successful authentication.

json
Copy
Edit
{
  "email": "user@example.com",
  "password": "userpassword"
}
Response:

200: A JWT token is returned:

json
Copy
Edit
{
  "token": "<JWT-TOKEN>"
}
401: Invalid credentials.

3. POST /refresh-token
Refreshes the JWT token by using the existing token. Authorization header must include the current token:

bash
Copy
Edit
x-access-token: <current-jwt-token>
Response:

200: A new JWT token is returned.

4. GET /admin-data
Admin-only route. Accessible only by users with the admin role. Requires JWT token in the header.

Response:

200: Welcome message for admin.

5. GET /test-data
Test-taker-only route. Accessible only by users with the test_taker role. Requires JWT token in the header.

Response:

200: Welcome message for test taker.

**Testing with Postman**
You can test this API using Postman or any other API testing tool.

Register a new user by making a POST request to /register.

Login by making a POST request to /login with email and password to get the JWT token.

Access role-based routes (/admin-data, /test-data) by sending a GET request with the JWT token in the x-access-token header.

Refresh the token by making a POST request to /refresh-token with the old JWT token in the header.

**Conclusion**
This project demonstrates the usage of JWT Authentication in a Flask-based backend, focusing on user registration, login, token management, and role-based access control. The simplicity of this app makes it a great starting point for more complex authentication systems in web applications.
