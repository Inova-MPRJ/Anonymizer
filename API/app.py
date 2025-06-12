from flask import Flask, jsonify, request
from tools.anonimization import anonymize_text
import csv
import io

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index(): # TODO: Fazer rota/função para receber CSV
    data = request.json
    # text = data['text'].lower() # Ativar somente para textos em CAPSLock
    text = data['text']
    print(text)
    anonymized_text = anonymize_text(text)
    return jsonify({"Texto anonimizado": anonymized_text})

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    try:
        # Verificar se um arquivo foi enviado
        if 'file' not in request.files:
            return jsonify({"erro": "Nenhum arquivo foi enviado"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"erro": "Nenhum arquivo selecionado"}), 400
        
        if not file.filename.lower().endswith('.csv'):
            return jsonify({"erro": "Arquivo deve ser um CSV"}), 400
        
        # Ler o CSV de forma estruturada
        file.stream.seek(0)
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)
        
        # Verificar se a coluna "Teor" existe
        if 'Teor' not in csv_reader.fieldnames:
            available_columns = ', '.join(csv_reader.fieldnames) if csv_reader.fieldnames else 'Nenhuma'
            return jsonify({
                "erro": "Coluna 'Teor' não encontrada no CSV",
                "colunas_disponíveis": available_columns
            }), 400
        
        # Extrair textos da coluna "Teor"
        teor_texts = []
        linha_count = 0
        
        for row in csv_reader:
            linha_count += 1
            teor_content = row.get('Teor', '').strip()
            
            if teor_content:  # Só adiciona se tiver conteúdo
                teor_texts.append({
                    'linha': linha_count,
                    'texto_original': teor_content
                })
        
        if not teor_texts:
            return jsonify({"erro": "Nenhum conteúdo encontrado na coluna 'Teor'"}), 400
        
        print(f"Encontrados {len(teor_texts)} registros com conteúdo na coluna 'Teor'")
        
        # Anonimizar cada texto da coluna "Teor"
        textos_anonimizados = []
        
        for item in teor_texts:
            texto_anonimizado = anonymize_text(item['texto_original'].lower())
            textos_anonimizados.append({
                'linha': item['linha'],
                'texto_original': item['texto_original'],
                'texto_anonimizado': texto_anonimizado
            })
        
        # Preparar resposta
        total_chars_original = sum(len(item['texto_original']) for item in textos_anonimizados)
        total_chars_anonimizado = sum(len(item['texto_anonimizado']) for item in textos_anonimizados)
        
        return jsonify({
            "total_registros_processados": len(textos_anonimizados),
            "total_caracteres_original": total_chars_original,
            "total_caracteres_anonimizado": total_chars_anonimizado,
            "resultados": textos_anonimizados
        })
        
    except Exception as e:
        return jsonify({"erro": f"Erro ao processar arquivo: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)