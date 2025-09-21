# Deploy do Gerenciador de Arquivos

## 🚀 Como fazer deploy na Render

### 1. Preparação dos arquivos
✅ `requirements.txt` - Dependências Python
✅ `Procfile` - Comando para iniciar o servidor
✅ `runtime.txt` - Versão do Python
✅ `server.py` - Servidor Flask modificado para produção

### 2. Deploy na Render

1. **Acesse**: https://render.com
2. **Crie uma conta** (pode usar GitHub)
3. **Clique em "New +"** → **"Web Service"**
4. **Conecte seu repositório** GitHub ou faça upload dos arquivos
5. **Configure**:
   - **Name**: `meu-gerenciador-arquivos`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn server:app`
   - **Instance Type**: `Free`

### 3. Variáveis de ambiente (opcional)
```
FLASK_ENV=production
PORT=10000
```

### 4. URL final
Após o deploy: `https://meu-gerenciador-arquivos.onrender.com`

## 📋 Arquivos incluídos:

- **requirements.txt**: Todas as dependências necessárias
- **Procfile**: Comando para executar o servidor com Gunicorn
- **runtime.txt**: Especifica Python 3.11
- **server.py**: Modificado para produção (suporte ao PORT da Render)

## ⚠️ Limitações da versão gratuita:
- Pode "dormir" após 15 minutos de inatividade
- Restart automático após inatividade
- Bandwidth limitado

## 🌟 Funcionalidades que funcionarão:
- ✅ Upload/download de arquivos
- ✅ Navegação em pastas
- ✅ Interface web completa
- ✅ API REST funcional
- ✅ CORS configurado