# Flask練習用ミニToDoアプリ

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# データベース設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

# モデル
class Todo(db.Model):
    __tablename__ = 'Todo' #省略可、練習のため入れてるの
    id = db.Column(db.Integer, primary_key = True) # 整数型、主キー
    task = db.Column(db.String(200), nullable = False) # 文字列（200字）、空欄NG
    complete = db.Column(db.Boolean, default = False) # 真偽値専用、未完了状態で自動スタート

# トップページ
@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos = todos)

# タスク追加
@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        new_todo = Todo(task = task) # class Todoのtaskカラムに変数taskをいれたオブジェクト
        db.session.add(new_todo) # それをDBに追加するよ
        db.session.commit() # それを確定するよ
    return redirect('/')

# タスク完了切り替え
@app.route('/complete/<int:id>')
def complete(id):
    todo = Todo.query.get(id)
    todo.complete = not todo.complete # True / False を逆に反転させるよ
    db.session.commit()
    return redirect('/')

# タスク削除
@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__': # このファイルが直接実行されたときだけ以下を実行するよ
    with app.app_context(): # 「このブロックの中はこのアプリに属する処理です」とFlaskに伝える宣言
        db.create_all() # モデルクラスに基づいてデータベースのテーブルを作成するよ
    app.run(debug=True) # Flaskの開発用サーバーを起動、コードを編集すると自動でサーバーが再起動
