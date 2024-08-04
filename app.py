from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Use um modelo público disponível
model_name = "distilgpt2"
generator = pipeline('text-generation', model=model_name)


@app.route('/generate-description', methods=['POST'])
def generate_description():
    data = request.json
    product_title = data['title']

    # Gerar a descrição do produto
    description = generator(product_title, max_length=50, num_return_sequences=1)[0]['generated_text']

    return jsonify({'description': description})


if __name__ == '__main__':
    app.run(debug=True)
