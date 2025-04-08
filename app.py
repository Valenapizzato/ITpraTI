from flask import Flask, render_template, request, redirect, url_for, session
import os, csv

app = Flask(__name__)
app.secret_key = 'supersecret'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formulario-estagiario', methods=['GET', 'POST'])
def formulario_estagiario():
    if request.method == 'POST':
        dados = request.form.to_dict()
        with open('cadastros_estagiarios.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(dados.keys())
            writer.writerow(dados.values())
        return render_template('confirmacao.html')
    return render_template('formulario_estagiario.html')

@app.route('/formulario-empresa', methods=['GET', 'POST'])
def formulario_empresa():
    if request.method == 'POST':
        dados = request.form.to_dict()
        with open('cadastros_empresas.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(dados.keys())
            writer.writerow(dados.values())
        return render_template('confirmacao_empresa.html')
    return render_template('form_empresa.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['usuario'] == 'admin' and request.form['senha'] == 'admin':
            session['logado'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', erro='Usuário ou senha incorretos.')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logado'):
        return redirect(url_for('login'))

    estagiarios = []
    if os.path.isfile('cadastros_estagiarios.csv'):
        with open('cadastros_estagiarios.csv', newline='', encoding='utf-8') as f:
            estagiarios = list(csv.reader(f))

    empresas = []
    if os.path.isfile('cadastros_empresas.csv'):
        with open('cadastros_empresas.csv', newline='', encoding='utf-8') as f:
            empresas = list(csv.reader(f))

    return render_template('dashboard.html', estagiarios=estagiarios, empresas=empresas)

# 🔐 Novas rotas dos portais:
@app.route('/portal-estudante')
def portal_estudante():
    return render_template('portal_estudante.html')

@app.route('/portal-empresa')
def portal_empresa():
    return render_template('portal_empresa.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

