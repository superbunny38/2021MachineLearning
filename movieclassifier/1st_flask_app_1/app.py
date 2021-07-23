#플라스크 웹 애플리케이션을 구동하기 위해 파이썬 인터프리터로 실행할 핵심 코드를 담음
from flask import Flask, render_template

app = Flask(__name__)#새로운 인스턴스 초기화
@app.route('/')#라우트 데코레이터: 특정 URLd이 index 함수를 실행하도록 지정
def index():
    return render_template('first_app.html')

if __name__ == '__main__':#현재 디렉터리와 같은 위치에서 HTML 템플릿 폴더 찾음 ("__main__")
    app.run(debug = True)#애플리케이션 시작
