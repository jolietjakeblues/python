from flask import Flask, request, jsonify
import requests, time

app = Flask(__name__)

OPENAI_API_URL = 'https://api.openai.com/v1/engines/davinci/completions'
API_KEY = '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'

@app.route('/openai', methods=['POST'])
def openai_request():
    text = request.json.get('text')
    data = {
        'prompt': f'Identificeer de belangrijkste concepten in de volgende tekst: "{text}"',
        'max_tokens': 50
    }

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    
    if response.status_code == 429:
        time.sleep(10)  # Wacht 10 seconden en probeer opnieuw
        response = requests.post(OPENAI_API_URL, headers=headers, json=data)

    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5000)
