from flask import Flask, request, send_from_directory
from PIL import Image
import pathlib
import os
import urllib

S3_BUCKET_URL = "https://s3-us-west-2.amazonaws.com/makersdistillery/"
IMAGES_PATH = pathlib.Path("images")

app = Flask(__name__)

@app.route("/images/<path:image_path>")
def images(image_path):
    file_path = IMAGES_PATH / os.path.dirname(image_path)
    file_name = os.path.basename(image_path)
    local_image_path = file_path / file_name
    _, extension = os.path.splitext(image_path)

    if not os.path.isfile(local_image_path):
        file_path.mkdir(parents=True, exist_ok=True)
        s3_url = S3_BUCKET_URL + image_path
        urllib.request.urlretrieve(s3_url, local_image_path)

    h_arg = request.args.get('h', None)
    w_arg = request.args.get('w', None)
    format_arg = request.args.get('format', None)

    if not (h_arg or w_arg or format_arg):
        return send_from_directory("images", image_path)

    image = Image.open(local_image_path)

    width, height = image.size

    new_height = height
    new_width = width

    if h_arg and not w_arg:
        new_height = int(h_arg)
        scale = new_height / height
        new_width = round(width * scale)
    elif w_arg and not h_arg:
        new_width = int(w_arg)
        scale = new_width / width
        new_height = round(height * scale)
    elif w_arg and h_arg:
        new_width = int(w_arg)
        new_height = int(h_arg)

    resized_image_path = pathlib.Path("resized", local_image_path)
    resized_image_file = "{}-{}{}".format(new_width, new_height, extension)

    if not os.path.isfile(IMAGES_PATH / resized_image_path / resized_image_file):
        (IMAGES_PATH / resized_image_path).mkdir(parents=True, exist_ok=True)
        resized_image = image.resize((new_width, new_height))
        resized_image.save(IMAGES_PATH / resized_image_path / resized_image_file)

    return send_from_directory("images", resized_image_path / resized_image_file)


if __name__ == "__main__":
    app.run()