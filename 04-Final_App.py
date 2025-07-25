from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import NumberRange

import numpy as np  
from tensorflow.keras.models import load_model
import joblib



from tensorflow.keras.models import load_model
import joblib


flower_model = load_model("final_iris_model.keras")
flower_scaler = joblib.load("iris_scaler.pkl")


def return_prediction(model,scaler,sample_json):
    
    # For larger data features, you should probably write a for loop
    # That builds out this array for you
    
    s_len = sample_json['sepal_length']
    s_wid = sample_json['sepal_width']
    p_len = sample_json['petal_length']
    p_wid = sample_json['petal_width']
    
    flower = [[s_len,s_wid,p_len,p_wid]]
    
    flower = scaler.transform(flower)
    
    classes = np.array(['setosa', 'versicolor', 'virginica'])
    
    class_ind = np.argmax(model.predict(flower), axis=1)
    return classes[class_ind[0]]



app = Flask(__name__)
# Configure a secret SECRET_KEY
# We will later learn much better ways to do this!!
app.config['SECRET_KEY'] = 'mysecretkey'


# REMEMBER TO LOAD THE MODEL AND THE SCALER!
flower_model = load_model("final_iris_model.keras")
flower_scaler = joblib.load("iris_scaler.pkl")


# Now create a WTForm Class
# Lots of fields available:
# http://wtforms.readthedocs.io/en/stable/fields.html
class FlowerForm(FlaskForm):
    sep_len = StringField('Sepal Length')
    sep_wid = StringField('Sepal Width')
    pet_len = StringField('Petal Length')
    pet_wid = StringField('Petal Width')

    submit = SubmitField('Analyze')



@app.route('/', methods=['GET', 'POST'])
def index():

    # Create instance of the form.
    form = FlowerForm()
    # If the form is valid on submission (we'll talk about validation next)
    if form.validate_on_submit():
        # Grab the data from the breed on the form.

        session['sep_len'] = form.sep_len.data
        session['sep_wid'] = form.sep_wid.data
        session['pet_len'] = form.pet_len.data
        session['pet_wid'] = form.pet_wid.data

        return redirect(url_for("prediction"))


    return render_template('home.html', form=form)


@app.route('/prediction')
def prediction():

    content = {}

    content['sepal_length'] = float(session['sep_len'])
    content['sepal_width'] = float(session['sep_wid'])
    content['petal_length'] = float(session['pet_len'])
    content['petal_width'] = float(session['pet_wid'])

    results = return_prediction(model=flower_model,scaler=flower_scaler,sample_json=content)

    return render_template('prediction.html',results=results)


if __name__ == '__main__':
    app.run(debug=True)