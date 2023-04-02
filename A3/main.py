import RSA
import time
import random
import hashlib 
import json
from typing import Dict, Any
import gmpy2
import datetime

class PKDA:
    res =[]
    def __init__(self):
        self.clients = {} # client ID -> public key
    # Define a function to generate nonces
    def generate_nonce(self):
        return random.randint(0, 2**32 - 1)

    # Define a function to get the current timestamp
    def get_timestamp(self):
        return int(time.time())

    def add_client(self, client_id, public_key):
        self.clients[client_id] = public_key
    
    def dict_hash(self,dictionary: Dict[str, Any]) -> str:
        """MD5 hash of a dictionary."""
        dhash = hashlib.md5()
        # We need to sort arguments so {'a': 1, 'b': 2} is
        # the same as {'b': 2, 'a': 1}
        encoded = json.dumps(dictionary, sort_keys=True).encode()
        dhash.update(encoded)
        return dhash.digest()

    
    def generate_pkda_keys(self):
        print('\n')
        print("Enter pkda's keys : ")
        pkda_public, pkda_private  = RSA.generate_keypair(1)
        pkda.res.append(pkda_public)
        pkda.res.append(pkda_private) 
        return pkda.res

    def get_public_key(self, client_id):
        if client_id in self.clients:
            return self.clients[client_id]
        else:
            return None
        
    def get_request(self):
        pass 
    def Calculate_Signature(self,hash_response):
        r =[]
        for c in hash_response:
            r.append(c)
        signature = [gmpy2.powmod((c), pkda.res[1][0], pkda.res[1][1]) for c in r]
        return signature
    def encrypt(self,value,key):
        res=[]
        if(key == 'type' or key=='sender' or key=='receiver' or key=='client_id' or key=='timeStamp'):
            test_list = [value]
            r = [ord(ele) for sub in test_list for ele in sub]
            for i in range(0,len(r)):
                res.append(((r[i])**pkda.res[1][0]) % pkda.res[1][1])
            return res
        else:
            res2=""
            if(key=='nonce' or key=='encrypted_public_key'):
                res2+=str((value**pkda.res[1][0]) % pkda.res[1][1])
                return res2
            else:
                return value
    def encrypt_response(self,response):
        for i in response:
            temp = pkda.encrypt(response[i],i)
            response[i]  = temp
        return response
    def handle_request(self, request):
        if request['type'] == 'public_key_request':
            client_id = request['client_id']
            duration = request['duration']
            public_key = self.get_public_key(client_id)
            nonce = request['nonce']
            time_stamp = request['timeStamp']
            if public_key:
                encrypted_key = self.encrypt_with_private_key(public_key)
                response = {
                    'type': 'public_key_response',
                    'sender': 'pkda',
                    'receiver': request['sender'],
                    'client_id': client_id,
                    'nonce': nonce,
                    'timeStamp' : time_stamp,
                    'duration' : duration,
                    'encrypted_public_key': public_key,
                    'signature':'',
                    'hash':''
                }
                encrypted_response_using_private_key = pkda.encrypt_response(response)
                # res+=str(response)
                # print("Dictionary Converted to string :",res)
                hash_response = pkda.dict_hash(response)
                signature = pkda.Calculate_Signature(hash_response)
                print("Hash of the response ...... :","  ",hash_response)
                response['signature'] = signature
                response['hash'] = hash_response
                return encrypted_response_using_private_key
        return None
    
    def encrypt_with_private_key(self, alice_public):
        # private_key = RSA.generate(2048)
        encrypted_key= ((alice_public**pkda.res[1][0]) % pkda.res[1][1])
        return encrypted_key
        # encrypted = private_key.encrypt(data, 32)[0]
        # return encrypted
    def get_own_certificate_from_pkda(self,client_id,own_public_key):
        time_stamp = str(datetime.datetime.now())[:19]
        duration = list(time_stamp)
        duration[14] = str(int(duration[14]) + 2)
        duration = ''.join(duration)
        print("Duration :" ,duration)
        # time_val = datetime.datetime.now()
        print("Time :",(str(time_stamp)))
        response = {
            'type': 'public_key_response',
            'sender': 'pkda',
            'client_id': client_id,
            'timeStamp' : time_stamp,
            'duration' : duration,
            'own_public_key': own_public_key,
            'signature':'',
            'hash':''
        }
        hash_response = pkda.dict_hash(response)
        signature = pkda.Calculate_Signature(hash_response)
        print("Hash of the response ...... :","  ",hash_response)
        response['signature'] = signature
        response['hash'] = hash_response
        return response


