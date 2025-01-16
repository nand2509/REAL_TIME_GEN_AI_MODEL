# from flask import Flask, render_template, request, jsonify
# import google.generativeai as genai
#
# # Configure the generative AI model
# genai.configure(api_key="AIzaSyBH9pjDICFfC4RqNF2luI86P1LVlLyCF78")
# model = genai.GenerativeModel("gemini-1.5-flash")
#
# app = Flask(__name__)
#
# # Store prompts and responses in memory for demonstration purposes
# saved_prompts = []
#
# def format_response(raw_response):
#     """
#     Format the raw response into a clear, point-wise format with each point on a new line.
#     """
#     sentences = raw_response.split(". ")
#     points = [f"{i + 1}. {sentence.strip()}." for i, sentence in enumerate(sentences) if sentence.strip()]
#     return "\n".join(points)
#
# @app.route("/")
# def index():
#     return render_template("index.html", prompts=saved_prompts)
#
# @app.route("/generate", methods=["POST"])
# def generate():
#     try:
#         user_prompt = request.json.get("prompt")
#         if not user_prompt:
#             return jsonify({"error": "Prompt is required"}), 400
#
#         response = model.generate_content(user_prompt)
#         formatted_response = format_response(response.text)
#
#         # Save the prompt and response
#         saved_prompts.append({"prompt": user_prompt, "response": formatted_response})
#         return jsonify({"response": formatted_response})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#
# @app.route("/delete_prompt", methods=["POST"])
# def delete_prompt():
#     try:
#         prompt_index = request.json.get("index")
#         if prompt_index is not None and 0 <= prompt_index < len(saved_prompts):
#             del saved_prompts[prompt_index]
#             return jsonify({"message": "Prompt deleted successfully"})
#         return jsonify({"error": "Invalid prompt index"}), 400
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#
# @app.route("/edit_prompt", methods=["POST"])
# def edit_prompt():
#     try:
#         prompt_index = request.json.get("index")
#         new_prompt = request.json.get("new_prompt")
#
#         if prompt_index is not None and 0 <= prompt_index < len(saved_prompts) and new_prompt:
#             response = model.generate_content(new_prompt)
#             formatted_response = format_response(response.text)
#
#             saved_prompts[prompt_index] = {"prompt": new_prompt, "response": formatted_response}
#             return jsonify({"response": formatted_response})
#         return jsonify({"error": "Invalid input"}), 400
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#
# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image

# Configure the generative AI model
genai.configure(api_key="AIzaSyBH9pjDICFfC4RqNF2luI86P1LVlLyCF78")
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"txt", "png", "jpg", "jpeg"}

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])


def allowed_file(filename):
    """Check if the uploaded file is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


def extract_text_from_file(filepath):
    """Extract text from a file."""
    if filepath.lower().endswith(".txt"):
        with open(filepath, "r") as file:
            return file.read()
    elif filepath.lower().endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(filepath)
        return pytesseract.image_to_string(image)
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle file upload."""
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Extract text from the uploaded file
        extracted_text = extract_text_from_file(filepath)
        if extracted_text:
            return jsonify({"text": extracted_text})
        return jsonify({"error": "Failed to extract text from the file"}), 400
    return jsonify({"error": "Invalid file type"}), 400


@app.route("/generate", methods=["POST"])
def generate():
    try:
        user_prompt = request.json.get("prompt")
        if not user_prompt:
            return jsonify({"error": "Prompt is required"}), 400

        response = model.generate_content(user_prompt)
        formatted_response = "\n".join(
            [f"{i + 1}. {line.strip()}." for i, line in enumerate(response.text.split(". ")) if line.strip()]
        )
        return jsonify({"response": formatted_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

