from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Pode ser qualquer sequência segura

# Diretório para salvar uploads
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Simulação de banco de dados em memória
dados_propostas = []

# Tela de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == '1234':
            session['user'] = request.form['username']
            return redirect(url_for('painel'))
        else:
            return render_template('login.html', erro=True)
    return render_template('login.html', erro=False)

# Painel principal
@app.route('/painel', methods=['GET', 'POST'])
def painel():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        arquivo = request.files['arquivo']
        data_faturamento = request.form['data_faturamento']
        nome_arquivo = secure_filename(arquivo.filename)
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
        arquivo.save(caminho)

        dados = {
            'cliente': request.form['cliente'],
            'vendedor': request.form['vendedor'],
            'carro': request.form['carro'],
            'ipva_tipo': request.form['ipva_tipo'],
            'ipva_valor': request.form['ipva_valor'],
            'emplacamento_tipo': request.form['emplacamento_tipo'],
            'emplacamento_valor': request.form['emplacamento_valor'],
            'data_faturamento': data_faturamento,
            'arquivo': nome_arquivo
        }
        dados_propostas.append(dados)

        return redirect(url_for('painel'))

    return render_template('painel.html', propostas=dados_propostas)

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
