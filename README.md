# Telegram Backend

This repository contains the backend API for managing Telegram chats and user authentication. The project is built using **FastAPI** and provides secure endpoints for interacting with Telegram and managing user data.

## Features

- **User Authentication**: Register, login, and logout functionality with JWT-based authentication.
- **Telegram Integration**: Connect your Telegram account and logout account, retrieve chats, and fetch messages.
- **API Endpoints**: Provides a robust API for frontend integration.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/VrenTati/TelegramViewerAPI.git
cd TelegramViewerAPI
```

### 2. Install Dependencies

Create a virtual environment and install required packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root of the project and set the following variables:

```env
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
```

### 4. Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`.

## API Endpoints

### Authentication Endpoints

- **`POST /auth/register`**: Register a new user.
  - Request Body: `{ "email": "user@example.com", "password": "password123" }`
  - Response: `201 Created`

- **`POST /auth/login`**: Authenticate a user and retrieve a token.
  - Request Body: `{ "email": "user@example.com", "password": "password123" }`
  - Response: `{ "access_token": "token", "token_type": "bearer", "phone": "optional" }`

- **`POST /auth/logout`**: Logout a user.
  - Response: `200 OK`

### Telegram Integration Endpoints

- **`POST /telegram/connect`**: Send a code to the user’s Telegram account.
  - Query Parameters: `phone=+123456789`
  - Response: `{ "status": "success", "message": "Code sent to your Telegram account" }`

- **`POST /telegram/login`**: Complete Telegram login using the verification code.
  - Query Parameters: `phone=+123456789, code=12345`
  - Response: `{ "status": "success", "message": "Login successful" }`

- **`GET /telegram/chats`**: Retrieve all chats for the connected Telegram account.
  - Query Parameters: `phone`
  - Response: `{ "status": "success", "data": { "chats": [...] } }`

- **`GET /telegram/messages`**: Retrieve messages for a specific chat.
  - Query Parameters: `phone`, `chat_id`, `limit - optional`
  - Response: `{ "status": "success", "data": { "messages": [...] } }`

- **`POST /telegram/logout`**: Disconnect the Telegram account.
  - Query Parameters: `phone`
  - Response: `{ "status": "success", "message": "Logout successful" }`

## Database

The project uses **SQLite** by default for database management. SQLAlchemy is used as the ORM, making it easy to switch to other databases if needed.

### Database Models

- **User**: Stores user data including email, hashed password, and optional phone number.
- **Base**: SQLAlchemy’s declarative base for defining models.

## Related Repositories

- **Frontend**: [Telegram Frontend](https://github.com/VrenTati/TelegrameViewerWEB)

