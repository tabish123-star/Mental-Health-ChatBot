# Mental Health Chatbot - FastAPI

A beginner-friendly mental health support chatbot project using Python and FastAPI.

## Features

- FastAPI REST API
- Rule-based chatbot
- Basic intent detection
- Basic mood detection
- Crisis keyword detection
- Supportive non-diagnostic responses
- SQLite chat history
- Mood history
- CORS support
- Swagger API documentation
- Separate Python files for clean project structure

## Project Structure

```text
mental_health_chatbot/
│
├── main.py
├── chatbot.py
├── database.py
├── requirements.txt
├── .env.example
└── README.md
```

## Installation

Create a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install packages:

```bash
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn main:app --reload
```

Or:

```bash
python main.py
```

Open:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Example Chat Request

POST `/chat`

```json
{
    "user_id": "user123",
    "message": "I am feeling very anxious today."
}
```

Example response:

```json
{
    "user_id": "user123",
    "message": "I am feeling very anxious today.",
    "response": "It sounds like you may be dealing with a lot of worry...",
    "mood": "anxious",
    "crisis_detected": false
}
```

## Other Endpoints

GET `/`

GET `/health`

POST `/chat`

POST `/mood`

GET `/history/{user_id}`

GET `/moods/{user_id}`

DELETE `/history/{user_id}`

## Important

This is an educational software project. It is not a replacement for a psychologist,
psychiatrist, doctor, emergency service, or crisis counselor.

The chatbot should not diagnose mental health conditions or make medical decisions.
For a real production system, use professional clinical review, secure data handling,
authentication, encryption, privacy controls, and carefully validated safety workflows.
