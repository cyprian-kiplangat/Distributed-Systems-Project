# Flask User Authentication System

A robust web application built with Flask that provides user authentication features including registration, login, and password reset functionality. The application uses MongoDB for data storage and implements secure password handling.

## Features

- User Registration with multiple fields (email, mobile, address, registration number)
- Secure Login System
- Password Reset via Email
- User Search Functionality
- Secure Password Hashing using Werkzeug
- MongoDB Integration for Data Persistence
- Email-based Password Reset System

## Technologies Used

- Flask 3.0.2 - Python web framework
- PyMongo 4.11.0 - MongoDB driver for Python
- Werkzeug 3.1.2 - WSGI web application library
- MongoDB - NoSQL database
- SMTP - For email functionality
- HTML Templates - For frontend views

## Prerequisites

Before running this application, make sure you have:

- Python 3.x installed
- MongoDB installed and running
- A Gmail account for SMTP email service
- Git (optional, for version control)

## Installation and Setup

1. Clone the repository (if using Git):
   ```bash
   git clone https://github.com/cyprian-kiplangat/Distributed-Systems-Project.git
   cd Distributed-Systems-Project
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following variables:
   ```
   MONGO_URI=your_mongodb_connection_string
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USE_SSL=true
   MAIL_USERNAME=your_gmail_address
   MAIL_PASSWORD=your_gmail_app_password
   MAIL_DEFAULT_SENDER=your_gmail_address
   ```

   Note: For Gmail, you'll need to use an App Password if you have 2-factor authentication enabled.

## MongoDB Atlas Setup

1. Create a MongoDB Atlas account if you don't have one
2. Create a new cluster
3. Add your current IP address to the IP Access List in Network Access settings
   - Go to Network Access in the Security section
   - Click "Add IP Address"
   - Add your current IP or allow access from anywhere (not recommended for production)
4. Create a database named "flask_app_db"
5. Inside the database, create a collection named "user_registrations"
6. Get your connection string from MongoDB Atlas:
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
   - Replace <password> with your database user password

## Environment Variables

The following environment variables need to be set:

- `MONGO_URI`: Your MongoDB Atlas connection string
- `MAIL_SERVER`: SMTP server address (smtp.gmail.com for Gmail)
- `MAIL_PORT`: SMTP server port (587 for Gmail)
- `MAIL_USE_TLS`: Enable TLS for secure email (true for Gmail)
- `MAIL_USE_SSL`: Enable SSL for secure email (true for Gmail)
- `MAIL_USERNAME`: Gmail address for sending password reset emails
- `MAIL_PASSWORD`: Gmail app password for authentication
- `MAIL_DEFAULT_SENDER`: Email address used as the sender

## Running the Application

1. Ensure MongoDB is running
2. Start the Flask application:
   ```bash
   python app.py
   ```
3. Access the application at `http://localhost:5000`

## Project Structure

```
.
├── app.py                  # Main application file
├── requirements.txt        # Project dependencies
├── .env                   # Environment variables
├── templates/             # HTML templates
│   ├── index.html         # Home page
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── success.html       # Success page
│   ├── forgot_password.html    # Password reset request
│   └── reset_password.html     # Password reset page
```

## API Endpoints

- `/` - Home page
- `/login` - User login (GET, POST)
- `/register` - User registration (GET, POST)
- `/success` - Success page after login/registration
- `/forgot-password` - Password reset request
- `/reset-password/<token>` - Password reset with token
- `/mongodb` - MongoDB connection test

## Database Schema

User document structure in MongoDB:
```json
{
    "mobile": "string",
    "email": "string",
    "password": "hashed_string",
    "address": "string",
    "registration_number": "string",
    "reset_token": "string (optional)",
    "reset_token_expiry": "datetime (optional)"
}
```

## Security Features

- Passwords are hashed using Werkzeug's security functions
- Secure password reset tokens
- Token expiration for password reset links
- Password length validation
- Email verification for password reset

## Error Handling

The application includes error handling for:
- Invalid login credentials
- User not found
- Password mismatch during reset
- Expired reset tokens
- Email sending failures

## Best Practices

1. Always keep your environment variables secure
2. Never commit the `.env` file to version control
3. Use a strong password for your Gmail account
4. Regularly update dependencies for security patches

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request
