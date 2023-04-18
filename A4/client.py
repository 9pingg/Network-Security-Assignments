import hashlib
import socket
import ssl
import datetime
from base64 import b64decode
from base64 import b64encode
# Load the SSL/TLS certificate of the TSA server
tls_cert = "/Users/vedan/Desktop/NS-Assignments/A4/cert.pem"
client_cert = "/Users/vedan/Desktop/NS-Assignments/A4/cert_c.pem"
client_key = "/Users/vedan/Desktop/NS-Assignments/A4/key_c.pem"
# Connect to the TSA server over an encrypted connection
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)
context.load_verify_locations(cafile=tls_cert)





# Generate a hash of the file to be timestamped
filename = "cert_generate.txt"
with open(filename, "rb") as f:
    file_data = f.read()
    file_hash = hashlib.sha256(file_data).hexdigest()

server_address = ('localhost', 10000)
with socket.create_connection(server_address) as sock:
    with context.wrap_socket(sock, server_hostname=server_address[0]) as ssock:
        # Send the file hash to the TSA server
        ssock.sendall(file_hash.encode())

        # Receive the signed timestamp from the TSA server
        timestamp_bytes = ssock.recv(1024)
        hash, signature, timestamp = timestamp_bytes.decode().split(",")
        hash = b64decode(hash)
        signature = b64decode(signature)
        timestamp = b64decode(timestamp)
        print(timestamp)
        print(signature, timestamp)

# Verify the signed timestamp using the TSA's public key (not implemented in this example)
