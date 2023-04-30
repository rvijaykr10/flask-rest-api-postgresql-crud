from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@db:5432/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

@app.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author} for book in books])

@app.route('/books', methods=['POST'])
def create_book():
    title = request.json['title']
    author = request.json['author']
    book = Book(title=title, author=author)
    db.session.add(book)
    db.session.commit()
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author})

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author})

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    title = request.json['title']
    author = request.json['author']
    book.title = title
    book.author = author
    db.session.commit()
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author})

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
