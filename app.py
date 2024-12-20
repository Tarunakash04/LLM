from flask import Flask, render_template, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load your fine-tuned model and tokenizer
model = GPT2LMHeadModel.from_pretrained("./gpt2_finetuned")
tokenizer = GPT2Tokenizer.from_pretrained("./gpt2_finetuned")

# Set pad token id and eos token id
tokenizer.pad_token = tokenizer.eos_token
model.eval()

app = Flask(__name__)

# Route for the main HTML page
@app.route('/')
def home():
    return render_template('index.html')

# Route for processing the question and generating an answer
@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get("question")

    # Ensure input is not empty
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # Tokenize input, ensuring truncation if it's too long (max length 1024 tokens for GPT-2)
    inputs = tokenizer(question, return_tensors="pt", padding=True, truncation=True, max_length=150)
    
    # Create attention mask: 1 for actual tokens, 0 for padding tokens (if any)
    attention_mask = inputs['attention_mask'] if 'attention_mask' in inputs else None
    
    try:
        # Generate the output with explicit attention mask and pad token id
        outputs = model.generate(
            inputs['input_ids'],
            attention_mask=attention_mask,  # Explicitly pass the attention mask
            max_length=150,                 # Set the maximum length for generated response tokens
            num_return_sequences=1,         # Only return one sequence
            no_repeat_ngram_size=2,         # Prevent repeating n-grams
            temperature=0.5,                # Adjust the randomness
            top_k=150,                       # Limit sampling to top 50 tokens
            top_p=0.75,                     # Use nucleus sampling
            pad_token_id=model.config.eos_token_id  # Set pad token id to eos token id
        )

        # Decode the generated text
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Return the answer as JSON
        return jsonify({'answer': answer})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
