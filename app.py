from flask import Flask, render_template, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = Flask(__name__)

model = GPT2LMHeadModel.from_pretrained("./gpt2_finetuned")
tokenizer = GPT2Tokenizer.from_pretrained("./gpt2_finetuned")
tokenizer.pad_token = tokenizer.eos_token
model.eval()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get("question")
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    inputs = tokenizer(question, return_tensors="pt", padding=True, truncation=True, max_length=150)
    attention_mask = inputs['attention_mask'] if 'attention_mask' in inputs else None

    try:
        outputs = model.generate(
            inputs['input_ids'],
            attention_mask=attention_mask,  # Pass the attention mask for proper token handling
            max_length=150,                 # Maximum length for generated tokens
            num_return_sequences=1,         # Return only one generated sequence
            no_repeat_ngram_size=2,         # Prevent repeating n-grams
            temperature=0.5,                # Adjust the randomness of the output
            top_k=150,                      # Use top-k sampling for diversity
            top_p=0.75,                     # Use nucleus sampling (top-p sampling)
            pad_token_id=model.config.eos_token_id  # Set pad token to eos token id for GPT-2
        )

        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return jsonify({'answer': answer})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
