#app.py
from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import pickle
import sqlite3
import os
import numpy as np

#로컬디렉토리에서 Hashing Vectorizer를 임포트
from vectorizer import vect

app = Flask(__name__)

### 분류기 준비
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