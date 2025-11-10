from flask import Flask, jsonify, request

app = Flask(__name__)

# "Base de datos" en memoria (para la tarea).
# En producción, aquí iría MongoDB, KeyDB, etc.
books = []
next_id = 1


def find_book(book_id: int):
    return next((b for b in books if b["id"] == book_id), None)


@app.route("/books", methods=["GET"])
def get_books():
    """
    GET /books → Obtener la lista de libros
    """
    return jsonify(books), 200


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    """
    GET /books/<id> → Obtener un libro específico
    """
    book = find_book(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book), 200


@app.route("/books", methods=["POST"])
def create_book():
    """
    POST /books → Agregar un nuevo libro
    Espera un JSON como:
    {
      "title": "Nombre",
      "author": "Autor",
      "year": 2024,
      "read": false
    }
    """
    global next_id

    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    data = request.get_json()

    title = data.get("title")
    author = data.get("author")
    year = data.get("year")
    read = data.get("read", False)

    if not title or not author:
        return jsonify({"error": "Fields 'title' and 'author' are required"}), 400

    new_book = {
        "id": next_id,
        "title": title,
        "author": author,
        "year": year,
        "read": bool(read),
    }
    next_id += 1
    books.append(new_book)

    return jsonify(new_book), 201


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    """
    PUT /books/<id> → Actualizar un libro
    Permite actualizar uno o varios campos.
    """
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    book = find_book(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()

    for field in ("title", "author", "year", "read"):
        if field in data:
            book[field] = data[field]

    return jsonify(book), 200


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    """
    DELETE /books/<id> → Eliminar un libro
    """
    book = find_book(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404

    books.remove(book)
    return jsonify({"message": "Book deleted"}), 200


if __name__ == "__main__":
    # En producción usarías: gunicorn -w 4 -b 0.0.0.0:5001 app:app
    app.run(debug=True, port=5001)
