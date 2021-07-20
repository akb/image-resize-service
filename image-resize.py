from flask import Flask, send_from_directory
import pathlib
import os
import urllib

S3_BUCKET_URL = "https://s3-us-west-2.amazonaws.com/makersdistillery/"
IMAGES_PATH = pathlib.Path("images")

app = Flask(__name__)

@app.route("/images/<path:image_path>")
def images(image_path):
    if not os.path.isfile(os.path.join("images", image_path)):
        print("not cached, saving to cache and then sending")
        file_path = IMAGES_PATH.joinpath(*image_path.split("/")[0:-1])
        file_name = os.path.basename(image_path)
        file_path.mkdir(parents=True, exist_ok=True)

        s3_url = S3_BUCKET_URL + image_path

        urllib.request.urlretrieve(s3_url, file_path / file_name)

    return send_from_directory("images", image_path)

if __name__ == "__main__":
    app.run()