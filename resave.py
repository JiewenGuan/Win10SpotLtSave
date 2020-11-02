USERNAME = "heiye"
SAVEPATH = "C:/Users/heiye/OneDrive/background/"


from flask import Flask, render_template
from PIL import Image
import glob, os, os.path
app = Flask(__name__)

@app.route("/")
def main():
    filelist = glob.glob(os.path.join("/static/", "*.jpg"))
    for f in filelist:
        os.remove(f)
    image_list = []
    for filename in glob.glob('C:/Users/'+USERNAME+'/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets/*'): 
        im=Image.open(filename)
        if(im.width == 1920):
            name = im.filename.split("Assets\\")[1]+".jpg"
            im=im.save("./static/"+name)
            #im.show()
            image_list.append("/static/"+name)

    return render_template('resave.html', image_list = image_list)

@app.route("/save/<name>")
def save(name):
    im=Image.open("./static/"+name)
    path = SAVEPATH+name
    im=im.save(path)
    return name + " saved to " + SAVEPATH 

if __name__ == "__main__":
    app.run(debug=True)