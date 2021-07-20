from flask import Flask, send_from_directory
import os
import urllib

S3_BUCKET_URL = "https://s3-us-west-2.amazonaws.com/makersdistillery/"

TEST_URL = "https://s3-us-west-2.amazonaws.com/makersdistillery/1000x/70c39d01b95bd38f265c22eba101de75_371055.jpg"

app = Flask(__name__)

@app.route("/images/<path:path>")
def images(path):
    if os.path.isfile(os.path.join("images", path)):
        return send_from_directory("images", path)
    else:
        return "{} NOT FILE".format(path)

if __name__ == "__main__":
    app.run()