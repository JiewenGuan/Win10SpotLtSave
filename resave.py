from getpass import getuser
from flask import Flask, render_template
from PIL import Image
import glob, os, os.path, webbrowser
from threading import Thread
from time import sleep
app = Flask(__name__)

USERNAME = getuser()
SAVEPATH = "C:/Users/"+USERNAME+"/OneDrive/background/"

global USERCOUNT
USERCOUNT = 0

def threaded_reset(arg):
    sleep(1)
    global USERCOUNT
    USERCOUNT = 0

@app.route("/")
def main():
    global USERCOUNT
    if(USERCOUNT == 0):
        USERCOUNT+=1
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
        t1 = Thread(target=threaded_reset, args=(10,))
        t1.start()
        return render_template('resave.html', image_list = image_list, DoubleOpen = False)

    return render_template('resave.html', image_list = [], DoubleOpen = True)


@app.route("/save/<name>")
def save(name):
    im=Image.open("./static/"+name)
    path = SAVEPATH+name
    im=im.save(path)
    return name + " saved to " + SAVEPATH 

#webbrowser.open has a bug that opens the link twice
webbrowser.open('http://127.0.0.1:5000/')


if __name__ == "__main__":
    app.run(debug=True)
