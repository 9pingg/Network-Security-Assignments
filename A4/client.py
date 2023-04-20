import hashlib
import socket
import os
import ssl
from base64 import b64decode
from base64 import b64encode
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

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

# Connect to the TSA server using SSL/TLS
server_address = ('localhost', 10000)
with socket.create_connection(server_address) as sock:
    with ssl_context.wrap_socket(sock, server_hostname=server_address[0]) as ssock:

        # Send the file hash to the TSA server
        ssock.sendall(file_hash.encode())

        # Receive the signed timestamp from the TSA server
        timestamp_bytes = ssock.recv(4096)
        
        # Split the received data into signature, timestamp, and TSA public key
        signature, timestamp, tsa_pub_key = timestamp_bytes.decode().split(",")
        signature = b64decode(signature)
        timestamp = b64decode(timestamp)
        tsa_pub_key = b64decode(tsa_pub_key)

        # Import the TSA public key and use it to decrypt the received signature
        tsa_pub_key_n = RSA.import_key(tsa_pub_key)
        cipher = PKCS1_OAEP.new(tsa_pub_key_n)
        decrypted_signature = cipher.decrypt(signature)
        
        # Calculate the hash of the file_hash, timestamp, and TSA public key
        hash_func = SHA256.new()
        data_with_tstamp_pubkey = file_hash.encode() + timestamp + tsa_pub_key        
        hash_func.update(data_with_tstamp_pubkey)
        timestamped_hash = hash_func.digest()
        
        # Verify the decrypted signature against the calculated hash
        print("\ndecrypted_signature: ", decrypted_signature)
        print("\nhash_to_be_checked:  ", timestamped_hash)

        if decrypted_signature == timestamped_hash: 
            print("\nSignature verified.\n\n")
            print("File Hash: ", file_hash.encode())
            print("\nTimestamp: ", timestamp)
            print("\nPublic Key TSA: ", b64encode(tsa_pub_key))
            print("\nSignature: ", b64encode(signature))

            # Save the received data to a file
            fp = "client_tsa_document.txt"
            with open(fp, 'wb') as f:
                f.write(b'File Hash: ')
                f.write(file_hash.encode())
                f.write(os.linesep.encode())
                f.write(b'Timestamp: ')
                f.write(timestamp)
                f.write(os.linesep.encode())
                f.write(b'TSA Public Key: ')
                f.write(b64encode(tsa_pub_key))
                f.write(os.linesep.encode())
                f.write(b'Signature: ')
                f.write(b64encode(signature))

        
# client_address = ('localhost', 10001)
# with socket.create_connection(server_address) as sock:
#     with ssl_context.wrap_socket(sock, server_hostname=server_address[0]) as ssock:
#         ssock.sendall(file_hash.encode())
#         timestamp_bytes = ssock.recv(4096)

