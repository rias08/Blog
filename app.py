from flask import Flask, render_template, request, redirect, url_for, session
import os, json

app = Flask(__name__)
app.secret_key = 'ananya_blog_secret'
POSTS_FILE = 'data/posts.json'

def load_posts():
    if not os.path.exists(POSTS_FILE):
        return []
    with open(POSTS_FILE, 'r') as f:
        return json.load(f)

def save_post(post):
    posts = load_posts()
    posts.insert(0, post)
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f, indent=4)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['name'] == 'Ananya C':
            session['user'] = 'Ananya C'
            return redirect(url_for('write'))
        return render_template('login.html', error=True)
    return render_template('login.html', error=False)

@app.route('/write', methods=['GET', 'POST'])
def write():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        save_post({'title': title, 'content': content})
        return redirect(url_for('blog'))
    return render_template('write.html')

@app.route('/blog')
def blog():
    posts = load_posts()
    return render_template('blog.html', posts=posts)

@app.route('/post/<int:index>')
def post(index):
    posts = load_posts()
    if index >= len(posts):
        return "Post not found", 404
    return render_template('post.html', post=posts[index], index=index)