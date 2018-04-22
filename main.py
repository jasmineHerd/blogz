from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):

    blog_id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    body = db.Column(db.String(400))
    
    def __init__(self, blog_title, body):
        self.blog_title = blog_title
        self.body = body
        
@app.route('/')
def home():
    return redirect('/blog')     

   
@app.route('/blog', methods=['GET'])
def index():

    blog_id = request.args.get('blog_id', '')

    if blog_id == '':
        blogs = Blog.query.order_by(Blog.blog_id.desc()).all()
        return render_template('display.html', title="Build a Blog ", 
            blogs=blogs)

    else:
        blog_id = int(blog_id)
        blog = Blog.query.get(blog_id)
        return render_template('singlePost.html', title=blog.blog_title, 
            body=blog.body)
    





@app.route('/newpost', methods=['POST','GET'])
def added_blog():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        body = request.form['body']


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
            new_blog = Blog(blog_title,body)
            db.session.add(new_blog)
            db.session.commit()

            return redirect('/blog?blog_id=' + str(new_blog.blog_id))
    else:
        return render_template('newpost.html', title="Add a Blog", 
        blog_title="" , body="" , title_error="" , body_error="")

if __name__ == '__main__':
    app.run()