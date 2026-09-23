import socket
import json
import sys

def send_user(name, email):
    HOST = '127.0.0.1'
    PORT = 8001

    # Cria o payload em formato JSON
    payload = json.dumps({"name": name, "email": email})

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        
        # Envia os dados
        client_socket.sendall(payload.encode('utf-8'))
        
        # Recebe e exibe a resposta formatada pelo servidor
        response = client_socket.recv(4096).decode('utf-8')
        print(response)
        
    except ConnectionRefusedError:
        print("[ERRO] Não foi possível conectar ao servidor. Ele está rodando?")
    finally:
        client_socket.close()

if __name__ == "__main__":
    print("--- Cadastro de Usuário via Socket ---")
    nome = input("Digite o nome: ")
    email = input("Digite o e-mail: ")
    
    if nome and email:
        send_user(nome, email)
    else:
        print("[ERRO] Nome e e-mail não podem ser vazios.")
