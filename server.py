from flask import Flask, jsonify, send_from_directory, abort, request, Response
from pathlib import Path
import datetime
from flask_cors import CORS
import shutil
import json
import zipfile
import tempfile
import os

app = Flask(__name__)
DESKTOP = Path.home() / "Desktop"
CORS(app)
@app.route("/", methods=["GET"])
def index():
    """Interface web simples para gerenciar arquivos"""
    html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gerenciador de Arquivos</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 20px; 
            background-color: #1a1a1a; 
            color: #e0e0e0; 
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background-color: #2d2d2d; 
            padding: 20px; 
            border-radius: 8px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.3); 
        }
        .section { 
            margin-bottom: 30px; 
            padding: 20px; 
            border: 1px solid #444; 
            border-radius: 5px; 
            background-color: #333; 
        }
        .section h2 { 
            margin-top: 0; 
            color: #fff; 
        }
        button { 
            padding: 8px 16px; 
            margin: 5px; 
            border: none; 
            border-radius: 4px; 
            cursor: pointer; 
            color: white;
        }
        .btn-primary { background-color: #0056b3; }
        .btn-success { background-color: #1e7e34; }
        .btn-danger { background-color: #bd2130; }
        .btn-info { background-color: #138496; }
        input[type="text"], input[type="file"], textarea { 
            padding: 8px; 
            margin: 5px; 
            border: 1px solid #555; 
            border-radius: 4px; 
            background-color: #404040; 
            color: #e0e0e0; 
        }
        input[type="text"]:focus, textarea:focus {
            border-color: #007bff;
            outline: none;
            background-color: #4a4a4a;
        }
        textarea { 
            width: 100%; 
            height: 100px; 
            resize: vertical; 
        }
        .file-list { 
            background-color: #2a2a2a; 
            padding: 15px; 
            border-radius: 4px; 
            margin: 10px 0; 
            border: 1px solid #444;
        }
        .file-item { 
            padding: 10px; 
            margin: 5px 0; 
            background-color: #3a3a3a; 
            border-radius: 4px; 
            border: 1px solid #555; 
        }
        .file-item strong { 
            color: #ffffff; 
        }
        .result { 
            margin: 10px 0; 
            padding: 10px; 
            border-radius: 4px; 
        }
        .success { 
            background-color: #155724; 
            border: 1px solid #1e7e34; 
            color: #d4edda; 
        }
        .error { 
            background-color: #721c24; 
            border: 1px solid #bd2130; 
            color: #f8d7da; 
        }
        .json-view { 
            background-color: #2a2a2a; 
            padding: 15px; 
            border-radius: 4px; 
            font-family: monospace; 
            white-space: pre-wrap; 
            border: 1px solid #444;
            color: #e0e0e0;
        }
        /* Estilo para navegação rápida */
        .nav-quick {
            background: #404040 !important;
            border: 1px solid #555;
        }
        /* Estilo para breadcrumb */
        .breadcrumb {
            background: #404040 !important;
            border: 1px solid #555;
        }
        /* Links no tema escuro */
        a {
            color: #66b3ff !important;
            text-decoration: none;
        }
        a:hover {
            color: #99ccff !important;
            text-decoration: underline;
        }
        /* Checkboxes no tema escuro */
        input[type="checkbox"] {
            accent-color: #007bff;
        }
        /* Labels no tema escuro */
        label {
            color: #e0e0e0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗂️ Gerenciador de Arquivos</h1>
        
        <!-- LISTAR ARQUIVOS -->
        <div class="section">
            <h2>📂 Listar Arquivos</h2>
            
            <!-- Navegação Rápida -->
            <div class="nav-quick" style="margin-bottom: 15px; padding: 10px; border-radius: 5px;">
                <strong>🚀 Navegação Rápida:</strong><br>
                <button class="btn-info" onclick="listarArquivos('')" style="margin: 2px;">🏠 Desktop</button>
                <button class="btn-info" onclick="listarArquivos('../')" style="margin: 2px;">👤 Pasta do Usuário</button>
                <button class="btn-info" onclick="listarArquivos('../../')" style="margin: 2px;">👥 Usuários</button>
                <button class="btn-info" onclick="navegarParaDisco('C:')" style="margin: 2px;">💾 Disco C:</button>
                <button class="btn-info" onclick="navegarParaDisco('D:')" style="margin: 2px;">💾 Disco D:</button>
                <button class="btn-info" onclick="navegarParaDisco('E:')" style="margin: 2px;">💾 Disco E:</button>
                <button class="btn-info" onclick="listarTodosProgramas()" style="margin: 2px;">⚙️ Programas</button>
                <button class="btn-info" onclick="listarSistema()" style="margin: 2px;">🔧 Sistema</button>
            </div>
            
            <input type="text" id="listPath" placeholder="Caminho (vazio = Desktop, ou caminho absoluto)" style="width: 70%;" />
            <button class="btn-info" onclick="listarArquivos()" style="margin-left: 5px;">📋 Listar</button>
            <button class="btn-info" onclick="voltarDiretorio()" style="margin-left: 5px;">⬅️ Voltar</button>
            <div id="listResult"></div>
        </div>

        <!-- CRIAR ARQUIVO -->
        <div class="section">
            <h2>📝 Criar/Atualizar Arquivo</h2>
            <input type="text" id="createPath" placeholder="Caminho do arquivo (ex: teste.txt)" />
            <br><br>
            <textarea id="createContent" placeholder="Conteúdo do arquivo..."></textarea>
            <br>
            <button class="btn-success" onclick="criarArquivo()">💾 Salvar</button>
            <div id="createResult"></div>
        </div>

        <!-- UPLOAD ARQUIVO -->
        <div class="section">
            <h2>📤 Upload Arquivo</h2>
            <input type="text" id="uploadPath" placeholder="Nome do arquivo destino" />
            <input type="file" id="uploadFile" />
            <button class="btn-success" onclick="uploadArquivo()">📤 Upload</button>
            <div id="uploadResult"></div>
        </div>

        <!-- DELETAR ARQUIVO -->
        <div class="section">
            <h2>🗑️ Deletar Arquivo/Pasta</h2>
            <input type="text" id="deletePath" placeholder="Caminho do arquivo/pasta" />
            <label>
                <input type="checkbox" id="deleteRecursive" /> Deletar pasta recursivamente
            </label>
            <br><br>
            <button class="btn-danger" onclick="deletarArquivo()">🗑️ Deletar</button>
            <div id="deleteResult"></div>
        </div>
    </div>

    <script>
        function showResult(elementId, message, isError = false) {
            const element = document.getElementById(elementId);
            element.innerHTML = `<div class="result ${isError ? 'error' : 'success'}">${message}</div>`;
        }

        function showJson(elementId, data) {
            const element = document.getElementById(elementId);
            element.innerHTML = `<div class="json-view">${JSON.stringify(data, null, 2)}</div>`;
        }

        async function listarArquivos(path = '') {
            console.log('Listando arquivos para o caminho:', path);
            document.getElementById('listPath').value = path;
            
            let url;
            if (path && (path.includes(':') || path.startsWith('../'))) {
                // Navegação no sistema completo
                url = `/items?path=${encodeURIComponent(path)}`;
            } else {
                // Navegação no Desktop (padrão)
                url = path ? `/items/${encodeURIComponent(path)}` : '/items';
            }
            
            try {
                const response = await fetch(url);
                const data = await response.json();
                console.log('Dados recebidos:', data);
                
                if (response.ok) {
                    if (Array.isArray(data)) {
                        exibirListaArquivos(data, path);
                        console.log('Lista atualizada com', data.length, 'itens');
                    } else {
                        showJson('listResult', data);
                    }
                } else {
                    showResult('listResult', `Erro: ${data.error || 'Erro desconhecido'}`, true);
                }
            } catch (error) {
                showResult('listResult', `Erro de conexão: ${error.message}`, true);
            }
        }

        async function criarArquivo() {
            const path = document.getElementById('createPath').value;
            const content = document.getElementById('createContent').value;
            
            if (!path) {
                showResult('createResult', 'Digite o caminho do arquivo', true);
                return;
            }
            
            try {
                const response = await fetch(`/items/${encodeURIComponent(path)}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ content })
                });
                
                const data = await response.json();
                showResult('createResult', data.msg || data.error, !response.ok);
            } catch (error) {
                showResult('createResult', `Erro: ${error.message}`, true);
            }
        }

        async function uploadArquivo() {
            const path = document.getElementById('uploadPath').value;
            const fileInput = document.getElementById('uploadFile');
            const file = fileInput.files[0];
            
            if (!path || !file) {
                showResult('uploadResult', 'Digite o caminho e selecione um arquivo', true);
                return;
            }
            
            const formData = new FormData();
            formData.append('file', file);
            
            try {
                const response = await fetch(`/items/${encodeURIComponent(path)}`, {
                    method: 'PUT',
                    body: formData
                });
                
                const data = await response.json();
                showResult('uploadResult', data.msg || data.error, !response.ok);
            } catch (error) {
                showResult('uploadResult', `Erro: ${error.message}`, true);
            }
        }

        async function deletarArquivo() {
            const path = document.getElementById('deletePath').value;
            const recursive = document.getElementById('deleteRecursive').checked;
            
            if (!path) {
                showResult('deleteResult', 'Digite o caminho do arquivo/pasta', true);
                return;
            }
            
            if (!confirm(`Tem certeza que deseja deletar "${path}"?`)) {
                return;
            }
            
            try {
                const url = recursive ? `/items/${encodeURIComponent(path)}?recursive=true` : `/items/${encodeURIComponent(path)}`;
                const response = await fetch(url, { method: 'DELETE' });
                
                const data = await response.json();
                showResult('deleteResult', data.msg || data.error, !response.ok);
            } catch (error) {
                showResult('deleteResult', `Erro: ${error.message}`, true);
            }
        }

        // Função para download de arquivos
        function downloadFile(filename) {
            const url = `/download/${encodeURIComponent(filename)}`;
            const link = document.createElement('a');
            link.href = url;
            link.download = filename.split('/').pop(); // Pega apenas o nome do arquivo
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        // Função para download de pasta como ZIP
        function downloadZip(foldername) {
            const url = `/download_zip/${encodeURIComponent(foldername)}`;
            const link = document.createElement('a');
            link.href = url;
            link.download = `${foldername.split('/').pop()}.zip`; // Pega apenas o nome da pasta
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        // Função para deletar item (arquivo ou pasta)
        function deleteItem(itemPath) {
            if (confirm(`Tem certeza que deseja deletar "${itemPath}"?`)) {
                deletarArquivo(itemPath, false);
                setTimeout(() => listarArquivos(), 1000); // Recarrega a lista após 1 segundo
            }
        }

        // Navegação para discos específicos
        function navegarParaDisco(disco) {
            listarSistema(disco + '/');
        }

        // Listar todos os programas
        function listarTodosProgramas() {
            listarSistema('C:/Program Files/');
        }

        // Listar arquivos do sistema
        function listarSistema(caminho = 'C:/') {
            fetch(`/items?path=${encodeURIComponent(caminho)}`)
                .then(response => response.json())
                .then(data => {
                    if (Array.isArray(data)) {
                        document.getElementById('listPath').value = caminho;
                        exibirListaArquivos(data, caminho);
                    } else {
                        showResult('listResult', data.error || 'Erro ao listar arquivos do sistema', true);
                    }
                })
                .catch(error => {
                    showResult('listResult', `Erro: ${error.message}`, true);
                });
        }

        // Voltar um diretório
        function voltarDiretorio() {
            const currentPath = document.getElementById('listPath').value;
            if (!currentPath) {
                return; // Já está no Desktop
            }
            
            const pathParts = currentPath.split('/').filter(part => part);
            pathParts.pop(); // Remove o último diretório
            
            if (pathParts.length === 0) {
                listarArquivos(''); // Volta para o Desktop
            } else if (pathParts.length === 1 && pathParts[0].endsWith(':')) {
                listarSistema(pathParts[0] + '/'); // Volta para a raiz do disco
            } else {
                const newPath = pathParts.join('/') + '/';
                listarSistema(newPath);
            }
        }

        // Função auxiliar para exibir lista de arquivos
        function exibirListaArquivos(data, currentPath) {
            let html = '<div class="file-list">';
            
            // Breadcrumb navigation
            html += '<div class="breadcrumb" style="margin-bottom: 15px; padding: 10px; border-radius: 5px;">';
            html += '<strong>📍 Localização atual: </strong>';
            
            if (currentPath && currentPath !== '') {
                const parts = currentPath.split('/').filter(part => part);
                let buildPath = '';
                
                for (let i = 0; i < parts.length; i++) {
                    buildPath += parts[i] + '/';
                    if (i === 0 && parts[i].endsWith(':')) {
                        html += `<a href="#" onclick="listarSistema('${buildPath}'); return false;" style="text-decoration: none;">💾 ${parts[i]}</a>`;
                    } else {
                        html += ` / <a href="#" onclick="listarSistema('${buildPath}'); return false;" style="text-decoration: none;">${parts[i]}</a>`;
                    }
                }
            } else {
                html += '🏠 Desktop';
            }
            html += '</div>';
            
            html += '<h4 style="color: #fff;">📁 Arquivos encontrados (' + data.length + ' itens):</h4>';
            
            data.forEach(item => {
                const icon = item.is_dir ? '📁' : '📄';
                const size = item.is_dir ? '' : ` (${(item.size / 1024).toFixed(1)} KB)`;
                const itemPath = currentPath ? `${currentPath}${item.name}` : item.name;
                
                html += '<div class="file-item" style="display: flex; justify-content: space-between; align-items: center; margin: 5px 0; padding: 10px; border-radius: 4px;">';
                
                // Nome do arquivo/pasta
                html += '<div style="flex: 1;">';
                if (item.is_dir) {
                    const nextPath = currentPath ? `${currentPath}${item.name}/` : `${item.name}/`;
                    if (currentPath && currentPath !== '') {
                        html += `<a href="#" onclick="listarSistema('${nextPath}'); return false;" style="text-decoration: none;">${icon} <strong>${item.name}</strong></a>`;
                    } else {
                        html += `<a href="#" onclick="listarArquivos('${item.name}'); return false;" style="text-decoration: none;">${icon} <strong>${item.name}</strong></a>`;
                    }
                } else {
                    html += `${icon} <strong style="color: #fff;">${item.name}</strong>`;
                }
                html += `${size} <br><small style="color: #ccc;">Modificado: ${new Date(item.modified).toLocaleString()}</small>`;
                html += '</div>';
                
                // Botões de ação
                html += '<div style="margin-left: 10px;">';
                if (item.is_dir) {
                    html += `<button class="btn-info" onclick="downloadZip('${itemPath}')" style="margin-left: 5px; padding: 5px 10px; border: none; border-radius: 3px; cursor: pointer;">📦 ZIP</button>`;
                } else {
                    html += `<button class="btn-success" onclick="downloadFile('${itemPath}')" style="margin-left: 5px; padding: 5px 10px; border: none; border-radius: 3px; cursor: pointer;">📥 Download</button>`;
                }
                html += '</div>';
                
                html += '</div>';
            });
            
            if (data.length === 0) {
                html += '<p style="text-align: center; color: #ccc; padding: 20px;">Nenhum arquivo encontrado nesta pasta.</p>';
            }
            
            html += '</div>';
            document.getElementById('listResult').innerHTML = html;
        }

        // Carregar lista inicial
        window.onload = () => listarArquivos();
    </script>
</body>
</html>
    """
    return html

def safe_target(subpath: str) -> Path:
    # Se é caminho absoluto e começa com uma letra de drive (ex: C:, D:)
    if len(subpath) >= 2 and subpath[1] == ':':
        target = Path(subpath).resolve()
        return target
    
    # Se começa com ../ significa navegar para fora do Desktop
    if subpath.startswith('../'):
        # Remove o ../ e navega a partir do diretório pai do Desktop
        relative_path = subpath[3:]  # Remove '../'
        if relative_path:
            target = (DESKTOP.parent / relative_path).resolve()
        else:
            target = DESKTOP.parent.resolve()
        return target
    
    # Caminho relativo normal baseado no Desktop
    if not subpath:
        return DESKTOP.resolve()
    
    target = (DESKTOP / subpath).resolve()
    return target

def safe_system_target(path: str) -> Path:
    """Permite navegação em todo o sistema com validações básicas"""
    if not path:
        return DESKTOP.resolve()
    
    try:
        target = Path(path).resolve()
        # Verificações básicas de segurança
        if target.exists():
            return target
        else:
            # Se não existe, retorna None para indicar erro
            return None
    except:
        return None

@app.route("/items", methods=["GET"])
def listar_desktop():
    # Verifica se foi especificado um caminho como parâmetro de query
    system_path = request.args.get('path', '')
    
    if system_path:
        # Navegação no sistema completo
        target = safe_system_target(system_path)
        if not target or not target.exists():
            return jsonify({"error": f"Caminho não encontrado: {system_path}"}), 404
        
        if not target.is_dir():
            return jsonify({"error": "Caminho especificado não é um diretório"}), 400
            
        base_path = target
    else:
        # Navegação padrão no Desktop
        if not DESKTOP.exists():
            return jsonify({"error": "Desktop não encontrada"}), 404
        base_path = DESKTOP

    itens = []
    try:
        for p in sorted(base_path.iterdir(), key=lambda x: x.name.lower()):
            try:
                stat = p.stat()
                itens.append({
                    "name": p.name,
                    "is_dir": p.is_dir(),
                    "size": stat.st_size,
                    "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
            except Exception:
                continue
    except PermissionError:
        return jsonify({"error": "Acesso negado a este diretório"}), 403
    except Exception as e:
        return jsonify({"error": f"Erro ao listar diretório: {str(e)}"}), 500

    # Retorna JSON formatado para melhor visualização
    return Response(
        json.dumps(itens, indent=2, ensure_ascii=False),
        mimetype='application/json; charset=utf-8'
    )
    for p in sorted(DESKTOP.iterdir(), key=lambda x: x.name.lower()):
        try:
            stat = p.stat()
            itens.append({
                "name": p.name,
                "is_dir": p.is_dir(),
                "size": stat.st_size,
                "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        except Exception:
            continue

    # Retorna JSON formatado para melhor visualização
    return Response(
        json.dumps(itens, indent=2, ensure_ascii=False),
        mimetype='application/json; charset=utf-8'
    )

@app.route("/items/<path:subpath>", methods=["GET"])
def listar_ou_serve(subpath):
    target = safe_target(subpath)
    if not target.exists():
        return jsonify({"error": "Não encontrado"}), 404

    if target.is_file():
        # serve o arquivo
        relative = str(target.relative_to(DESKTOP))
        return send_from_directory(str(DESKTOP), relative, as_attachment=False)

    # é pasta -> lista conteúdo
    itens = []
    for p in sorted(target.iterdir(), key=lambda x: x.name.lower()):
        try:
            stat = p.stat()
            itens.append({
                "name": p.name,
                "is_dir": p.is_dir(),
                "size": stat.st_size,
                "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        except Exception:
            continue
    
    # Retorna JSON formatado para melhor visualização
    return Response(
        json.dumps(itens, indent=2, ensure_ascii=False),
        mimetype='application/json; charset=utf-8'
    )

@app.route("/download/<path:filename>", methods=["GET"])
def download(filename):
    target = safe_target(filename)
    if not target.exists() or target.is_dir():
        return jsonify({"error": "Arquivo não encontrado"}), 404
    relative = str(target.relative_to(DESKTOP))
    return send_from_directory(str(DESKTOP), relative, as_attachment=True)

@app.route("/download_zip/<path:foldername>", methods=["GET"])
def download_zip(foldername):
    """Download de pasta como arquivo ZIP"""
    target = safe_target(foldername)
    if not target.exists() or not target.is_dir():
        return jsonify({"error": "Pasta não encontrada"}), 404
    
    # Criar arquivo ZIP temporário
    temp_dir = tempfile.mkdtemp()
    zip_filename = f"{target.name}.zip"
    zip_path = os.path.join(temp_dir, zip_filename)
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Adicionar todos os arquivos da pasta ao ZIP
            for root, dirs, files in os.walk(target):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Calcular caminho relativo dentro do ZIP
                    arcname = os.path.relpath(file_path, target.parent)
                    zipf.write(file_path, arcname)
        
        # Enviar o arquivo ZIP
        return send_from_directory(temp_dir, zip_filename, as_attachment=True)
    
    except Exception as e:
        return jsonify({"error": f"Erro ao criar ZIP: {str(e)}"}), 500

# -----------------------
# Atualizar / Criar arquivo
# -----------------------
@app.route("/items/<path:subpath>", methods=["PUT"])
def atualizar_arquivo(subpath):
    """
    - Se enviar multipart/form-data com campo 'file' -> salva/overwrite arquivo com o conteúdo binário.
    - Se enviar JSON {"content": "..."} -> grava texto UTF-8.
    - Cria diretório pai se necessário.
    """
    target = safe_target(subpath)
    parent = target.parent
    parent.mkdir(parents=True, exist_ok=True)

    # multipart/form-data file upload
    if "file" in request.files:
        uploaded = request.files["file"]
        # salva o arquivo (sobrescreve)
        uploaded.save(str(target))
        return jsonify({"msg": "Arquivo salvo (upload)"}), 200

    # json text content
    if request.is_json:
        data = request.json
        content = data.get("content")
        if content is None:
            return jsonify({"error": "JSON deve conter a chave 'content'"}), 400
        # escreve texto
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        return jsonify({"msg": "Arquivo salvo (conteúdo JSON)"}), 200

    return jsonify({"error": "Envie multipart/form-data com campo 'file' ou JSON com 'content'"}), 400

# -----------------------
# Deletar arquivo / pasta
# -----------------------
@app.route("/items/<path:subpath>", methods=["DELETE"])
def deletar(subpath):
    """
    - Para arquivos: deleta direto.
    - Para pastas:
        - se vazia -> deleta
        - se não vazia -> exigir ?recursive=true para remover recursivamente
    """
    target = safe_target(subpath)
    if not target.exists():
        return jsonify({"error": "Não encontrado"}), 404

    if target.is_file():
        target.unlink()
        return jsonify({"msg": "Arquivo deletado"}), 200

    # é diretório
    recursive = request.args.get("recursive", "false").lower() == "true"
    # verifica se vazio
    try:
        next(target.iterdir())
        is_empty = False
    except StopIteration:
        is_empty = True

    if is_empty:
        target.rmdir()
        return jsonify({"msg": "Pasta vazia deletada"}), 200

    if recursive:
        shutil.rmtree(target)
        return jsonify({"msg": "Pasta deletada recursivamente"}), 200

    return jsonify({
        "error": "Pasta não vazia. Para deletar recursivamente, adicione ?recursive=true"
    }), 400

if __name__ == "__main__":
    import sys
    import logging
    import os
    
    # Para deploy na Render e outros serviços
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    
    # Verificar se deve executar em modo silencioso
    silent_mode = '--silent' in sys.argv or '--no-console' in sys.argv or os.environ.get('FLASK_ENV') == 'production'
    
    if silent_mode or os.environ.get('PORT'):  # Se PORT está definida, provavelmente é deploy
        # Configurar logging para arquivo
        logging.basicConfig(
            filename='server.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Redirecionar stdout e stderr para arquivos apenas se não estiverem já redirecionados
        if not os.getenv('PYTHONIOENCODING') and not os.environ.get('PORT'):
            try:
                sys.stdout = open('server_output.log', 'w', encoding='utf-8')
                sys.stderr = open('server_error.log', 'w', encoding='utf-8')
            except:
                pass  # Se falhar, continua normalmente
        
        # Executar sem output de debug
        app.run(host=host, port=port, debug=False, use_reloader=False)
    else:
        print("🚀 Servidor iniciando...")
        print(f"📍 Acesse: http://127.0.0.1:{port}")
        print("💡 Para executar sem terminal, use: python server.py --silent")
        print("🛑 Para parar, pressione Ctrl+C")
        app.run(host=host, port=port, debug=False)
