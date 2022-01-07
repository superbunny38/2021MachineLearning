from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
from update import update_model


app = Flask(__name__)

class HelloForm(Form):
    sayhello = TextAreaField('',[validators.DataRequired()])

@app.route('/')

def index():
    form = HelloForm(request.form)
    return render_template('first_app.html',form = form)

@app.route('/hello',methods = ['POST'])

def hello():
    form = HelloForm(request.form)
    if request.method == 'POST' and form.validate():#내용 검증후
        name = request.form['sayhello']
        return render_template('hello.html',name=name)
    return render_template('first_app.html',form=form)

if __name__ == '__main__':
    ckf = update_model(db_path = db, model = clf, batch_size = 10000)
    app.run(debug = True)#플라스크 디버거 활성화

    
