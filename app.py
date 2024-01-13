from flask import Flask, render_template,send_from_directory,request
import os
import json 
import socket

app = Flask(__name__)

class ImgStore:

    def __init__(self):
            self.app = app 
            @app.route('/<image_name>')
            def get_image(image_name):
                return send_from_directory(f'./json_{image_name}', f"{image_name}.png")


            @app.route('/')
            def main():
                return render_template("upload.html")


            @app.route('/upload',methods=['POST'])
            def upload():
                print(request.form['path'])
                if not os.path.exists(f'./json_{request.form["path"]}'):
                    os.makedirs(f"./json_{request.form['path']}")
                request.files['image'].save(f"./json_{request.form['path']}/{request.form['path']}.png")
                print('creating img.file....')
                with open(f"./json_{request.form['path']}/img.json",'w') as img:
                    ip = self.get_local_ip() if not self.get_local_ip() is None else "192.168.8.140"
                    print(ip)
                    img.write(json.dump({'link':f'https://{ip}:5005/{request.form["path"]}'}))
                print('Complete!')
                
    def run(self):
        self.app.debug = True 
        self.app.run(host = '0.0.0.0',port=5005)

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('10.255.255.255', 1))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            print(f"Error getting local IP: {e}")
            return None



if __name__ == '__main__':
    img = ImgStore()
    img.run()
