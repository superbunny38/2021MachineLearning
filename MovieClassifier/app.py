from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import pickle
import sqlite3
import os
import numpy as np

#로컬디렉토리에서 Hashing Vectorizer를 임포트
from vectorizer import vect

app = Flask(__name__)

####### 분류기 준비
cur_dir = os.path.dirname(__file__)
clf = pickle.load(open(os.path.join(cur_dir, 'pkl_objects', 'classifier.pkl'), 'rb'))#로지스틱 회귀 분류기 복원

db = os.path.join(cur_dir, 'reviews.sqlite')

def classify(document):#예측 확률 반환
    label ={0: 'negative',1:'positive'}
    X = vect.transform([document])
    y = clf.predict(X)[0]
    proba = np.max(clf.predict_proba(X))
    return label[y],proba

def train(document, y):#분류기 업데이트
    X = vect.transform([document])
    clf.partial_fit(X,[y])

def sqlite_entry(path, document,y):#사용자 입력을 SQLite 데이터베이스에 하나의 레코드로 저장
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("INSERT INTO review_db (review, sentiment, date)"
    "VALUES (?,?, DATETIME('now'))",(document,y))
    conn.commit()
    conn.close()

####### 플라스크
class ReviewForm(Form):#Text Area Field 객체 생성
    moviereview = TextAreaField('', [validators.DataRequired(), validators.length(min=15)])#리뷰입력최소길이설정

@app.route('/')
def index():
    form = ReviewForm(request.form)
    return render_template('reviewform.html',form = form)#출력

@app.route('/results',methods = ['POST'])
def results():
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate():
        review = request.form['moviereview']
        y, proba = classify(review)
        return render_template('results.html', content = review, prediction = y, probability = round(proba*100,2))
    return render_template('reviewform.html',form = form)

@app.route('/thanks',methods=['POST'])
def feedback():
    feedback = request.form('feedback_button')
    review = request.form['review']
    prediction = request.form['prediction']
    inv_label = {'negative':0, 'positive':1}
    y = inv_label[prediction]
    if feedback == 'Incorrect':
        y = int(not(y))
    train(review, y)
    sqlite_entry(db,review,y)
    return render_template('thanks.html')#감사하다는 메시지 출력


if __name__=='__main__':
    app.run(debug=True)