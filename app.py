from flask import Flask, request, jsonify

app = Flask(__name__)

clientes = [
    {
        "id": 1,
        "nome": "murilo",
        "cidade": "Curitiba"
    },
    {
        "id": 2,
        "nome": "carlinhos",
        "cidade": "SP"
    }
]

@app.get("/clientes")
def listar_clientes():
    return jsonify(clientes)

@app.get("/clientes/<int:id>")
def buscar_cliente(id):
    for cliente in clientes:
        if cliente["id"] == id:
            return jsonify(cliente)
        
    return {"erro": "Cliente não encontrado"}, 404

@app.post("/clientes")
def registrar_cliente():

    dados = request.get_json()

    novo = {
        "id": len(clientes) + 1,
        "nome": dados["nome"],
        "cidade": dados["cidade"]
    }

    clientes.append(novo)

    return jsonify(novo), 201

@app.put("/clientes/<int:id>")
def atualizar_cliente(id):

    dados = request.get_json()

    for cliente in clientes:

        if cliente["id"] == id:
            cliente["nome"] == dados["id"]
            cliente["cidade"] == dados["cidade"]

            return jsonify(cliente)
        
    return {"erro": "Cliente não encontrado"}, 404

@app.delete("/clientes/<int:id>")
def remover_cliente(id):

    for cliente in clientes:

        if cliente["id"] == id:
            clientes.remove(cliente)
            return "", 204
        
    return {"erro": "Cliente não encontrado"}, 404

if __name__ == "__main__":
    app.run(debug=True)