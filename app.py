from flask import Flask, render_template, request, send_file
import pandas as pd
import os
from services.analise import processar_dados

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processar', methods=['POST'])
def processar():
    file = request.files['file']

    if not file:
        return "Nenhum arquivo enviado"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        df = pd.read_csv(filepath, sep=';', encoding='latin1')
        resultado = processar_dados(df)

        output_path = os.path.join(UPLOAD_FOLDER, "relatorio.xlsx")
        resultado.to_excel(output_path, index=False)

        tabela_html = resultado.to_html(index=False)

        return render_template('index.html', tabela=tabela_html)

    except Exception as e:
        return f"Erro: {str(e)}"

@app.route('/download')
def download():
    return send_file(os.path.join(UPLOAD_FOLDER, "relatorio.xlsx"), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
