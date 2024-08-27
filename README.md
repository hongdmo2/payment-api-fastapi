
# Payment Processing System Technical Documentation

## 1. Introduction

### 1.1 Purpose
This document provides a comprehensive overview of the Payment Processing System, a FastAPI-based application designed to handle financial transactions securely and efficiently.

### 1.2 Scope
The system covers user authentication, transaction management, and basic payment processing functionalities.

### 1.3 Audience
This documentation is intended for developers, system administrators, and project stakeholders involved in the development, deployment, or maintenance of the Payment Processing System.

## 2. System Overview

### 2.1 Architecture
The system follows a microservices architecture, with the main components being:
- FastAPI web framework
- PostgreSQL database
- SQLAlchemy ORM
- Pydantic for data validation

### 2.2 Technologies Used
- Python 3.9+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT for authentication

### 2.3 Dependencies
- `fastapi`
- `uvicorn`
- `sqlalchemy`
- `pydantic`
- `psycopg2-binary`
- `python-jose[cryptography]`
- `passlib[bcrypt]`

## 3. Installation Guide

### 3.1 Prerequisites
- Python 3.9 or higher
- PostgreSQL database

### 3.2 Installation Steps
1. Clone the repository
2. Create a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Set up the PostgreSQL database
5. Configure environment variables in `.env` file

## 4. Configuration Guide

### 4.1 Configuration Parameters
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT encoding algorithm

### 4.2 Environment Setup
Create a `.env` file in the project root with the following content:

```env
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

## 5. Usage Guide

### 5.1 User Interface Overview
The system provides a RESTful API interface, accessible via HTTP requests.

### 5.2 User Authentication
Users can authenticate using JWT tokens obtained through the `/token` endpoint.

### 5.3 Core Functionality
- User registration and authentication
- Create, read, update transactions
- View transaction history

## 6. API Documentation

### 6.1 Endpoints
- `POST /users/`: Create a new user
- `POST /token`: Obtain access token
- `GET /users/me/`: Get current user info
- `POST /transactions/`: Create a new transaction
- `GET /transactions/`: List all transactions
- `GET /transactions/{transaction_id}`: Get specific transaction
- `PUT /transactions/{transaction_id}`: Update transaction status

### 6.2 Request and Response Formats
All requests and responses use JSON format.

### 6.3 Authentication and Authorization
Protected endpoints require a valid JWT token in the Authorization header.

## 7. Database Schema

### 7.1 Table Definitions
- `users`: Stores user information
- `transactions`: Stores transaction details

### 7.2 Relationships and Constraints
- One-to-many relationship between users and transactions

## 8. Testing

### 8.1 Test Plan
The system includes unit tests and integration tests for core functionalities. Tests are organized within a `tests` directory, using pytest as the testing framework.

### 8.2 Test Cases
- User registration
- Authentication
- Transaction creation and retrieval
- Database operations

### 8.3 Test Structure
The `tests` directory contains the following subdirectories and files:
- `test_users.py`: Tests related to user registration and authentication.
- `test_transactions.py`: Tests related to transaction creation, retrieval, and updates.
- `conftest.py`: Setup configurations and fixtures for pytest.

### 8.4 Test Results
All tests pass successfully, ensuring the system's reliability and correctness.

### 8.5 Running Tests
To run the tests, navigate to the project root directory and use the following command:
```bash
pytest
```

## 9. Deployment

### 9.1 Deployment Process
1. Set up a production PostgreSQL database
2. Configure environment variables for production
3. Deploy the FastAPI application using a WSGI server (e.g., Gunicorn)
4. Set up a reverse proxy (e.g., Nginx)

### 9.2 Release Notes
**Version 1.0.0:**
- Initial release with core functionalities

### 9.3 Known Issues and Limitations
- Limited to basic transaction types
- No integration with external payment gateways yet

## Difficulties Faced and Resolutions

1. **Database Connection Issues**: 
   - **Problem**: Initial difficulties in connecting to PostgreSQL database.
   - **Resolution**: Properly configured `DATABASE_URL` in the `.env` file and ensured PostgreSQL service was running.
   
2. **Authentication Implementation**: 
   - **Problem**: Challenges in implementing JWT-based authentication.
   - **Resolution**: Utilized FastAPI's built-in security utilities and implemented proper token validation.
   
3. **Data Validation Errors**: 
   - **Problem**: Inconsistencies between Pydantic models and database schema.
   - **Resolution**: Aligned Pydantic models with SQLAlchemy models and added proper validation rules.
   
4. **Swagger UI Authorization**: 
   - **Problem**: Difficulty in testing protected routes via Swagger UI.
   - **Resolution**: Implemented custom Swagger UI configuration to support OAuth2 authentication.

## Steps Left Out from Initial Plan

1. Advanced Fraud Detection: Implementation of sophisticated fraud detection algorithms was postponed for future releases.
2. Payment Gateway Integration: Integration with external payment gateways was not implemented in this version.
3. Comprehensive Logging System: While basic error handling is in place, a more robust logging system is planned for future iterations.
4. User Dashboard: Development of a frontend user interface was not part of this initial backend-focused release.
5. Performance Optimization: While the system performs well for current needs, advanced optimization techniques (like caching) were not implemented in this version.

## How to Run

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```
