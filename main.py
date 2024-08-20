import logging
from flask import Flask, request, jsonify
from huggingface_hub import InferenceClient

# Initialize Flask app
app = Flask(__name__)
app.config['DEBUG'] = True  # Enable debug mode

# Initialize InferenceClients with tokens
llama_client = InferenceClient(
    model="meta-llama/Llama-2-7b-chat-hf",
    token="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"
)

mistral_client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token="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"
)

# Dictionary to hold clients
clients = {
    "llama2": llama_client,
    "mistral": mistral_client
}

# Dictionary to store conversations
conversations = {}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/select_model', methods=['POST'])
def select_model():
    """
    Endpoint to select the model for a user.
    """
    data = request.get_json()
    logger.info(f"Received data for select_model: {data}")
    
    if not data:
        return jsonify({"error": "No data received"}), 400
    
    user_id = data.get('user_id')
    model_name = data.get('model')

    # Validate inputs
    if not user_id or not model_name:
        return jsonify({"error": "user_id or model missing"}), 400

    if model_name not in clients:
        return jsonify({"error": "Model not found"}), 404
    
    # Initialize conversation history for the user
    conversations[user_id] = {"model": model_name, "history": []}
    logger.info(f"Model {model_name} selected for user {user_id}")
    return jsonify({"message": f"Model {model_name} selected"}), 200

@app.route('/query', methods=['POST'])
def query():
    """
    Endpoint to query the selected model.
    """
    data = request.get_json()
    logger.info(f"Received data for query: {data}")
    
    if not data:
        return jsonify({"error": "No data received"}), 400
    
    user_id = data.get('user_id')
    question = data.get('question')
    model_name = data.get('model')

    # Validate inputs
    if not user_id or not question or not model_name:
        return jsonify({"error": "user_id, question, or model missing"}), 400
    
    if user_id not in conversations:
        if model_name in clients:
            conversations[user_id] = {"model": model_name, "history": []}
        else:
            return jsonify({"error": "Model not found"}), 404
    
    client = clients[model_name]

    # Construct the messages with the previous history, ensuring alternating roles
    history = conversations[user_id]["history"]
    messages = []
    for i, (q, a) in enumerate(history):
        messages.append({"role": "user", "content": q})
        if a:  # Include assistant's answer if available
            messages.append({"role": "assistant", "content": a})
    messages.append({"role": "user", "content": question})
    
    logger.info(f"Messages sent to model: {messages}")

    try:
        # Using InferenceClient to get the response
        response = client.chat_completion(messages=messages, max_tokens=500)
        logger.info(f"Raw response from model: {response}")

        # Extracting the answer
        answer = ""
        for choice in response.get('choices', []):
            if 'message' in choice and 'content' in choice['message']:
                answer += choice['message']['content']
            elif 'delta' in choice and 'content' in choice['delta']:  # For backward compatibility
                answer += choice['delta']['content']
            elif 'text' in choice:  # In case the response format is different
                answer += choice['text']

        if not answer:
            answer = "No valid response received from the model."

        # Store the question and answer in the conversation history
        conversations[user_id]["history"].append((question, answer))
        logger.info(f"Updated conversation history for user {user_id}: {conversations[user_id]['history']}")

        return jsonify({"answer": answer}), 200

    except Exception as e:
        logger.error(f"Error during model query: {e}")
        return jsonify({"error": "An error occurred during the model query"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
