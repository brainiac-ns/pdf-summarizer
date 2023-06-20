import os

from flask import Flask, render_template, request, send_file

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload():
    # Check if a file is included in the request
    if "file" not in request.files:
        return "No file included in the request", 400

    file = request.files["file"]

    # Check if the file is a PDF
    if file.filename.endswith(".pdf"):
        # Save the file to a local directory
        file.save(os.path.join("uploads", file.filename))

        # Send the file back for download
        return send_file(os.path.join("uploads", file.filename), as_attachment=True)

    return "Invalid file format. Only PDF files are supported.", 400


@app.route("/upload.html")
def serve_page():
    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
