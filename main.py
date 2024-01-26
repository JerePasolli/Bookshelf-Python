from flask import Flask, render_template, request, redirect, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column('book_id', db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, title, author, rating):
        self.title = title
        self.author = author
        self.rating = rating


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    result = db.session.execute(db.select(Books).order_by(Books.title))
    all_books = result.scalars().all()
    print(all_books)
    return render_template('index.html', books=all_books)


@app.route("/add")
def add():
    return render_template('add.html')


@app.route("/add/new_input", methods=['POST'])
def receive_data():
    book_name = request.form['book_name']
    book_author = request.form['book_author']
    rating = request.form['rating']
    new_book = Books(title=book_name, author=book_author, rating=rating)
    db.session.add(new_book)
    db.session.commit()
    return (f"<h1>Book correctly added</h1>"
            f"<p><a href='/'>Go to main page</a></p>")


@app.route("/edit", methods=['GET', 'POST'])
def edit_rating():
    if request.method == 'POST':
        book_id = request.form['id']
        book_to_update = Books.query.get_or_404(book_id)
        book_to_update.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Books.query.get_or_404(book_id)
    return render_template('edit_rating.html', book=book_selected)


if __name__ == "__main__":
    app.run(debug=True)

