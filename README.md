
# Learning Management System (LMS)

This is a Learning Management System (LMS) built with FastAPI and MongoDB using asynchronous architecture. The project includes multi-role authentication and authorization for different user types such as Software Admin, Organization Admin, and Organization User.

## Features

- **Role-based Authentication and Authorization**: 
  - Three main user roles: Software Admin, Organization Admin, and Organization User.
  - Role-based access control for specific API routes.
  - JWT-based authentication for secure user login.
  
- **Organization Management**: 
  - Software Admins can create organizations.
  - Organization Admins can manage users within their organization.

- **User Management**:
  - Auto-generated passwords for users upon creation.
  - Separate login and signup mechanisms for Software Admins, Organization Admins, and Organization Users.
  
- **MongoDB Integration**:
  - Asynchronous operations using `motor`, a non-blocking MongoDB driver.
  - User data is stored in separate collections based on role.

## Technologies Used

- **FastAPI**: A modern, fast web framework for building APIs with Python 3.7+ based on standard Python-type hints.
- **MongoDB**: A NoSQL database for storing user and organization data.
- **Motor**: An asynchronous MongoDB driver for seamless integration with FastAPI.
- **JWT**: JSON Web Token for secure authentication.
- **Pydantic**: Data validation and parsing based on Python type hints.
- **Passlib**: Password hashing and verification.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/lms-api.git
   cd lms-api
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   Create a `.env` file in the root directory and add the following configurations:

   ```
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   MONGO_DB_URL=mongodb://localhost:27017
   ```

5. Start the FastAPI application:

   ```bash
   uvicorn app.main:app --reload
   ```

6. Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

## API Endpoints

### Authentication

- **Software Admin Sign-In**: 
  - `POST /admin/sign-in/`
  - Returns a JWT token for Software Admin.

- **Organization Admin Sign-In**: 
  - `POST /organization/sign-in/`
  - Returns a JWT token for Organization Admin.

- **Organization User Sign-In**: 
  - `POST /user/sign-in/`
  - Returns a JWT token for Organization Users.

### Organization Management

- **Create Organization**: 
  - `POST /admin/organization/create/`
  - Requires Software Admin permissions.
  
### User Management

- **Create Organization User**: 
  - `POST /organization/user/create/`
  - Allows Organization Admin to create users within their organization.


## Future Improvements

- Add support for additional roles and permissions.
- Improve security features (e.g., rate limiting, IP whitelisting).
- Enhance organization-specific reporting and user analytics.

## Contributing

Contributions are welcome! Please submit a pull request with detailed changes and ensure all tests pass before submitting.

## License

This project is licensed under the MIT License.
