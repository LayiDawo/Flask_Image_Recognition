"""Load the trained hand-sign digit model and process images for prediction."""

from keras.models import load_model
from keras.utils import img_to_array
import numpy as np
from PIL import Image

# Load the pretrained Keras model
model = load_model("digit_model.h5")


def preprocess_img(img_path):
    """Prepare an uploaded image for the prediction model.

    Resize the image to 224x224 pixels, normalize pixel values,
    and reshape it into a batch of one RGB-format image.

    Args:
        img_path: Uploaded image file or file-like object.

    Returns:
        A NumPy array with shape (1, 224, 224, 3).
    """
    op_img = Image.open(img_path)
    img_resize = op_img.resize((224, 224))
    img2arr = img_to_array(img_resize) / 255.0
    img_reshape = img2arr.reshape(1, 224, 224, 3)
    return img_reshape


def predict_result(predict):
    """Predict the hand-sign digit using the pretrained Keras model.

    Args:
        predict: Preprocessed image array containing one image.

    Returns:
        The index of the class with the highest prediction score.
    """
    pred = model.predict(predict)
    return np.argmax(pred[0], axis=-1)
