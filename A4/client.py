import hashlib
import socket
import ssl
import datetime
from base64 import b64decode
from base64 import b64encode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
import os

# Load the SSL/TLS certificate of the TSA server
tsa_cert = "/Users/vedan/Desktop/NS-Assignments/A4/ssl/cert_s.pem"
client_cert = "/Users/vedan/Desktop/NS-Assignments/A4/ssl/cert_c.pem"
client_key = "/Users/vedan/Desktop/NS-Assignments/A4/ssl/key_c.pem"
# Connect to the TSA server over an encrypted connection
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_cert_chain(certfile=client_cert, keyfile=client_key)
ssl_context.load_verify_locations(cafile=tsa_cert)


# Generate a hash of the file to be timestamped
fp = "cert_generate.txt"
with open(fp, "rb") as f:
    file_data = f.read()
    file_hash = hashlib.sha256(file_data).hexdigest()

hash_func = SHA256.new()
server_address = ('localhost', 10000)
with socket.create_connection(server_address) as sock:
    with ssl_context.wrap_socket(sock, server_hostname=server_address[0]) as ssock:
        # Send the file hash to the TSA server
        ssock.sendall(file_hash.encode())

        # Receive the signed timestamp from the TSA server
        timestamp_bytes = ssock.recv(4096)
        
        signature, timestamp, tsa_pub_key = timestamp_bytes.decode().split(",")
        signature = b64decode(signature)
        timestamp = b64decode(timestamp)
        tsa_pub_key = b64decode(tsa_pub_key)

        
        tsa_pub_key_n = RSA.import_key(tsa_pub_key)
        cipher = PKCS1_OAEP.new(tsa_pub_key_n)
        decrypted_signature = cipher.decrypt(signature)
        
        
        data_with_tstamp_pubkey = file_hash.encode() + timestamp + tsa_pub_key        
        hash_func.update(data_with_tstamp_pubkey)
        timestamped_hash = hash_func.digest()
        
        print(decrypted_signature)
        print(timestamped_hash)

        if decrypted_signature == timestamped_hash: 
            print("verified")
            print("File Hash: ", file_hash.encode())
            print("Timestamp: ", timestamp)
            print("Public Key TSA: ", b64encode(tsa_pub_key))
            print("Signature: ", signature)

            fp = "client_a_cert_tsa.txt"
            with open(fp, 'wb') as f:
                f.write(file_hash.encode())
                f.write(os.linesep.encode())
                f.write(timestamp)
                f.write(os.linesep.encode())
                f.write(b64encode(tsa_pub_key))
                f.write(os.linesep.encode())
                f.write(b64encode(signature))

        

