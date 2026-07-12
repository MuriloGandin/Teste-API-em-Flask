from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect(
    "clientes.db",
    check_same_thread=False
)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()


@app.get("/clientes")
def listar_clientes():

    clientes = cursor.execute("""
        SELECT * FROM clientes
    """).fetchall()

    return jsonify([dict(cliente) for cliente in clientes])


@app.get("/clientes/<int:id>")
def buscar_cliente(id):

    cliente = cursor.execute("""
        SELECT *
        FROM clientes
        WHERE id = ?
    """, (id,)).fetchone()

    if cliente is None:
        return {"erro": "Cliente não encontrado"}, 404

    return jsonify(dict(cliente))


@app.post("/clientes")
def registrar_cliente():

    dados = request.get_json()

    cursor.execute("""
        INSERT INTO clientes (nome, cidade)
        VALUES (?, ?)
    """, (dados["nome"], dados["cidade"]))

    conn.commit()

    novo = cursor.execute("""
        SELECT *
        FROM clientes
        WHERE id = last_insert_rowid()
    """).fetchone()

    return jsonify(dict(novo)), 201


@app.put("/clientes/<int:id>")
def atualizar_cliente(id):

    dados = request.get_json()

    cursor.execute("""
        UPDATE clientes
        SET nome = ?, cidade = ?
        WHERE id = ?
    """, (dados["nome"], dados["cidade"], id))

    conn.commit()

    if cursor.rowcount == 0:
        return {"erro": "Cliente não encontrado"}, 404

    cliente = cursor.execute("""
        SELECT *
        FROM clientes
        WHERE id = ?
    """, (id,)).fetchone()

    return jsonify(dict(cliente))


@app.delete("/clientes/<int:id>")
def remover_cliente(id):

    cursor.execute("""
        DELETE FROM clientes
        WHERE id = ?
    """, (id,))

    conn.commit()

    if cursor.rowcount == 0:
        return {"erro": "Cliente não encontrado"}, 404

    return "", 204


if __name__ == "__main__":
    app.run(debug=True)