class Client:

    def __init__(self, client_id):
        self.client_id = client_id
        # self.keypair = RSA.generate(2048)
    
    def get_public_key(self):
        return self.keypair.publickey().export_key()
    
    # def set_other_public_key(self, other_public_key):
    #     print("other_public_key :"," ",other_public_key)
    #     self.other_public_key = RSA.import_key(other_public_key)

    def decrypt_public_key(self,key):
        decrypted_key= ((key**pkda.res[0][0]) % pkda.res[0][1])
        return decrypted_key
    
    def decrypt(self,value,key):
        if(key == 'type' or key=='sender' or key=='receiver' or key=='client_id'or key=='timeStamp'):
            res=[]
            for i in range(0,len(value)):
                res.append(((value[i])**pkda.res[0][0]) % pkda.res[0][1])
            r = ""
            for val in res:
                r = r+ chr(val)
            return r
        else:
            
            if(key=='nonce' or key=='encrypted_public_key'):
                res2= ((int(value)**pkda.res[0][0]) % pkda.res[0][1])
                return res2
            else:
                return value
    def Verify_response(self,response):
        name =''
        if(response['sender']=='Alice'):
            name = 'Alice'
        else:
            name='Bob'
        if(name=='Alice'):
            for i in response:
                temp = alice.decrypt(response[i],i)
                response[i]  = temp
            return response
        elif(name=='Bob'):
            for i in response:
                temp = bob.decrypt(response[i],i)
                response[i]  = temp
            return response
    def Verify_Signature(self,r):

        time_val = str(datetime.datetime.now())[:19]
        signature =r['signature']
        
        decrypt_sig  = [str(x) for x in signature]

        # print(decrypt_sig)
        res = [int(x) for x in decrypt_sig]
        plain = [gmpy2.powmod((k), pkda.res[0][0], pkda.res[0][1]) for k in res]
        res2 = [int(x) for x in plain]
        # print("Plain Number :",res2)
        decrypted_Signature = bytes(res2)
        print('\n')
        print("Hash of the Decrypted Signature :",decrypted_Signature)
        if(r['hash'] == decrypted_Signature and r['duration'] >time_val):
            return True
        else:
            return False

    def send_request_to_pkda(self, pkda, other_client_id):
        nonce = random.randint(0, 2**32 - 1)
        # time_val = int(time.time())
        time_val = str(datetime.datetime.now())[:19]
        duration = list(time_val)
        duration[14] = str(int(duration[14]) + 2)
        duration = ''.join(duration)
        print("Duration :" ,duration)
        # time_val = datetime.datetime.now()
        print("Time :",(str(time_val)))

        request = {
            'type': 'public_key_request',
            'sender': self.client_id,
            'receiver': 'pkda',
            'client_id': other_client_id,
            'nonce': nonce,
            'timeStamp':time_val,
            'duration':duration
        }
        ans_from_pkda = pkda.handle_request(request)
        return ans_from_pkda
        # if response and response['type'] == 'public_key_response' and response['nonce'] == nonce:
        #     public_key = self.keypair.decrypt(response['public_key'])
        #     pkda.add_client(other_client_id, public_key)
    
    def encrypt_request(self,value,key,other_Client_public_key):
        res=[]
        if(key == 'type' or key=='sender' or key=='receiver' or key=='client_id'):
            test_list = [value]
            r = [ord(ele) for sub in test_list for ele in sub]
            for i in range(0,len(r)):
                res.append(((r[i])**other_Client_public_key) % Bob_public[1])
            return res
        else:
            res2=""
            if(key=='nonce'):
                res2+=str((value**other_Client_public_key) % Bob_public[1])
                return res2
            else:
                return value
    def encrypt_client_request(self,request,other_Client_public_key):

        for i in request:
            temp = alice.encrypt_request(request[i],i,other_Client_public_key)
            request[i]  = temp
        return request
    
    def send_request_to_otherClient(self,other_Client_public_key,other_client_id,nonce1):
        
        request = {
            'type': 'request_to_other_client',
            'sender': self.client_id,
            'receiver': 'Bob',
            'client_id': other_client_id,
            'nonce': nonce1,
        }
        encrypted_request = alice.encrypt_client_request(request,other_Client_public_key)
        return encrypted_request
    def encrypt_request_for_nonces(self,value,key,other_Client_public_key):
        res=[]
        if(key == 'type' or key=='sender' or key=='receiver' or key=='client_id'):
            test_list = [value]
            r = [ord(ele) for sub in test_list for ele in sub]
            for i in range(0,len(r)):
                res.append(((r[i])**other_Client_public_key) % alice_public[1])
            return res
        else:
            res2=""
            if(key=='nonce1' or key=='nonce2'):
                res2+=str((value**other_Client_public_key) % alice_public[1])
                return res2
            else:
                return value
    def encrypt_nonces(self, request2,other_Client_public_key):
        for i in request2:
            temp = bob.encrypt_request_for_nonces(request2[i],i,other_Client_public_key)
            request2[i]  = temp
        return request2
    def send_Message_to_Alice(self,other_Client_public_key,other_client_id,nonce1,nonce2):
        
        request_2 = {
            'type': 'request_to_other_client',
            'sender': self.client_id,
            'receiver': 'Alice',
            'client_id': other_client_id,
            'nonce1': nonce1,
            'nonce2': nonce2,
        }
        encrypted_request_from_Bob_to_Alice = bob.encrypt_nonces(request_2,other_Client_public_key)
        return encrypted_request_from_Bob_to_Alice
    def send_Message_to_Bob(self,other_Client_public_key,other_client_id,nonce2):
        request_3 = {
            'type': 'request_to_other_client',
            'sender': self.client_id,
            'receiver': 'Bob',
            'client_id': other_client_id,
            'nonce2': nonce2,
        }
        establishment_of_Connection_confirmation = alice.encrypt_nonces(request_3, other_Client_public_key)
        return establishment_of_Connection_confirmation

