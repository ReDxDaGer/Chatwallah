# Chat Application

This is a simple chat application built with Flask, Flask-SocketIO, and Flask-SQLAlchemy.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Code Explanation](#code-explanation)
- [Database Models](#database-models)
- [Routes](#routes)
- [SocketIO Events](#socketio-events)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/chat-app.git
   cd chat-app
   ```
2. Create a virtual environment and activate it:

   ```bash
    python -m venv venv
    source venv/bin/activate
   ```
3. Install the dependencies:

   ```bash
    pip install -r requirements.txt
   ```
4. Run the application:

   ```bash
     python main.py
   ```

## Usage 

- Open your web browser and go to `http://127.0.0.1:5000`.
- Enter your name and either create a new room or join an existing one using the room code.
- Start chatting!

# Code Explanation
## Database Models

- Room: Represents a chat room.

    - `id`: Primary key.
    - `code`: Unique code for the room.
    - `members`: Number of members in the room.
    - `messages`: Relationship to the Message model.

- Message: Represents a chat message.

    - `id`: Primary key.
    - `name`: Name of the user who sent the message.
    - `content`: The message content.
    - `room_id`: Foreign key to the Room model.
 
## Routes
- / (GET, POST): Home route where users can create or join a chat room.
- /room (GET): Room route where users can see the chat interface and messages.

## SocketIO Events

  - `message`: Handles incoming chat messages, saves them to the database, and broadcasts them to the room.
  - `connect`: Handles user connection, joins them to the room, and updates the member count.
  - `disconnect`: Handles user disconnection, removes them from the room, and updates the member count.

## Code Structure
  
  ```
   chat-app/
├── app.py
├── templates/
│   ├── home.html
│   └── room.html
├── static/
│   └── style.css
└── requirements.txt
```

