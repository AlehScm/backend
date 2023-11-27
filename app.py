from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grupo = db.Column(db.String(50))
    produtos = db.relationship('Produto', backref='menu', lazy=True, cascade="all,delete")

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120))
    preco = db.Column(db.Float)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)

with app.app_context():
    db.create_all()

# ROTAS

@app.route('/menu/', methods=['POST'])
def create_menu():
    data = request.form
    grupo = data['grupoexistente'] if data['grupoexistente'] else data['grupo']
    produtos = request.form.getlist('produto[]')  # Modificado para array
    precos = request.form.getlist('preco[]')  # Modificado para array

    # Tenta recuperar o grupo existente
    menu = Menu.query.filter_by(grupo=grupo).first()

    # Se o grupo não existir, cria um novo
    if menu is None:
        menu = Menu(grupo=grupo)
        db.session.add(menu)

    # Itera sobre os produtos e preços, criando novos produtos e adicionando ao grupo
    for produto, preco in zip(produtos, precos):
        novo_produto = Produto(nome=produto, preco=preco, menu=menu)
        db.session.add(novo_produto)

    db.session.commit()
    return jsonify({'message': 'Cardápio criado com sucesso!'}), 201

@app.route('/menu/<id>', methods=['GET'])
def retrieve_menu(id):
    menu = Menu.query.get(id)
    if menu is None:
        return jsonify({'message': 'Cardápio não encontrado'}), 404
    else:
        produtos = [{'nome': produto.nome, 'preco': produto.preco} for produto in menu.produtos]
        return jsonify({'grupo': menu.grupo, 'produtos': produtos})

@app.route('/menu/<id>', methods=['PUT'])
def update_menu(id):
    data = request.get_json()
    menu = Menu.query.get(id)
    if menu is None:
        return jsonify({'message': 'Cardápio não encontrado'}), 404
    else:
        menu.grupo = data['grupo']
        # Atualiza os produtos existentes ou adiciona novos produtos
        for produto_data in data['produtos']:
            produto = Produto.query.filter_by(nome=produto_data['nome'], menu=menu).first()
            if produto is None:
                produto = Produto(nome=produto_data['nome'], menu=menu)
                db.session.add(produto)
            produto.preco = produto_data['preco']
        db.session.commit()
        return jsonify({'message': 'Cardápio atualizado com sucesso!'})

@app.route('/grupos/', methods=['GET'])
def get_grupos():
    grupos = Menu.query.with_entities(Menu.grupo).distinct()
    return jsonify([grupo[0] for grupo in grupos])

@app.route('/produtos/<grupo>', methods=['GET'])
def get_produtos(grupo):
    menu = Menu.query.filter_by(grupo=grupo).first()
    if menu is None:
        return jsonify({'message': 'Grupo não encontrado'}), 404
    else:
        produtos = [{'nome': produto.nome, 'preco': produto.preco} for produto in menu.produtos]
        return jsonify(produtos)    

@app.route('/grupos/<nome>', methods=['DELETE'])
def delete_grupo(nome):
    grupo = Menu.query.filter(func.lower(Menu.grupo) == func.lower(nome)).first()
    if grupo is None:
        return jsonify({'message': 'Grupo não encontrado'}), 404
    else:
        db.session.delete(grupo)
        db.session.commit()
        return jsonify({'message': 'Grupo excluído com sucesso!'})

@app.route('/produtos/<nome>', methods=['DELETE'])
def delete_produto(nome):
    produto = Produto.query.filter(func.lower(Produto.nome) == func.lower(nome)).first()
    if produto is None:
        return jsonify({'message': 'Produto não encontrado'}), 404
    else:
        db.session.delete(produto)
        db.session.commit()
        return jsonify({'message': 'Produto excluído com sucesso!'})

@app.route('/grupos_produtos/', methods=['GET'])
def get_grupos_produtos():
    grupos = Menu.query.all()
    grupos_produtos = []
    for grupo in grupos:
        produtos = [{'nome': produto.nome, 'preco': produto.preco} for produto in grupo.produtos]
        grupos_produtos.append({'grupo': grupo.grupo, 'produtos': produtos})
    return jsonify(grupos_produtos)


if __name__ == '__main__':
    app.run(debug=True)
