from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Função para carregar descrições de arquivos .txt
def load_descriptions(directory):
    descriptions = []
    import os
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                descriptions.append(file.read())
    return descriptions

# Carregar descrições
directory = 'descriptions'  # Diretório onde os arquivos .txt estão localizados
descriptions = load_descriptions(directory)

# Carregar o modelo de IA
model_name = "gpt-3"
generator = pipeline('text-generation', model=model_name)

def generate_description(title):
    prompt = f"Descreva o produto com o título: {title}. Baseado nas seguintes descrições: {descriptions}"
    generated_texts = generator(prompt, max_length=100, num_return_sequences=1)
    return generated_texts[0]['generated_text']

@app.route('/descricao', methods=['POST'])
def descricao():
    data = request.json
    title = data.get('title', '')
    if not title:
        return jsonify({"error": "Title is required"}), 400
    description = generate_description(title)
    return jsonify({"title": title, "description": description})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