if __name__=="__main__":

    print("Enter Alice Keys")
    alice_public,alice_private = RSA.generate_keypair(1)
    print("Alice Public Keys:",alice_public)
    print("Alice Private Keys:",alice_private)
    print('\n')

    print("Enter Bob's Keys")
    Bob_public,Bob_private = RSA.generate_keypair(1)
    print("Bob's Public Keys:",Bob_public)
    print("Bob's Private Keys:",Bob_private)

    pkda = PKDA()
    pkda.add_client('Alice',alice_public[0])
    pkda.add_client('Bob', Bob_public[0])
    pkda.generate_pkda_keys()

    alice = Client('Alice')
    bob = Client('Bob')
    print('\n')
    print("Alice own Public-Key Ceritficate",pkda.get_own_certificate_from_pkda('Alice',alice_public[0]))
    print('\n')
    print("Bob own Public-Key Ceritficate",pkda.get_own_certificate_from_pkda('Bob',Bob_public[0]))
    print('\n')
    print("***********************************************************************************"
          "************************************************************")

    
   
    print("Step 1 : Alice Request to PKDA for Bob's public key")
    r = alice.send_request_to_pkda(pkda,'Bob')
    print('\n')
    print("Step 2 :Encrypted Response From PKDA using his private Key to Alice.........", r,end ='\n')
    Verify_Encrypted_response = alice.Verify_response(r)
    print('\n')
    print("Decrypted Response By Alice using public  Key of pkda.........")
    print(Verify_Encrypted_response)
    print('\n')
    print("Verify Signature By Alice.........")
    verify = alice.Verify_Signature(r)
    if(verify ==True):
        print("Verfied, Not tampering in the message")
    else:
        print("Response from PKDA has been tampererd")

    print('\n')
    # request = pkda.encrypt_with_private_key(Bob_public[0])

    # print("Encrypted Public key of Bob's by PKDA private Key", request)

    decrypt1 = (Verify_Encrypted_response['encrypted_public_key'])
    print("Decrypted Public Key of Bob's :",decrypt1)
    print('\n')

    print("***********************************************************************************"
            "************************************************************")
    print('\n')

    print('Step 3: Alice Sends to Bob the  Messaage of establishing connection by encrypting Nonce and his client id using Bob public Key after getting from pkda...')
    
    nonce1 = random.randint(0, 2**32 - 1)
    request = alice.send_request_to_otherClient(decrypt1,'Bob',nonce1)

    print("Encrypted request from Alice to Bob :",request)


    print('\n')
    print("***********************************************************************************"
          "************************************************************")

    print('\n')
    print("Step 4 :Now Bob Request to PKDA for Alice's public key")
    r2 = bob.send_request_to_pkda(pkda,'Alice')
    print("Encrypted Response From PKDA using his private Key to Bob.........", r2,end ='\n')
    Verify_Encrypted_response_2 = bob.Verify_response(r2)
    print('\n')
    print("Decrypted Response By Bob using public Keys of pkda.........")
    print(Verify_Encrypted_response_2)
    print('\n')

    print("Verify Signature By Bob.........")
    verify = bob.Verify_Signature(Verify_Encrypted_response_2)
    if(verify ==True):
        print("Verfied, Not tampering in the message")
    else:
        print("Response from PKDA has been tampererd")


    print('\n')
    decrypt2 =(Verify_Encrypted_response_2['encrypted_public_key'])
    print("Decrypted Public Key of Alice's :",decrypt2)

    print("***********************************************************************************"
          "************************************************************")
    print('\n')
    
    print("Step 5 : After Receiving Public Key of Alice from PKDA, Now Bob will send the nonce N1 and N2 for confirming the establishment" 
          "of connection by encrypting nonces using public key of Alice.")
    print('\n')

    nonce2 = random.randint(0, 2**32 - 1)
    encrypted_request_from_Bob =  bob.send_Message_to_Alice(decrypt2,'Alice',nonce1,nonce2)

    print("Encrypted Request from Bob to Alice for establishment of connection :" , encrypted_request_from_Bob)

    print('\n')
    print("***********************************************************************************"
          "************************************************************")
    print('\n')

    print("Step 6 : After Alice received the nonces , he replies back with Nonce 2 which confirms establishment of connection and now to have further communication")

    encrypted_request_from_Alice_Nonce_2 = alice.send_Message_to_Bob(decrypt1,'Bob',nonce2)

    print("Esatablsihment of connection after Alice sends nonce 2")
    print(encrypted_request_from_Alice_Nonce_2)
    
    print('\n')
    print("***********************************************************************************"
          "************************************************************")


    
    print('\n')
    print(" Step 7: Now after establishment of connection ,Alice Send Message to Bob by using Bob's public key to encrypt the Message :")
    M1 = ['Hi1']
    G1 = ['Got-it1']
    # for i in range(0,3):
    res = [ord(ele) for sub in M1 for ele in sub]
    # print(res)
    print('\n')
    print("Sending the Message to Bob using Bob's public key to encrypt....")
    print("Message to be sent : ",M1[0])
    encrypted_M=[]
    decrypted_M=[]
    for i in range(0,len(res)):
        encrypted_M.append(((res[i]**decrypt1) % Bob_public[1]))
    print("Normal Message in ascii",res)
    print("Encrypted Message in acii ",encrypted_M)
    print('\n')
    print("Bob's Decrytps the Message using his private Key :")
    for i in range(0,len(encrypted_M)):
        decrypted_M.append(((encrypted_M[i]**Bob_private[0]) % Bob_public[1]))
    print("Decrypted Message in ascii",decrypted_M)
    recived_Message = ""
    for val in decrypted_M:
        recived_Message+=chr(val)
    print("Decrypted Message :" ,recived_Message)

    print("Bob will respond to Alice that he recieved the Message.")
    print("Bob send message to Alice using public key of Alice to encrypt.")

    res2 = [ord(ele) for sub in G1 for ele in sub]
    print("Sending the Message to Alice ....")
    print("Message to be sent : ",G1)
    encrypted_M=[]
    decrypted_M=[]
    for i in range(0,len(res2)):
        encrypted_M.append(((res2[i]**decrypt2) % alice_public[1]))
    print("Normal Message in ascii",res2)
    print("Encrypted Message ",encrypted_M)
    print('\n')
    print("Alice's Decrytps the Message using his private Key :")
    for i in range(0,len(encrypted_M)):
        decrypted_M.append(((encrypted_M[i]**alice_private[0]) % alice_public[1]))
    print("Decrypted Message in ascii",decrypted_M)
    recived_Message = ""
    for val in decrypted_M:
        recived_Message+=chr(val)
    print("Decrypted Message :" ,recived_Message)

    print('\n')
    print("***********************************************************************************"
          "************************************************************")

    print(" Similarly Alice Send 2nd Message to Bob by using  Bob's public Key to encrypt the Message :")
    M1 = ['Hi2']
    G1 = ['Got-it2']
    # for i in range(0,3):
    res = [ord(ele) for sub in M1 for ele in sub]
    # print(res)
    print('\n')
    print("Sending the Message to Bob using Bob's public key....")
    print("Message to be sent : ",M1[0])
    encrypted_M=[]
    decrypted_M=[]
    for i in range(0,len(res)):
        encrypted_M.append(((res[i]**decrypt1) % Bob_public[1]))
    print("Normal Message in ascii",res)
    print("Encrypted Message in acii ",encrypted_M)
    print('\n')
    print("Bob's Decrytps the Message using his private Key :")
    for i in range(0,len(encrypted_M)):
        decrypted_M.append(((encrypted_M[i]**Bob_private[0]) % Bob_public[1]))
    print("Decrypted Message in ascii",decrypted_M)
    recived_Message = ""
    for val in decrypted_M:
        recived_Message+=chr(val)
    print("Decrypted Message :" ,recived_Message)

    print("Bob will respond to Alice that he recieved the Message.")
    print("Bob send message to Alice using Alice public key to encrypt.")

    res2 = [ord(ele) for sub in G1 for ele in sub]
    print("Sending the Message to Alice....")
    print("Message to be sent : ",G1)
    encrypted_M=[]
    decrypted_M=[]
    for i in range(0,len(res2)):
        encrypted_M.append(((res2[i]**decrypt2) % alice_public[1]))
    print("Normal Message in ascii",res2)
    print("Encrypted Message ",encrypted_M)
    print('\n')
    print("Alice's Decrytps the Message using his private Key :")
    for i in range(0,len(encrypted_M)):
        decrypted_M.append(((encrypted_M[i]**alice_private[0]) % alice_public[1]))
    print("Decrypted Message in ascii",decrypted_M)
    recived_Message = ""
    for val in decrypted_M:
        recived_Message+=chr(val)
    print("Decrypted Message :" ,recived_Message)

    print('\n')
    print("***********************************************************************************"
          "************************************************************")

    print(" Similarly Alice Send 3rd Message to Bob by using Bob's public Key to encrypt the Message :")
    M1 = ['Hi3']
    G1 = ['Got-it3']
    # for i in range(0,3):
    res = [ord(ele) for sub in M1 for ele in sub]
    # print(res)
    print('\n')
    print("Sending the Message to Bob....")
    print("Message to be sent : ",M1[0])
    encrypted_M=[]
    decrypted_M=[]
    for i in range(0,len(res)):
        encrypted_M.append(((res[i]**decrypt1) % Bob_public[1]))
    print("Normal Message in ascii",res)
    print("Encrypted Message in acii ",encrypted_M)
    print('\n')
    print("Bob's Decrytps the Message using his private Key :")
    for i in range(0,len(encrypted_M)):
        decrypted_M.append(((encrypted_M[i]**Bob_private[0]) % Bob_public[1]))
    print("Decrypted Message in ascii",decrypted_M)
    recived_Message = ""
    for val in decrypted_M:
        recived_Message+=chr(val)
    print("Decrypted Message :" ,recived_Message)

    print("Bob will respond to Alice that he recieved the Message.")
    print("Bob send message to Alice using Alice public key to encrypt.")

    res2 = [ord(ele) for sub in G1 for ele in sub]
    print("Sending the Message to Alice....")
    print("Message to be sent : ",G1)
    encrypted_M=[]
    decrypted_M=[]
    for i in range(0,len(res2)):
        encrypted_M.append(((res2[i]**decrypt2) % alice_public[1]))
    print("Normal Message in ascii",res2)
    print("Encrypted Message ",encrypted_M)
    print('\n')
    print("Alice's Decrytps the Message using his private Key :")
    for i in range(0,len(encrypted_M)):
        decrypted_M.append(((encrypted_M[i]**alice_private[0]) % alice_public[1]))
    print("Decrypted Message in ascii",decrypted_M)
    recived_Message = ""
    for val in decrypted_M:
        recived_Message+=chr(val)
    print("Decrypted Message :" ,recived_Message)
    

