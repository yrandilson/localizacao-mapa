from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return open('index.html').read()  # Serve o HTML que contém o mapa

@app.route('/localizacao', methods=['POST'])
def receber_localizacao():
    data = request.get_json()
    print(f"Localização recebida: Latitude={data['latitude']}, Longitude={data['longitude']}")
    # Aqui você pode processar ou armazenar a localização, se necessário
    return jsonify(status="OK", latitude=data['latitude'], longitude=data['longitude'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
