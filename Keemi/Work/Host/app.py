from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
from accelerate import Accelerator
import torch
from huggingface_hub import login
import os

# Optional: Secure your Hugging Face token by setting it as an environment variable
# os.environ["HF_HOME"] = "/path/to/your/huggingface/token"

# Log in to Hugging Face
login("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")  # Replace with your Hugging Face token (ensure it's secure)

# Initialize the Accelerator
accelerator = Accelerator()

# Model name (adjust as needed)
model_name = "meta-llama/Llama-2-7b-chat-hf"  # Replace with your specific model path or name

# Load tokenizer and model with accelerator management
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",  # Automatically place on the best available device (GPU/CPU)
    torch_dtype=torch.float16  # Use FP16 precision if supported
)

# Create the Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend communication

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get JSON data from the request
        data = request.json
        prompt = data.get('prompt', '')  # Extract the 'prompt' field

        if not prompt:
            return jsonify({'response': 'Please provide a prompt.'}), 400

        # Tokenize the input
        inputs = tokenizer(prompt, return_tensors="pt").to(accelerator.device)

        # Generate output from the model
        outputs = model.generate(inputs.input_ids, max_length=100, num_return_sequences=1)

        # Decode the response
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return jsonify({'response': generated_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
