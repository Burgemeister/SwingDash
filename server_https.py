import http.server
import ssl
import os

PORT = 8000
# Pad naar de huidige map waar het script draait
current_dir = os.path.dirname(os.path.abspath(__file__))
KEY_FILE = os.path.join(current_dir, 'key.pem')
CERT_FILE = os.path.join(current_dir, 'cert.pem')

# Definieer de handler (standaard SimpleHTTPRequestHandler)
handler = http.server.SimpleHTTPRequestHandler

# Maak een SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
try:
    print(f"Pogen certificaat te laden: {CERT_FILE}")
    print(f"Pogen key te laden: {KEY_FILE}")
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
except FileNotFoundError:
    print(f"FOUT: Certificaat ({CERT_FILE}) of key ({KEY_FILE}) niet gevonden.")
    print("Zorg ervoor dat key.pem en cert.pem in dezelfde map staan als dit script.")
    exit()
except ssl.SSLError as e:
    print(f"SSL FOUT bij het laden van certificaat/key: {e}")
    print("Mogelijk is het certificaat of de key corrupt of niet correct gegenereerd.")
    print("Probeer de .pem bestanden opnieuw te genereren.")
    exit()
except Exception as e:
    print(f"Algemene FOUT bij laden certificaat/key: {e}")
    exit()

# Maak de HTTPS server
# We binden aan 'localhost' om er zeker van te zijn dat het overeenkomt met het certificaat CN
server_address = ('localhost', PORT)
with http.server.HTTPServer(server_address, handler) as httpd:
    print(f"Serving HTTPS op https://{server_address[0]}:{server_address[1]}/")
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer gestopt.")
        httpd.server_close()

