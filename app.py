#import require python classes and packages

from flask import *
from auth_utils import *
from werkzeug.utils import secure_filename
import os,random
import numpy as np
import pandas as pd
import joblib


random_seed = 42
random.seed(random_seed)
np.random.seed(random_seed)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt','csv'}
MAX_UPLOAD_SIZE_MB = 512  # Maximum upload size in megabytes

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_SIZE_MB * 1024 * 1024  # Set max content length

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route("/signup")
def signup_route():
    return signup()


@app.route("/signin")
def signin_route():
    return signin()

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/heart')
def heart():
	return render_template('heart_predict.html')

@app.route('/diabetes')
def diabetes():
	return render_template('diabetes_predict.html')


@app.route('/parkinson')
def parkinson():
	return render_template('parkinsons_predict.html')


@app.route('/heart_notebook')
def heart_notebook():
	return render_template('heart_test.html')

@app.route('/parkinson_notebook')
def parkinson_notebook():
	return render_template('parkinson_test.html')

@app.route('/diabetes_notebook')
def diabetes_notebook():
	return render_template('diabetes_test.html')

@app.route('/predict',methods=['POST'])
def predict():
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    model = joblib.load('model/heart_model.sav')
    predict = model.predict(final4)
    if predict == 0:
        output = "NO Heart"
        alert_class = "alert-success text-success"  # Green color for positive result
        icon = "fas fa-smile-beam text-success"  # Happy icon
        text_color = "green"
    elif predict == 1:
        output = "Heart"
        alert_class = "alert-danger text-danger"  # Red color for warning
        icon = "fas fa-exclamation-triangle text-danger"  # Warning icon
        text_color = "red"
    
    

    return render_template('prediction.html', output=output,alert_class=alert_class,icon=icon,text_color=text_color)

@app.route('/predict2',methods=['POST'])
def predict2():
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    model = joblib.load('model/diabetes.sav')
    predict = model.predict(final4)

    if predict == 0:
        output = "No Diabetes"
        alert_class = "alert-success text-success"  # Green color for positive result
        icon = "fas fa-smile-beam text-success"  # Happy icon
        text_color = "green"
    elif predict == 1:
        output = "Diabetes"
        alert_class = "alert-danger text-danger"  # Red color for warning
        icon = "fas fa-exclamation-triangle text-danger"  # Warning icon
        text_color = "red"
    
    
    
    return render_template('prediction.html', output=output, alert_class=alert_class, icon=icon,text_color=text_color)


@app.route('/predict3',methods=['POST'])
def predict3():
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    model = joblib.load('model/parkinson.sav')
    predict = model.predict(final4)

    if predict == 0:
        output = "NO Parkinson"
        alert_class = "alert-success text-success"  # Green color for positive result
        icon = "fas fa-smile-beam text-success"  # Happy icon
        text_color = "green"
    elif predict == 1:
        output = "Parkinson"
        alert_class = "alert-danger text-danger"  # Red color for warning
        icon = "fas fa-exclamation-triangle text-danger"  # Warning icon
        text_color = "red"
    
    
    return render_template('prediction.html', output=output, alert_class=alert_class, icon=icon,text_color=text_color)


if __name__ == '__main__':
    app.run(debug=True)