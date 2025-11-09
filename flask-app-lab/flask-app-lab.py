# Flask練習用ログイン／ログアウト機能

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'ngalrtfsmjaijlsfbvhuifvewkcbyieghisgogtafvh'

# ログイン管理
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "ログインが必要ですわ✨"

# データベース設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask-app-lab.db'
db = SQLAlchemy(app)

# ユーザーモデル
class User(db.Model, UserMixin):    # UserMixinの継承でFlask-Loginが扱える
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(200), nullable = False, unique=True)
    password = db.Column(db.String(200), nullable = False)

    todos = db.relationship('Todo', backref='user', lazy=True) # UserからTodoへの一対多の関係を定義

    def get_id(self):
        return str(self.user_id)
    
# Todoモデル
class Todo(db.Model):
    __tablename__ = 'todo' #省略可、練習のため入れてるの
    id = db.Column(db.Integer, primary_key = True) # 整数型、主キー
    task = db.Column(db.String(200), nullable = False) # 文字列（200字）、空欄NG
    complete = db.Column(db.Boolean, default = False) # 真偽値専用、未完了状態で自動スタート
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)

# ユーザーをIDから読み出すための関数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ログイン機能
# ログイントップページ
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()    # 同じユーザー名があるか確認

        if user and check_password_hash(user.password, password):
            login_user(user)    # センション管理ではなくFlask-Loginでログインを管理
            return redirect(url_for('menu'))
        else:
            message = "ユーザー名またはパスワードが違いますわ💦"
            return render_template('login.html', message=message, username=username)
    
    username = session.pop('temp_username', '')    # セッションからデータを受け取り、削除
    password = session.pop('temp_password', '')
    message = session.pop('temp_message', '') 

    return render_template('login.html',  username=username, password=password, message=message) 

# 新規登録
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first() 
        if existing_user:
            message = "そのユーザー名はすでに登録されておりますわ💦"
            return render_template('register.html', message=message)
     
        new_user = User(username=username, password=generate_password_hash(password))    # 新しいユーザーを作成してデータベースに保存
        db.session.add(new_user)
        db.session.commit()

        session['temp_username'] = username    # ログインページに戻った後用にセッションに一時保存
        session['temp_password'] = password
        session['temp_message'] = "登録が完了しました💖"

        return redirect(url_for('login'))
    
    return render_template('register.html')    # 最初のアクセス時は登録フォームを表示

# ログイン後のメニュー
@app.route('/menu')
@login_required    # このデコレータで「ログイン必須」になるよ
def menu():
    username = current_user.username    # 現在ログインしているユーザーを取得
    return render_template('menu.html')

# ログアウト処理
@app.route('/logout')
@login_required
def logout():
    logout_user()    # Flask-Loginのログアウト関数
    return redirect(url_for('login'))


# Todo
# Todoトップページ
@app.route('/todo_main')
@login_required    # ログインしてない人はtodoに入れない
def todo_main():
    todos = current_user.todos    # Flask-Loginのcurrent_user使用
    return render_template('todo_main.html', todos = todos)

# タスク追加
@app.route('/todo_add', methods=['POST'])
@login_required
def todo_add():
    task_content = request.form.get('task')
    if task_content and 0 < len(task_content) <= 200:
        new_todo = Todo(task = task_content, user_id=current_user.user_id) 
        db.session.add(new_todo) 
        db.session.commit()
    else:
        pass    #とりあえず無効なタスクは無視で
    return redirect(url_for('todo_main'))

# タスク完了切り替え
@app.route('/todo_complete/<int:id>')
@login_required
def todo_complete(id):
    todo = Todo.query.get(id)

    if not todo:
        return "タスクが見つかりませんわ💦", 404

    if todo.user_id != current_user.user_id:
        return "他の方のタスクは操作できませんわ💢", 403

    todo.complete = not todo.complete 
    db.session.commit()
    return redirect(url_for('todo_main'))

# タスク削除
@app.route('/todo_delete/<int:id>')
@login_required
def todo_delete(id):
    todo = Todo.query.get(id)

    if not todo:
        return "タスクが見つかりませんわ💦", 404

    if todo.user_id != current_user.user_id:
        return "他の方のタスクは操作できませんわ💢", 403

    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo_main'))


# 動作確認用ユーザー一覧　
@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

# 動作確認用ユーザー削除
@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')


if __name__ == '__main__':     # このファイルが直接実行されたときだけ以下を実行するよ
    with app.app_context():    # 「このブロックの中はこのアプリに属する処理です」とFlaskに伝える宣言
        db.create_all()        # モデルクラスに基づいてデータベースのテーブルを作成するよ
    app.run(debug=True)        # Flaskの開発用サーバーを起動、コードを編集すると自動でサーバーが再起動

# http://localhost:5000