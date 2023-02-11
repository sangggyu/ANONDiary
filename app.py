import sys, json
from flask import Flask, render_template, request, jsonify, url_for, redirect

app = Flask(__name__)

from pymongo import MongoClient

import hashlib
import datetime

import jwt

#유저인증위한 JWT라이브러리
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,get_jwt
#로그아웃 기능구현
from flask_jwt_extended import get_jti

import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:thals@cluster0.kbk9mgh.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
#   isLogin = api_valid()
#   print(isLogin, file=sys.stderr)
#   return render_template('index.html',isLogin=isLogin['result'])
    return render_template('index.html')

# 메인페이지 일기 보여주기
@app.route("/diary", methods=["GET"])
def diary_get():
  list_data = list(db.diary.find({}, {'_id': False}))
  return jsonify({'list': list_data})

# 메인페이지 search 기능
@app.route("/search", methods=['POST'])
def search_get():
  search = request.form['search']
  list_data = list(db.diary.find({"title": {"$regex": search}}, {'_id': False}))
  return render_template('search.html', list=list_data)

# ------- 로그인
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

# 회원가입 API
@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.users.find_one({'id': id_receive})

    if result is not None:
        return jsonify({'result': 'fail', 'msg': '이미 존재하는 ID입니다!'})
    else:
        db.users.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})
        return jsonify({'result': 'success'})

SECRET_KEY = 'SPARTA'

@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # token을 준다.
        return jsonify({'result': 'success', 'token': token})
        # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# @app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userinfo = db.users.find_one({'id': payload['id']}, {'_id': 0})
        # return jsonify({'result': 'success', 'nickname': userinfo['nick']})
        return {'result': 'True', 'nickname': userinfo['nick']}

    except jwt.ExpiredSignatureError:
        # return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
        return False

    except jwt.exceptions.DecodeError:
        # return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})
        return False
#     ---------

@app.route('/create_page')
def createpage():
    return render_template('create.html')

@app.route('/create', methods=["POST"])
def create():
    title = request.form['title']
    content = request.form['comment']
    count = list(db.diary.find({},{'_id':False}))

    if count == []:
        diaryid = 1
        doc = {
            'diaryid':diaryid,
            'title':title,
            'content':content,
            'view': 0,
        }
        db.diary.insert_one(doc)
        return jsonify({'msg': '작성완료'})
    elif title == '' or content == '':
        return jsonify({'msg':'내용을 입력해주세요'})
    else:
        done = count[len(count) - 1]
        diaryid = done['diaryid']
        diaryid = diaryid + 1
        doc = {
            'diaryid':diaryid,
            'title':title,
            'content':content,
            'view': 0,
        }
        db.diary.insert_one(doc)
        return jsonify({'msg':'작성완료'})

# detail 페이지
@app.route("/detail/<param>")
def detail(param):
    # print(param,file=sys.stderr)
    return render_template("detail.html", param=param)

@app.route("/detail/<param>", methods=["POST"])
def get_data(param):
  diaryid = int(param)
  print(diaryid,file=sys.stderr)
  detail_data = db.diary.find_one_and_update({'diaryid': diaryid},{"$inc":{"view":1}},{'_id':False})
  # detail_data = db.diary.find_one({'diaryid': diaryid},{'_id':False})
  return jsonify({'data': detail_data})

# detail > comment
# 댓글 등록
@app.route("/commentsave", methods=["POST"])
def comment_post():
    comment_receive = request.form["comment_give"]
    diaryid = request.form["param_give"]
    count = list(db.comment.find({}, {'_id': False}))
    commentid = len(count) + 1

    doc = {
        'commentid': commentid,
        'diaryid': diaryid,
        'comment': comment_receive,
    }
    db.comment.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

# 댓글 데이터 불러오기
@app.route("/commentshow", methods=["POST"])
def comment_get():
    recive_contentid = request.form['give_contentid']

    comment_list = list(db.comment.find(
        {'diaryid': recive_contentid}, {'_id': False}))
    return jsonify({'commentlist': comment_list})

# 삭제 버튼
@app.route("/comment/delete", methods=["POST"])
def delete_comment():
    deletenum_receive = request.form["deletenum_give"]
    db.comment.delete_one({'commentid': int(deletenum_receive)})
    return jsonify({'msg': '삭제 완료'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)