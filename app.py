"""Flask application for hand-sign digit recognition."""

from flask import Flask, render_template, request
from model import preprocess_img, predict_result

# Initialize Flask application
app = Flask(__name__)


@app.route("/")
def main():
    """Display the application's image-upload page."""
    return render_template("index.html")


@app.route("/prediction", methods=["POST"])
def predict_image_file():
    """Process an uploaded image and display the predicted digit."""
    try:
        uploaded_file = request.files["file"]

        img = preprocess_img(uploaded_file.stream)
        pred = predict_result(img)

        return render_template("result.html", predictions=str(pred))

    except (KeyError, ValueError, OSError) as error:
        app.logger.warning("Image processing failed: %s", error)
        return render_template(
            "result.html",
            err="File cannot be processed."
        )


if __name__ == "__main__":
    app.run(port=9000, debug=True)
