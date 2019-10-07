import os
import requests
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

backend_host = os.getenv("BACKEND_HOST", "localhost")
backend_port = os.getenv("BACKEND_PORT", 8001)


@app.route('/', methods=['GET', 'POST'])
def index():
    template = "index.html"
    app.logger.info(template)
    if request.method == 'POST':
        componente = request.form.get("componente")
        responsavel = request.form.get("responsavel")
        status = request.form.get("status")
        versao = request.form.get("versao")
        try:
            status_code, response = create_deploy(
                componente, responsavel, status, versao)
            return render_template(template, status_code=status_code, response=response)
        except Exception as e:
            app.logger.error(e)

    return render_template(template)


@app.route('/deploys', methods=['GET'])
def view_deploys():
    template = "view_deploys.html"
    try:
        status_code, response = list_deploys()
        return render_template(template, status_code=status_code, response=response)
    except Exception as e:
        app.logger.error(e)


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"frontend_status": "ok", "backend_status": "{}".format(backend_status())})


def backend_status():
    try:
        url = "http://{}:{}/health".format(backend_host, backend_port)
        app.logger.info(url)
        r = requests.get(url)
        return "ok"
    except Exception as e:
        app.logger.error(e)
        return "nok"


def create_deploy(componente, responsavel, status, versao):
    app.logger.info("Recebido: componente: %s, versao: %s", componente, versao)
    try:
        url = "http://{}:{}/api/deploys".format(backend_host, backend_port)
        json = {"componente": f"{componente}",
                "responsavel": f"{responsavel}", "status": f"{status}", "versao": f"{versao}"}
        app.logger.info("Url {}, Payload {}".format(url, json))

        r = requests.post(url, json=json)
        if r.status_code == 200:
            status_code, response = r.status_code, r.json()
        else:
            status_code, response = r.status_code, None

        app.logger.info("Result code {}, Reponse {}".format(
            status_code, response))
        return status_code, response

    except Exception as e:
        app.logger.error(e)


def list_deploys():
    try:
        url = "http://{}:{}/api/deploys".format(backend_host, backend_port)
        r = requests.get(url)
        if r.status_code == 201:
            status_code, response = r.status_code, r.json()
        else:
            status_code, response = r.status_code, None
        return status_code, response
    except Exception as e:
        app.logger.error(e)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
