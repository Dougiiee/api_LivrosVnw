from flask import Flask, request, jsonify  # Aqui estamos importando a classe Flask do módulo flask para criar nossa aplicação

# Criamos uma instância do Flask e armazenamos na variável "app"
# O parâmetro __name__ indica que este arquivo será reconhecido como o principal da aplicação
app = Flask(__name__)

import sqlite3



def initi_db():

    # sqlite3 crie o arquivo database.db e se conect com a variavel conn (connection)
    with sqlite3.connect('database.db') as conn:
        conn.execute('''
                CREATE TABLE IF NOT EXISTS LIVROS(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    image_url TEXT NOT NULL
                    )
    ''')

initi_db()

@app.route('/doar', methods = ['POST'])
def doar():

    dados = request.get_json()

    print(f'AQUI ESTAO OS DADOS RETORNADOS DO CLIENTE {dados}')

    titulo = dados.get('titulo')
    categoria = dados.get('categoria')
    autor = dados.get('autor')
    image_url = dados.get('image_url')

    if not titulo or not categoria or not autor or not image_url:
        return jsonify({'erro':'Todos os campos sao obrigatorios'}), 400


    with sqlite3.connect('database.db') as conn:
        conn.execute(f'''
        INSERT INTO LIVROS (titulo, categoria, autor, image_url)
        VALUES ('{titulo}', '{categoria}', '{autor}', '{image_url}')
        ''')

    conn.commit()

    return jsonify({'mensagem': 'Livro cadastrado com sucesso'}), 201
# Aqui verificamos se o script está sendo executado diretamente e não importado como módulo

@app.route("/livros", methods=["GET"])
def listar_livros():

    with sqlite3.connect("database.db") as conn:
        livros = conn.execute("SELECT * FROM LIVROS").fetchall()


        livros_formatados = []


        for item in livros:
            dicionario_livros = {
                "id":item[0],
                "titulo":item[1],
                "categoria":item[2],
                "autor":item[3],
                "image_url":item[4]

            }

            livros_formatados.append(dicionario_livros)

        return jsonify(livros_formatados)






if __name__ == "__main__":
    # Inicia o servidor Flask no modo de depuração (nesse modo nossa API responde automaticamente a qualquer atualização que fizermos no código)
    app.run(debug=True)