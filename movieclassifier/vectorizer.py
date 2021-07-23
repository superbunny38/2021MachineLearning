#vectorizer.py 내용
from sklearn.feature_extraction.text import HashingVectorizer
import re
import os
import pickle

cur_dir = os.path.dirname(__file__)
stop = pickle.load(open(
    os.path.join(cur_dir,
                'pkl_objects',
                'stopwords.pkl'),'rb'
))


def tokenizer(text):
    #텍스트 정제->불용어 제거-> 토큰으로 분리
    text = re.sub('<[^>]*>','',text)#정규표현식 사용
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)',text)
    text = (re.sub('[\W]+',' ',text.lower()) +#단어가 아닌 문자 모두 제거
            ''.join(emoticons).replace('-',''))#소문자로 바꿈, 이모티콘 변수를 처리 완료된 문자열 끝에 추가
    tokenized = [w for w in text.split() if w not in stop]
    return tokenized

vect = HashingVectorizer(decode_error = 'ignore',
                        n_features = 2**21,
                        preprocessor = None,
                        tokenizer=tokenizer
                        )