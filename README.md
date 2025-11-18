# Flask Learning Projects  
Flask を学ぶための練習プロジェクトをまとめたリポジトリです。  
基礎的な機能の実装や、Webアプリの構造を理解するための練習が中心です。

---

## 🎯 このリポジトリの目的  
- Flask の基本的な使い方を理解する  
- Webアプリの作り方を段階的に学ぶ  
- 学習記録としてまとめ、後から見返せるようにする  

---

🔧 使用技術
Python
Flask
HTML / CSS
Jinja2

---

## 📁 プロジェクト一覧  

### 1. `flask-todo-lab`
- Todoアプリの練習
- ルーティング・テンプレートの基本など
- Flaskの最小構成を理解するための練習
- SQLの基本 
- CRUD処理（一覧・追加・更新・削除）の基礎を学習

### 2. `flask-login-lab`
- ログイン機能の練習 （認証・セッション管理の基礎）
- ユーザー登録（email / username / password）
- ログイン・ログアウト
- パスワードのハッシュ化（例：werkzeug.security）
- 保護されたページ（ログイン必須のルート）
- 「ログインしたまま」オプションやセッション管理

### 3. `flask-app-lab`
- 1と2を統合
- 認証付きの Todo アプリを作り、ユーザーごとにデータを分ける

---

## 🧪 使い方（ローカル実行）  
```bash
git clone https://github.com/bota-rabbit/Made-for-beginners-to-practice.git
python -m venv venv
pip install -r requirements.txt
flask run

