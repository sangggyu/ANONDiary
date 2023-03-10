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
# client = MongoClient('mongodb+srv://parkmj4312:Qkrp4918@cluster0.serijac.mongodb.net/?retryWrites=true&w=majority')

db = client.dbsparta

@app.route('/')
def home():
  isLogin = api_valid()
  if isLogin['result']:
    return render_template('index.html',isLogin=isLogin)
  else:
    return render_template('index.html',isLogin=isLogin)

# @app.route("/diary/save", methods=["POST"])
# def diary_save():
#     diary_list = list(db.anondiary.find({}))
#     numlist = [0]
#     for a in diary_list:
#         numlist.append(a['num'])
#     count = max(numlist) + 1
#     name = request.form['name_give']
#     comment = request.form['comment_give']
#     doc = {
#     'num':count,
#     'name':name,
#     'comment':comment
#     }
#     db.anondiary.insert_one(doc)
#     return jsonify({'msg': '일기 기록 완료!'})

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
        return {'result': True, 'nickname': userinfo['nick']}

    except jwt.ExpiredSignatureError:
        # return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
        return {'result': False}

    except jwt.exceptions.DecodeError:
        # return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})
        return {'result': False}

#     ---------

@app.route('/create_page')
def createpage():
    isLogin = api_valid()
    if isLogin['result']:
        return render_template('create.html', isLogin=isLogin['nickname'])
    else:
        return render_template('login.html')

@app.route('/create', methods=["POST"])
def create():
    title = request.form['title']
    content = request.form['comment']
    nick = request.form['nick']
    count = list(db.diary.find({},{'_id':False}))
    create_time = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    
    if count == []:
        diaryid = 1
        doc = {
            'diaryid':diaryid,
            'nick': nick,
            'title':title,
            'content':content,
            'createtime':create_time,
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
            'nick': nick,
            'title':title,
            'content':content,
            'createtime':create_time,
            'view': 0,
        }
        db.diary.insert_one(doc)
        return jsonify({'msg':'작성완료'})

# detail 페이지
@app.route("/detail/<param>")
def detail(param):
    isLogin = api_valid()
    if isLogin['result']:
        return render_template('detail.html', isLogin=isLogin['nickname'],param=param)
    else:
        return render_template('detail.html', param=param)
    # print(param,file=sys.stderr)

@app.route("/detail/<param>", methods=["POST"])
def get_data(param):
  diaryid = int(param)
#   print(diaryid,file=sys.stderr)
  detail_data = db.diary.find_one_and_update({'diaryid': diaryid},{"$inc":{"view":1}},{'_id':False})
  # detail_data = db.diary.find_one({'diaryid': diaryid},{'_id':False})
  return jsonify({'data': detail_data})

# # diary_modify 페이지
# @app.route("/diary/modify_open/<param>")
# def modify_open(param):
#     # print(param,file=sys.stderr)
#     return render_template("diary_modify.html", param=param)

# @app.route("/diary/modify_open/<param>", methods=["POST"])
# def get_modify(param):
#   num = int(param)
#   print(num,file=sys.stderr)
#   modify_data = db.diary.find_one({'num': num},{'_id':False})
#   return jsonify({'data': modify_data})
# if __name__ == '__main__':
#     app.run('0.0.0.0', port=4000, debug=True)

# @app.route("/diary/modify/<param>")
# def diary_modify(param):
#     print("@",param,file=sys.stderr)
#     return render_template("detail.html", param=param)

# @app.route("/diary/modify/<param>", methods=["POST"])
# def update_modify(param):
#   num = int(param)
#   title = request.form['title']
#   content = request.form['content']
#   print(num,file=sys.stderr)
#   db.diary.update_one({'num': num}, {'$set': {'title': title,'content':content}})
#   return jsonify({'msg': '수정 완료!'})

# detail > comment
# 댓글 등록
@app.route("/commentsave", methods=["POST"])
def comment_post():
    nick = request.form['nick']
    comment_receive = request.form["comment_give"]
    diaryid = request.form["param_give"]
    count = list(db.comment.find({}, {'_id': False}))
    commentid = len(count) + 1

    doc = {
        'commentid': commentid,
        'nick': nick,
        'diaryid': diaryid,
        'comment': comment_receive,
    }
    db.comment.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

# 댓글 데이터 불러오기
@app.route("/commentshow", methods=["POST"])
def comment_get():
    recive_contentid = request.form['give_contentid']
    print("@",recive_contentid ,file=sys.stderr)
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