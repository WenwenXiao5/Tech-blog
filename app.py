# ORM (Object Relational Mapping)
# SQLAlchemy is an ORM for python
# Flask-sqlalchemy is a flask extension for SqlAlchemy

from datetime import datetime

import requests
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nicoco:@localhost:5432/techblog'
db = SQLAlchemy(app)

# Create a sqlAlchemy class named BlogPost, which inherent db.Model
class BlogPost(db.Model):
    # The class is called BlogPost, therefore, it will look for a table called BlogPost, unless we change it __tablename__
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    subtitle = db.Column(db.String)
    author = db.Column(db.String)
    content = db.Column(db.String)
    date_posted = db.Column('timestamp', db.DateTime, default=datetime.now())

blog_posts = [BlogPost(id=0, title="How to use", subtitle="Read me", 
    author="Wenwen", date_posted=datetime.now(), content="Click 'Add' button at the top right corner to add new blog post.")]

@app.route('/')
def index():
    posts = BlogPost.query.all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = BlogPost.query.get(post_id)
    return render_template('post.html', post=post)


@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = BlogPost(title=title, subtitle=subtitle, author=author, content=content)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/news')
def news():
    url = ('http://newsapi.org/v2/top-headlines?country=us&apiKey=API_KEY')
    response = requests.get(url)
    data = response.json()
    articles = data ['articles']
    return render_template('news.html', articles=articles)


if __name__ == '__main__':
    app.run(debug=True)