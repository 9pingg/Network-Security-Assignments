import socket
import datetime
import ssl
from base64 import b64decode
from base64 import b64encode
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP



# Path to the TLS certificate and private key
tsa_cert = "/Users/vedan/Desktop/NS-Assignments/A4/ssl/cert_s.pem"
tsa_key = "/Users/vedan/Desktop/NS-Assignments/A4/ssl/key_s.pem"


# Create an SSL context
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile=tsa_cert, keyfile=tsa_key)
ssl_context.load_verify_locations(cafile=tsa_cert)

# Generate the RSA key pair and export the public and private keys
rsa_key = RSA.generate(2048)
private_key = rsa_key.publickey().export_key()
tsa_pub_key = rsa_key.export_key()
s = PKCS1_OAEP.new(rsa_key)


def tsa_server():

    # Create a socket object and bind it to the server address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    print(f"Starting TSA server on {server_address[0]}:{server_address[1]}")
    sock.bind(server_address)
    sock.listen(1)

    while True:
        print("Waiting for a connection...")
        c, client_ip = sock.accept()
        # Wrap the socket with SSL/TLS
        sls_connection = ssl_context.wrap_socket(c, server_side=True)

        try:
            print(f"\nConnection from {client_ip}\n")
            # Receive the hash from the client
            data = sls_connection.recv(4096)

            if data:
                # Calculate the timestamp
                timestamp = datetime.datetime.now().isoformat().encode('utf-8')

                # Calculate the hash of the timestamped hash
                data_with_tstamp_pubkey = data + timestamp + tsa_pub_key
                hash_func = SHA256.new()
                hash_func.update(data_with_tstamp_pubkey)
                timestamped_hash = hash_func.digest()

                # Sign the timestamped hash with the TSA's private key
                signature = s.encrypt(timestamped_hash)

                # Combine the signature, timestamp, and TSA public key into a single response string
                response = b64encode(signature).decode('utf-8') + "," + b64encode(timestamp).decode('utf-8') + "," + b64encode(tsa_pub_key).decode('utf-8')

                print("\nResponse send to client:\n", response, "\n\n")
                sls_connection.sendall(response.encode('utf-8'))
                
            else:
                print("No data received from client")

        except Exception as e:
            print(f"Exception occurred: {e}")

        finally:
            # Close the connection
            sls_connection.shutdown(socket.SHUT_RDWR)
            sls_connection.close()

if __name__ == "__main__":
    tsa_server()
