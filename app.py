import sys, json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

import certifi
ca = certifi.where()
# client = MongoClient('mongodb+srv://test:thals@cluster0.kbk9mgh.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
client = MongoClient('mongodb+srv://parkmj4312:Qkrp4918@cluster0.serijac.mongodb.net/?retryWrites=true&w=majority')

db = client.dbsparta

@app.route('/')
def home():
  return render_template('index.html')

@app.route("/diary/save", methods=["POST"])
def diary_save():
    diary_list = list(db.anondiary.find({}))
    numlist = [0]
    for a in diary_list:
        numlist.append(a['num'])
    count = max(numlist) + 1
    name = request.form['name_give']
    comment = request.form['comment_give']
    doc = {
    'num':count,
    'name':name,
    'comment':comment
    }
    db.anondiary.insert_one(doc)
    return jsonify({'msg': '일기 기록 완료!'})

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

# 일기 추가
# @app.route('/content', methods=["POST",'GET'])
# def content_post():
#   if request.method == "POST":
#     title = request.form['title']
#     content = request.form['content']
#     # print(title, content, file=sys.stderr)

#     count = list(db.diary.find({}, {'_id': False}))
#     num = len(count) + 1

#     doc = {
#     'num': num,
#     'title': title,
#     'content': content,
#     }
#     db.diary.insert_one(doc)
#     return jsonify({'msg': '일기 등록 완료!'})
#   else:
#     return render_template('post.html')

@app.route('/create_page')
def createpage():
    return render_template('create.html')

@app.route('/create', methods=["POST"])
def create():
    title = request.form['name']
    content = request.form['comment']
    count = list(db.diary.find({},{'_id':False}))

    if count == []:
        num = 1
        doc = {
            'num':num,
            'title':title,
            'content':content
        }
        db.diary.insert_one(doc)
        return jsonify({'msg': '작성완료'})
    elif title == '' or content == '':
        return jsonify({'msg':'내용을 입력해주세요'})
    else:
        done = count[len(count) - 1]
        num = done['num']
        num = num + 1
        doc = {
            'num':num,
            'title':title,
            'content':content
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
  num = int(param)
  print(num,file=sys.stderr)
  detail_data = db.diary.find_one({'num': num},{'_id':False})
  return jsonify({'data': detail_data})
# diary_modify 페이지
@app.route("/diary/modify_open/<param>")
def modify_open(param):
    # print(param,file=sys.stderr)
    return render_template("diary_modify.html", param=param)

@app.route("/diary/modify_open/<param>", methods=["POST"])
def get_modify(param):
  num = int(param)
  print(num,file=sys.stderr)
  modify_data = db.diary.find_one({'num': num},{'_id':False})
  return jsonify({'data': modify_data})
if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)

@app.route("/diary/modify/<param>")
def diary_modify(param):
    print("@",param,file=sys.stderr)
    return render_template("detail.html", param=param)

@app.route("/diary/modify/<param>", methods=["POST"])
def update_modify(param):
  num = int(param)
  title = request.form['title']
  content = request.form['content']
  print(num,file=sys.stderr)
  db.diary.update_one({'num': num}, {'$set': {'title': title,'content':content}})
  return jsonify({'msg': '수정 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)