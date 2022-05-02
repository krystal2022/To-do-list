from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.xvovm.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/todolist", methods=["POST"])
def todolist_post():
    todo_receive = request.form['todo_give']
    todo_list = list(db.todolist.find({}, {'_id': False}))
    count = len(todo_list) + 1
    doc = {
        'todolist': todo_receive,
        'num': count,
        'done': 0
    }
    db.todolist.insert_one(doc)
    return jsonify({'msg': '추가 완료!'})

@app.route("/todolist/done", methods=["POST"])
def todolist_done():
    num_receive = request.form['num_give']
    db.todolist.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '할일 완료!'})

@app.route("/todolist/remove", methods=["POST"])
def todolist_remove():
    num_receive = request.form['num_give']
    db.todolist.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제 완료!'})

@app.route("/todolist", methods=["GET"])
def todolist_get():
    all_todo = list(db.todolist.find({}, {'_id': False}))
    return jsonify({'todolist': all_todo})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)