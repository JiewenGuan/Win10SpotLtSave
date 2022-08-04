from flask import Flask, render_template, send_from_directory
from PIL import Image
import glob, os, os.path
from threading import Thread
from time import sleep

app = Flask(__name__)
URL = 'http://127.0.0.1:5000/'
#BROWSER can be set to 'edge', 'chrome', 'firefox'
BROWSER = 'chrome'
USERNAME = os.getlogin()
SAVEPATH = "C:/Users/"+USERNAME+"/OneDrive/background/"
WAITETIME = 1000
if not os.path.exists(SAVEPATH):
    os.makedirs(SAVEPATH)

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
        if not os.path.exists('static'):
            os.mkdir('static')
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
    return render_template('saved.html', name = name, savepath = SAVEPATH, waittime = WAITETIME) 

@app.route("/static/<name>")
def static_file(name):
    return send_from_directory('static', name)

@app.route('/shutdown', methods=['GET'])
def shutdown():
    with os.scandir('static/') as dir:
        for file in dir:
            os.remove(file.path)
    os._exit(0)
 

#webbrowser.open has a bug that opens the link twice
#webbrowser.open('http://127.0.0.1:5000/')
if(BROWSER != 'edge'):
    BROWSER+=" "
else:
    BROWSER="microsoft-edge:"
os.system('powershell.exe start '+BROWSER+URL)

if __name__ == "__main__":
    app.run(debug=True)

