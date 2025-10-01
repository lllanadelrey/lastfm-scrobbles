import pylast
import time
import sys
from datetime import datetime

# --- CONFIGURAÇÕES DE AUTENTICAÇÃO E DA MÚSICA ---

# Credenciais de Aplicação
API_KEY = "284880e097d91c86ed590c50f7f398db"
API_SECRET = "78cb1bfcf0de7b51a789ed735b541507" 

# SESSION KEY PERMANENTE OBTIDA VIA AUTORIZAÇÃO MANUAL
SESSION_KEY = "wG43G3jJbF7wB4d9bY6s5x5vL7wB4d9b" 
USERNAME = "luizzzyq" 

# Detalhes da Música para Scrobble
ARTIST_NAME = "Lana Del Rey"
TRACK_TITLE = "Black Beauty"
ALBUM_TITLE = "Ultraviolence"

# --- CONFIGURAÇÕES DO LOOP ---
INTERVAL_SECONDS = 6

# --- FUNÇÃO PRINCIPAL ---

def scrobble_loop():
    
    # 1. Configurar a rede Last.fm
    print("= INICIANDO CONFIGURAÇÃO (pylast) =")
    try:
        # pylast autentica diretamente com a Session Key
        network = pylast.LastFMNetwork(
            api_key=API_KEY,
            api_secret=API_SECRET,
            session_key=SESSION_KEY 
        )
        print("STATUS: Conexão pylast estabelecida com Session Key.")
        # Teste rápido para confirmar que a chave pertence ao usuário
        user = network.get_authenticated_user()
        print(f"Usuário autenticado: {user.get_name()}")
        
    except Exception as e:
        print(f"ERRO CRÍTICO: Falha ao conectar ou autenticar: {e}")
        print("Verifique a Session Key. Se o erro for persistente, o Last.fm pode ter revogado a chave.")
        return

    # 2. Iniciar o Loop de Scrobble
    scrobble_count = 0
    
    print("\n= INICIANDO LOOP DE SCROBBLE =")
    print(f"MÚSICA: {ARTIST_NAME} - {TRACK_TITLE}")
    print(f"INTERVALO: {INTERVAL_SECONDS} segundos")
    print("\nPARA PARAR: Pressione Ctrl+C a qualquer momento.")
    print("=" * 40)

    while True:
        try:
            scrobble_count += 1
            timestamp = int(time.time())
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"[{current_time}] SCROBBLE #{scrobble_count}: Enviando...")
            
            # Scrobble usando pylast
            network.scrobble(
                artist=ARTIST_NAME, 
                title=TRACK_TITLE, 
                timestamp=timestamp, 
                album=ALBUM_TITLE
            )
            
            print(f"[{current_time}] SCROBBLE #{scrobble_count}: SUCESSO. Próximo envio em {INTERVAL_SECONDS}s.")
            print("-" * 40)
            
            # Pausa
            time.sleep(INTERVAL_SECONDS)

        except pylast.WSError as e:
            # Erros de API do Last.fm (incluindo "Invalid Session Key")
            print(f"\n[{current_time}] ERRO NA API (Scrobble #{scrobble_count}): Falha no envio.")
            print(f"DETALHE DO ERRO: {e.details}")
            print(f"STATUS: Tentando novamente em {INTERVAL_SECONDS} segundos...")
            print("-" * 40)
            scrobble_count -= 1 
            time.sleep(INTERVAL_SECONDS) 

        except KeyboardInterrupt:
            # Captura Ctrl+C
            print("\n" + "=" * 40)
            print("ENCERRANDO...")
            print(f"STATUS: Loop de Scrobble INTERROMPIDO. Total de {scrobble_count} scrobbles enviados.")
            print("=" * 40)
            sys.exit(0)
            
        except Exception as e:
            # Outros erros
            print(f"\n[{current_time}] ERRO INESPERADO (Scrobble #{scrobble_count}): Falha no envio.")
            print(f"DETALHE DO ERRO: {e}")
            print(f"STATUS: Tentando novamente em {INTERVAL_SECONDS} segundos...")
            print("-" * 40)
            scrobble_count -= 1 
            time.sleep(INTERVAL_SECONDS)


if __name__ == '__main__':
    scrobble_loop()
