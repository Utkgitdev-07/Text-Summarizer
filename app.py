import os
from flask import Flask, request, jsonify, render_template
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Define model path
MODEL_PATH = os.path.join("models", "text_summarizer_full.pth")

# Load tokenizer (Must match the trained model)
tokenizer = T5Tokenizer.from_pretrained("t5-small")

# Load model correctly
try:
    model = T5ForConditionalGeneration.from_pretrained("t5-small")  # Load architecture
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))  # Load weights
    model.eval()  # Set model to evaluation mode
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Serve frontend

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.form.get('text', '').strip()  # Get and clean input
        if not data:
            return jsonify({'error': 'No text provided'}), 400

        print(f"📥 Received Text: {data[:100]}...")  # Log first 100 characters

        # Prepend prefix for T5
        input_text = "summarize: " + data

        # Tokenize input
        tokenized = tokenizer([input_text], return_tensors='pt', truncation=True, padding=True, max_length=512)
        tokenized = {k: v.to("cpu") for k, v in tokenized.items()}  # Move to CPU

        print(f"✅ Tokenized Input Shape: {tokenized['input_ids'].shape}")

        if tokenized["input_ids"].shape[1] == 0:  # Ensure input is not empty
            return jsonify({'error': 'Text is too short or could not be processed'}), 400

        # Generate summary (T5 requires `decoder_start_token_id`)
        results = model.generate(
            **tokenized,
            max_length=256,
            num_beams=4,
            early_stopping=True,
            decoder_start_token_id=tokenizer.pad_token_id  # Required for T5
        )

        # Decode output
        summary = tokenizer.decode(results[0], skip_special_tokens=True)

        print("✅ Summary Generated:", summary)
        return jsonify({'summary': summary})  # Return summarized text

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({'error': 'An error occurred: ' + str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port) # Run app
