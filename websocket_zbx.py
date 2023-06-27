import websocket
import time

def monitorar_conexao(url):
    conexao_recusada = False  # Variável de controle para rastrear o estado da conexão

    while True:
        try:
            ws = websocket.WebSocket()
            ws.connect(url)

            if ws.connected:
                if conexao_recusada:
                    print("Conexão restabelecida com sucesso.")
                    conexao_recusada = False  # Resetar o estado da conexão recusada
                else:
                    print("Conexão estabelecida com sucesso.")
            else:
                print("Falha ao estabelecer conexão.")

            ws.close()
        except ConnectionRefusedError:
            if not conexao_recusada:
                print("Conexão recusada. Verifique se o serviço de WebSocket está em execução.")
                conexao_recusada = True

        time.sleep(60)  # Espera 1 minuto

url = "wss://exemplo.com/ws"

monitorar_conexao(url)