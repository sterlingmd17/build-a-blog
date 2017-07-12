from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 

# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key= "derp"

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route("/newpost", methods=['POST', 'GET'])
def newpost():
    if request.method=='POST':
        title = request.form['title']
        body = request.form['body']
        if len(title) and len(body) > 0:
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/')
        else:
            error0=''
            error1=''
            if len(title)==0:
                error0="please enter a title"
            if len(body)==0:
                error1="please enter a body"
            return render_template('newpost.html', title=title, body=body, error0=error0, error1=error1)
            

    return render_template('newpost.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    posts = Blog.query.all()
    return render_template("blog.html", posts=posts)

if __name__ == '__main__':
    app.run()