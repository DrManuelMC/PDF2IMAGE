from flask import Flask
from flask_restful import  Api


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
# observer = Observer()


api = Api(app)

from pdf_2_tiff import Pdf2Tiff
# observer.schedule(MyHandler(), path='input/', recursive=False)
# observer.start()
api.add_resource(Pdf2Tiff, '/convertir')

@app.route('/')
def home():
    return 'Hello World!'

if __name__ == '__main__':


    
    app.run(debug=True, port=5003)