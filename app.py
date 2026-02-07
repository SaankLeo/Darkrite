import os
import subprocess
from flask import Flask, request, send_file, render_template

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# CHANGE if your Ghostscript path is different
GS_PATH = "gs"


@app.route("/", methods=["GET", "POST"])
def upload_pdf():
    if request.method == "POST":
        file = request.files["pdf"]

        if not file or not file.filename.endswith(".pdf"):
            return "Please upload a valid PDF."

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(OUTPUT_FOLDER, "dark_" + file.filename)

        file.save(input_path)

        # Soft dark, low contrast, images preserved
        command = [
            GS_PATH,
            "-o", output_path,
            "-sDEVICE=pdfwrite",
            "-dPDFSETTINGS=/ebook",
            "-c", "{0.75 mul 1 exch sub} settransfer",
            "-f", input_path
        ]

        subprocess.run(command, check=True)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
