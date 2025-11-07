from flask import Flask, jsonify, request, render_template
import uuid

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Lista de tarefas (nosso "banco de dados" simulado)
tarefas = [
    {"id": 1, "tarefa": "Estudar Flask", "feita": False},
    {"id": 2, "tarefa": "Fazer exercícios de programação", "feita": True},
    {"id": 3, "tarefa": "Aprender sobre APIs RESTful", "feita": False}
]

# Rota principal - página de teste
@app.route('/')
def index():
    return render_template('teste.html')

# Rota alternativa para a página de teste
@app.route('/teste')
def pagina_teste():
    return render_template('teste.html')

# API - GET: Obter todas as tarefas
@app.route('/tarefas', methods=['GET'])
def obter_tarefas():
    return jsonify(tarefas)

# API - POST: Criar nova tarefa
@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    dados = request.get_json()
    if 'tarefa' not in dados:
        return jsonify({"erro": "Campo 'tarefa' é obrigatório"}), 400
    nova_tarefa = {
        "id": len(tarefas) + 1,
        "tarefa": dados['tarefa'],
        "feita": False
    }
    tarefas.append(nova_tarefa)
    return jsonify(nova_tarefa), 201

# API - PUT: Atualizar tarefa existente
@app.route('/tarefas/<int:id>', methods=['PUT'])
def atualizar_tarefa(id):
    tarefa = next((t for t in tarefas if t['id'] == id), None)
    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    dados = request.get_json()
    tarefa['tarefa'] = dados.get('tarefa', tarefa['tarefa'])
    tarefa['feita'] = dados.get('feita', tarefa['feita'])
    return jsonify(tarefa)

# API - DELETE: Remover tarefa
@app.route('/tarefas/<int:id>', methods=['DELETE'])
def deletar_tarefa(id):
    global tarefas
    tarefas = [t for t in tarefas if t['id'] != id]
    return jsonify({"mensagem": "Tarefa deletada com sucesso"})

if __name__ == '__main__':
    app.run(debug=True)