import socket
import hashlib
import datetime
import ssl
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from base64 import b64decode
from base64 import b64encode

# Path to the TLS certificate and private key
tls_cert = "/Users/vedan/Desktop/NS-Assignments/A4/cert.pem"
tls_key = "/Users/vedan/Desktop/NS-Assignments/A4/key.pem"


# Create an SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=tls_cert, keyfile=tls_key)
context.load_verify_locations(cafile=tls_cert)

# Initialize the RSA key and hash function
rsa_key = RSA.generate(2048)
hash_func = SHA256.new()

# Define the TSA server
def tsa_server():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_address = ('localhost', 10000)
    print(f"Starting TSA server on {server_address[0]}:{server_address[1]}")
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    with open("server.pub", "rb") as f:
        tsa_pub_key = ssl.DER_cert_to_PEM_cert(f.read())
    # Start the main loop
    while True:
        print("Waiting for a connection...")
        # Wait for a connection
        connection, client_address = sock.accept()

        # Wrap the socket with SSL/TLS
        ssl_conn = context.wrap_socket(connection, server_side=True)

        try:
            print(f"Connection from {client_address}")

            # Receive the hash from the client
            data = ssl_conn.recv(1024)

            if data:
                # Calculate the timestamp
                timestamp = datetime.datetime.now().isoformat().encode('utf-8')
                print(timestamp)
                print(tsa_pub_key)
                # Calculate the hash of the timestamped hash
                data_with_tstamp_pubkey = data + timestamp + tsa_pub_key
                # hash_func.update(data)
                hash_func.update(data_with_tstamp_pubkey)
                timestamped_hash = hash_func.digest()

                # Sign the timestamped hash with the TSA's private key
                signature = pkcs1_15.new(rsa_key).sign(hash_func)

                # Construct the response message
                response = b64encode(timestamped_hash).decode('utf-8') + "," + b64encode(signature).decode('utf-8') + "," + b64encode(timestamp).decode('utf-8') + b64encode(tsa_pub_key).decode('utf-8')
                print(response)
                # Send the response to the client
                ssl_conn.sendall(response.encode('utf-8'))
                
            else:
                print("No data received from client")

        except Exception as e:
            print(f"Exception occurred: {e}")

        finally:
            # Close the connection
            ssl_conn.shutdown(socket.SHUT_RDWR)
            ssl_conn.close()

if __name__ == "__main__":
    tsa_server()
