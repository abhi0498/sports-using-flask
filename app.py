from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    uri = db.Column(db.String(200), nullable=False)
    cat = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<URL %r>' % self.id


@app.route('/')
def index():
    new_cat = url.query.all()
    return render_template('index.html', cats=new_cat)


@app.route('/<string:cat>')
def renderCat(cat):
    if cat:
        new_cat = url.query.all()

        return render_template('cat.html', cats=new_cat, cat=cat)
    else:
        return redirect('/')


@app.route('/add', methods=['POST', 'GET'])
def add():
    if(request.method == 'POST'):

        name = request.form['name']
        uri = request.form['url']
        cat = request.form['cat']
        new_url = url(name=name, uri=uri, cat=cat)
        try:
            db.session.add(new_url)
            db.session.commit()
            return redirect("/"+cat)
        except:
            return 'DB error '
    else:
        return render_template('add.html')


if __name__ == "__main__":
    app.run()
