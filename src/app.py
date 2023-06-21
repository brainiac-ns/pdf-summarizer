import logging
import os

from flask import Flask, render_template, request, send_file
from utils import extract_text, write_list_to_pdf

logging.basicConfig(level=logging.INFO, format="%(message)s")

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload():
    logging.info("AAAAAA")
    if "file" not in request.files:
        return "No file included in the request", 400

    file = request.files["file"]
    logging.info("AAAAAA")
    if file.filename.endswith(".pdf"):
        output_path = os.path.join("uploads", file.filename)
        summarized_path = os.path.join("uploads", "summarized.pdf")

        file.save(output_path)
        extracted_text = extract_text(output_path)
        write_list_to_pdf(extracted_text, summarized_path)

        return send_file(summarized_path, as_attachment=True)

    return "Invalid file format. Only PDF files are supported.", 400


@app.route("/upload.html")
def serve_page():
    return render_template("upload.html")


@app.route("/")
def default():
    logging.info(os.listdir())
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
