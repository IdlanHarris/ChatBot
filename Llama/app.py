from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# Model and pipeline initialization
try:
    model_name = "meta-llama/LlaMA-2-7b-chat-hf"
    auth_token = "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"

    # Load tokenizer and model
    print("Loading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=auth_token)
    model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=auth_token)

    # Initialize pipeline with explicit truncation
    llama_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer
    )
    print("Pipeline initialized successfully!")
except Exception as e:
    print(f"Error during model initialization: {e}")
    llama_pipeline = None  # Ensure the app doesn't crash if initialization fails

# Route to serve the index.html page
@app.route("/")
def home():
    """
    Serve the homepage.
    Ensure that 'index.html' exists in the 'templates' folder.
    """
    return render_template("index.html")

# Route to process the POST request
@app.route("/process", methods=["POST"])
def process_input():
    """
    Process text input from the user and generate a response using the model.
    """
    if llama_pipeline is None:
        return jsonify({"error": "Model pipeline failed to initialize"}), 500

    try:
        # Log the request data
        data = request.json
        print("Received data:", data)

        # Extract the input text
        text = data.get("textInput")
        if not text:
            print("No text provided")
            return jsonify({"error": "No text provided"}), 400

        # Generate text using the pipeline with explicit truncation
        result = llama_pipeline(
            text,
            max_length=50,
            num_return_sequences=1,
            truncation=True  # Ensure input truncation
        )
        print("Generated text:", result)

        # Return the generated text
        return jsonify({"response": result[0]["generated_text"]})
    except Exception as e:
        print("Error during text generation:", str(e))
        return jsonify({"error": str(e)}), 500

# Main entry point
if __name__ == "__main__":
    app.run(debug=True)
