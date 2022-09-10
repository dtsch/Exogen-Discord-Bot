from flask import Flask
from threading import Thread
from waitress import serve

# code to keep got awake when being web-hosted on Repl.it
app = Flask('')


@app.route('/')
def main():
    return "Your Bot Is Ready"


def run():
    # app.run(host="0.0.0.0", port=8080)
    serve(app, host="0.0.0.0", port=8080)


def keep_alive():
    server = Thread(target=run)
    server.start()
