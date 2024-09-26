from flask import Flask, send_file, request, Response
from flask_cors import CORS, cross_origin
from dataclasses import asdict
import json
import Parser

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])  # Allow only your React app


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route("/pdf")
def get_pdf():
    Parser.set_pdf("test_pdfs/invoice.pdf")
    return send_file(Parser.get_pdf_file_path())


@app.route("/words")
def get_words():
    return json.dumps([asdict(word) for word in Parser.get_words()])


@app.route("/run_query", methods=["POST"])
def run_query():
    for line in request.json["query"].split("\n"):
        if not line:
            continue
        print(line)
        Parser.query(line)
    response = {}
    for key in Parser.execute(""):
        response[key] = [asdict(word) for word in Parser.execute("")[key]]
    print(response)
    return json.dumps(response)


# main driver function
if __name__ == "__main__":

    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
