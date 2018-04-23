from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):

    blog_id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    body = db.Column(db.String(400))
    owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    
    def __init__(self, blog_title, body,owner):
        self.blog_title = blog_title
        self.body = body
        self.owner = owner
################


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(25))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html')



@app.before_request
def require_login():
    allowed_routes = ['home','login', 'signup']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')

@app.route('/logout')
def logout():
    del session['user']
    return redirect('/')











###################
@app.route('/')
def index():


    return redirect('/blog')     

   
@app.route('/blog', methods=['GET'])
def home():
    ###blogz add
    if 'user' not in session:
            users =User.query.all()
            return render_template("index.html",title="All Users",users = users)

    blog_id = request.args.get('blog_id', '')

    if blog_id == '':
        blogs = Blog.query.order_by(Blog.blog_id.desc()).all()
        return render_template('display.html', title="Build a Blog ", 
            blogs=blogs)

    else:
        blog_id = int(blog_id)
        blog = Blog.query.get(blog_id)
        return render_template('single.html', title=blog.blog_title, 
            body=blog.body)
    





@app.route('/newpost', methods=['POST','GET'])
def added_blog():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        body = request.form['body']
       ##blogz add
        owner = User.query.filter_by(username=session['user']).first()


        body_error = ""
        title_error = ""

        if blog_title == "":
            title_error = "Error Enter Title!"
        if body == "":
            body_error = "Error Enter Body"
            return render_template('newpost.html',title="Add a Blog", 
                blog_title = blog_title, body = body, title_error = title_error, 
                body_error = body_error )
            
        else:    
            new_blog = Blog(blog_title,body,owner)
            db.session.add(new_blog)
            db.session.commit()

            return redirect('/blog?blog_id=' + str(new_blog.blog_id))
    else:
        return render_template('newpost.html', title="Add a Blog", 
        blog_title="" , body="" , title_error="" , body_error="")

if __name__ == '__main__':
    app.run()