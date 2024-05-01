from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Article(db.Model):
    firstName = db.Column(db.String, nullable=False)
    hours = db.Column(db.Integer, default=0)
    date = db.Column(db.Text, default=datetime.utcnow)
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    def __repr__(self):
        return '<Article %r>' % self.id
        

@app.route('/')
def main():
    global total_steps
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('main.html', articles=articles)


@app.route('/form', methods=['POST', 'GET'])
def form():
    if request.method == 'POST':
        firstName = request.form['firstName']
        date = request.form['date']
        hours = request.form['hours']
        article = Article(firstName=firstName, date=date, hours=hours)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error'
    else:
        return render_template('form.html')


@app.route('/del_all')
def form_delete_all():
    articles = Article.query.all()
    try:
        for el in articles:
            db.session.delete(el)
            db.session.commit()
        return redirect('/') 
    except:
        return 'Error'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)