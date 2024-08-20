
# 🚀 Python LLM Server

This project is a Python server that allows users to select between two language models (Llama2 and Mistral), send queries to the selected model, and maintain the context of the conversation.

## ✨ Features

1. Select between Llama2 and Mistral models.
2. Send queries to the selected model and get answers.
3. Maintain the conversation context (previous questions and answers).

## 🛠 Getting Started

### 📋 Prerequisites

- Docker
- Python 3.10

### 🔧 Setup

1. Clone the repository.

```sh
git clone https://github.com/al0olo/python-llm-server.git
cd PYTHON-LLM-SERVER
```

2. Create a virtual environment and activate it.

```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Build and run the Docker container.

```sh
docker build --no-cache -t python-llm-server .
docker run -p 8000:8000 python-llm-server
```

### 🌐 API Endpoints

#### 📦 Select Model

- **URL:** `/select_model`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "user_id": "123",
    "model": "llama2"
  }
  ```
- **Response:**
  ```json
  {
    "message": "Model llama2 selected"
  }
  ```

#### 📦 Query Model

- **URL:** `/query`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "user_id": "123",
    "model": "llama2",
    "question": "What is the capital of France?"
  }
  ```
- **Response:**
  ```json
  {
    "answer": "The capital of France is Paris."
  }
  ```

### 📝 Example cURL Requests

#### 📦 Select Model

```sh
curl --location 'http://localhost:8000/select_model' --header 'Content-Type: application/json' --data '{
    "user_id": "123",
    "model": "llama2"
}'
```

#### 📦 Query Model

```sh
curl --location 'http://localhost:8000/query' --header 'Content-Type: application/json' --data '{
    "user_id": "123",
    "model": "llama2",
    "question": "What is the capital of France?"
}'
```

### 📝 Example Conversation

1. Select the model:

```sh
curl --location 'http://localhost:8000/select_model' --header 'Content-Type: application/json' --data '{
    "user_id": "123",
    "model": "llama2"
}'
```

2. Ask the first question:

```sh
curl --location 'http://localhost:8000/query' --header 'Content-Type: application/json' --data '{
    "user_id": "123",
    "model": "llama2",
    "question": "Who is the president of the USA?"
}'
```

3. Ask a follow-up question to maintain context:

```sh
curl --location 'http://localhost:8000/query' --header 'Content-Type: application/json' --data '{
    "user_id": "123",
    "model": "llama2",
    "question": "What age is he?"
}'
```

### 📑 Postman Collection

You can import the provided Postman collection [here](https://dark-resonance-874488.postman.co/workspace/public~d3c714b6-434c-42c6-96b0-ffa97ea17e00/collection/8821057-0252beef-aad2-4b21-8774-6ef98fae99cb?action=share&creator=8821057) to test the endpoints.

### 🔧 Note on Model Selection

Please note that I am using the `InferenceClient` interface to interact with the models. This approach was chosen because downloading and setting up the models locally can be time-consuming.
