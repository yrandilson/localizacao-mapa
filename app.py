from flask import Flask, request, render_template_string

app = Flask(__name__)

html_page = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Rastrear Localização</title>
  <style>
    body { font-family: Arial; text-align: center; padding: 30px; }
    #status { margin-top: 20px; font-size: 18px; color: #333; }
  </style>
</head>
<body>
  <h2>Obtendo dados do dispositivo...</h2>
  <div id="status">Aguarde, por favor.</div>

  <script>
    function enviarInformacoes(dados) {
      fetch('/localizacao', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
      });
    }

    function pedirLocalizacao() {
      if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const dados = {
              latitude: position.coords.latitude,
              longitude: position.coords.longitude,
              userAgent: navigator.userAgent,
              idioma: navigator.language,
              dataHora: new Date().toString()
            };

            fetch('https://api.ipify.org?format=json')
              .then(res => res.json())
              .then(ip => {
                dados.ip = ip.ip;
                enviarInformacoes(dados);
                document.getElementById('status').innerText = 'Informações enviadas com sucesso!';
              })
              .catch(() => {
                document.getElementById('status').innerText = 'Erro ao obter IP.';
              });
          },
          () => {
            document.getElementById('status').innerText = 'Erro ao obter localização.';
          }
        );
      } else {
        document.getElementById('status').innerText = 'Geolocalização não suportada.';
      }
    }

    window.onload = pedirLocalizacao;
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_page)

@app.route('/localizacao', methods=['POST'])
def receber_localizacao():
    data = request.get_json()
    print("\n📍 Dados recebidos:")
    print(f"Latitude: {data.get('latitude')}")
    print(f"Longitude: {data.get('longitude')}")
    print(f"IP: {data.get('ip')}")
    print(f"Dispositivo: {data.get('userAgent')}")
    print(f"Idioma: {data.get('idioma')}")
    print(f"Data e Hora: {data.get('dataHora')}")
    return 'OK', 200

if __name__ == '__main__':
    import socket
    ip = socket.gethostbyname(socket.gethostname())
    print(f"Acesse no celular: http://{ip}:5000")
    app.run(host='0.0.0.0', port=5000)

