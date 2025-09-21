import subprocess
import sys
import os
import time

def verificar_servidor():
    """Verifica se o servidor está respondendo"""
    try:
        import urllib.request
        response = urllib.request.urlopen('http://127.0.0.1:5000', timeout=2)
        if response.getcode() == 200:
            print("🟢 Servidor está rodando em http://127.0.0.1:5000")
            return True
    except:
        print("🔴 Servidor não está respondendo")
        return False

def parar_servidor_por_porta():
    """Para o processo que está usando a porta 5000"""
    try:
        # Encontrar processo usando a porta 5000
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            linhas = result.stdout.split('\n')
            pid_encontrado = None
            
            for linha in linhas:
                if ':5000' in linha and 'LISTENING' in linha:
                    partes = linha.split()
                    if len(partes) >= 5:
                        pid_encontrado = partes[-1]
                        break
            
            if pid_encontrado:
                print(f"🎯 Encontrado processo na porta 5000 (PID: {pid_encontrado})")
                
                # Tentar parar o processo específico
                resultado = subprocess.run(['taskkill', '/F', '/PID', pid_encontrado], 
                                         capture_output=True, text=True, shell=True)
                
                if resultado.returncode == 0:
                    print("✅ Servidor parado com sucesso!")
                    return True
                else:
                    print(f"❌ Erro ao parar processo: {resultado.stderr}")
                    return False
            else:
                print("❌ Nenhum processo encontrado na porta 5000")
                return False
        else:
            print("❌ Erro ao listar conexões de rede")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def parar_servidor_por_nome():
    """Para processos Python que possam ser nosso servidor (método alternativo)"""
    try:
        # Listar processos Python
        result = subprocess.run(['wmic', 'process', 'where', 'name="python.exe"', 'get', 'ProcessId,CommandLine'], 
                              capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            linhas = result.stdout.strip().split('\n')
            processos_parados = 0
            
            for linha in linhas:
                if 'server.py' in linha:
                    # Extrair PID da linha
                    partes = linha.strip().split()
                    if len(partes) >= 1:
                        try:
                            pid = partes[-1]  # PID geralmente é o último elemento
                            if pid.isdigit():
                                print(f"🎯 Parando servidor Python (PID: {pid})")
                                resultado = subprocess.run(['taskkill', '/F', '/PID', pid], 
                                                         capture_output=True, text=True, shell=True)
                                if resultado.returncode == 0:
                                    processos_parados += 1
                        except:
                            continue
            
            if processos_parados > 0:
                print(f"✅ {processos_parados} processo(s) do servidor parado(s)")
                return True
            else:
                print("❌ Nenhum servidor Python encontrado")
                return False
        else:
            print("❌ Erro ao listar processos Python")
            return False
            
    except Exception as e:
        print(f"❌ Erro no método alternativo: {e}")
        return False

def parar_todos_python():
    """Para todos os processos Python (último recurso)"""
    try:
        resultado = subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                                 capture_output=True, text=True, shell=True)
        
        if resultado.returncode == 0:
            print("✅ Todos os processos Python foram finalizados")
            return True
        else:
            print("❌ Nenhum processo Python encontrado para finalizar")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao finalizar processos Python: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Verificando status do servidor...")
    servidor_ativo = verificar_servidor()
    
    if servidor_ativo:
        print("\n🛑 Servidor detectado. Escolha o método para parar:")
        print("1. Por porta (recomendado)")
        print("2. Por nome do processo")
        print("3. Parar todos os Python")
        print("4. Cancelar")
        
        try:
            escolha = input("\nEscolha (1-4): ").strip()
            
            if escolha == "1":
                sucesso = parar_servidor_por_porta()
            elif escolha == "2":
                sucesso = parar_servidor_por_nome()
            elif escolha == "3":
                confirma = input("⚠️  Isso irá parar TODOS os processos Python. Confirma? (s/n): ")
                if confirma.lower() in ['s', 'sim', 'y', 'yes']:
                    sucesso = parar_todos_python()
                else:
                    print("✅ Operação cancelada")
                    sucesso = False
            elif escolha == "4":
                print("✅ Operação cancelada")
                sucesso = False
            else:
                print("❌ Opção inválida")
                sucesso = False
            
            if sucesso:
                print("\n⏳ Aguardando 2 segundos...")
                time.sleep(2)
                print("🔍 Verificando se o servidor parou...")
                if not verificar_servidor():
                    print("✅ Servidor parado com sucesso!")
                else:
                    print("⚠️  Servidor ainda está respondendo")
        
        except KeyboardInterrupt:
            print("\n✅ Operação cancelada pelo usuário")
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
    
    else:
        print("✅ Servidor já está parado")
    
    input("\nPressione Enter para sair...")