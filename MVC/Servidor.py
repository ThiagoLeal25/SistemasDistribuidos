import socket
import json

# ==========================================
# 1. MODEL (Modelo - Dados e Regras de Negócio)
# ==========================================
class UserModel:
    def __init__(self):
        # Banco de dados simulado em memória
        self.users = [] 

    def add_user(self, name, email):
        # Validação: Verifica se o e-mail já existe
        for user in self.users:
            if user['email'].lower() == email.lower():
                return {"success": False, "message": "Erro: Este e-mail já está cadastrado!"}
        
        # Adiciona o novo usuário
        self.users.append({"name": name, "email": email})
        
        # Regra de negócio: Sempre ordenar pelo nome após inserção
        self.users.sort(key=lambda u: u['name'].lower())
        
        return {"success": True, "data": self.users}


# ==========================================
# 2. VIEW (Visão - Formatação da Resposta)
# ==========================================
class UserView:
    @staticmethod
    def render_response(result):
        if not result["success"]:
            return f"[ERRO] {result['message']}\n"
        
        # Formata a lista de usuários ordenados para exibição
        output = "\n--- LISTA DE USUÁRIOS ATUALIZADA (ORDENADA) ---\n"
        for idx, user in enumerate(result["data"], 1):
            output += f"{idx}. {user['name']} ({user['email']})\n"
        output += "----------------------------------------------\n"
        return output


# ==========================================
# 3. CONTROLLER (Controlador - Orquestração)
# ==========================================
class UserController:
    def __init__(self):
        self.model = UserModel()
        self.view = UserView()

    def handle_request(self, raw_data):
        try:
            # Transforma a string JSON recebida em dicionário Python
            data = json.loads(raw_data)
            name = data.get("name")
            email = data.get("email")

            if not name or not email:
                return "[ERRO] Nome e e-mail são obrigatórios.\n"

            # Envia para o Model processar e aplicar as regras
            result = self.model.add_user(name, email)
            
            # Passa o resultado para a View formatar o retorno
            return self.view.render_response(result)

        except json.JSONDecodeError:
            return "[ERRO] Formato de dados inválido. Envie um JSON.\n"


# ==========================================
# CONFIGURAÇÃO E INICIALIZAÇÃO DO SOCKET
# ==========================================
def run_server():
    HOST = '127.0.0.1'
    PORT = 8001

    controller = UserController()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    
    print(f"[*] Servidor MVC Socket rodando em {HOST}:{PORT}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[*] Conexão aceita de {addr}")
        
        try:
            # Recebe os dados do cliente
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                # O Controller processa a requisição e gera a resposta
                response = controller.handle_request(data)
                # Envia a resposta de volta ao cliente
                client_socket.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"[!] Erro ao processar: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    run_server()
