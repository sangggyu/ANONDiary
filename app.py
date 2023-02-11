import sys, json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://limsanggyu:lgo!12qwopqw12@cluster0.kdfqzoq.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/create_page')
def createpage():
    return render_template('create.html')

@app.route('/create', methods=["POST"])
def create():
    name = request.form['name']
    comment = request.form['comment']
    count = list(db.create.find({},{'_id':False}))

    if count == []:
        num = 1
        doc = {
            'num':num,
            'name':name,
            'comment':comment
        }
        db.create.insert_one(doc)
        return jsonify({'msg': '작성완료'})
    elif name == '' or comment == '':
        return jsonify({'msg':'내용을 입력해주세요'})
    else:
        done = count[len(count) - 1]
        num = done['num']
        num = num + 1
        doc = {
            'num':num,
            'name':name,
            'comment':comment
        }
        db.create.insert_one(doc)
        return jsonify({'msg':'작성완료'})


@app.route("/create_list", methods=["GET"])
def book_card_get():
    createlist = list(db.create.find({}, {'_id': False}))
    return jsonify({'creates': createlist})


if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)