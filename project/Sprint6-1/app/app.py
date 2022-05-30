from flask import Flask, render_template
import os
import random

# instantiate the Flask app
app = Flask(__name__)

# list of cat images
images = [
    "https://cdn.pixabay.com/photo/2014/11/30/14/11/cat-551554_960_720.jpg",
    "https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083492_960_720.jpg",
    "https://cdn.pixabay.com/photo/2015/04/23/21/59/tree-736877_960_720.jpg",
    "https://cdn.pixabay.com/photo/2015/11/16/14/43/cat-1045782_960_720.jpg",
    "https://cdn.pixabay.com/photo/2021/10/19/10/56/cat-6723256_960_720.jpg",
    "https://cdn.pixabay.com/photo/2016/01/20/13/05/cat-1151519_960_720.jpg",
    "https://cdn.pixabay.com/photo/2018/02/21/05/17/cat-3169476_960_720.jpg",
    "https://cdn.pixabay.com/photo/2018/01/28/12/37/cat-3113513_960_720.jpg",
    "https://cdn.pixabay.com/photo/2018/03/27/17/25/cat-3266673_960_720.jpg",
    "https://media.istockphoto.com/photos/sad-looking-kitten-trying-to-climb-over-a-wire-fence-picture-id157398449?s=612x612"
    ]
    
@app.route("/")
def index():
    # return "Finally Hello"
    # url = random.choice(images)
    # return render_template("index.html", url=url)
    return render_template("index.html")
    
@app.route("/pic")
def pic():
    url = random.choice(images)
    return render_template("pic.html", url=url)
    
@app.route('/app')
def blog():
    return "Hello, from App!"
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8801)))
