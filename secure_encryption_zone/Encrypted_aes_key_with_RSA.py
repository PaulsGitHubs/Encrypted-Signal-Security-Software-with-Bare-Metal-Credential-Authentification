from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import base64

key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

with open("private_key.pem", "wb") as prv_key_file:
    prv_key_file.write(private_key)

with open("public_key.pem", "wb") as pub_key_file:
    pub_key_file.write(public_key)

print("Private and Public keys generated successfully!")

# 1. Generate a random AES key
aes_key = get_random_bytes(32)  # AES-256

# 2. Encrypt the AES key using the RSA public key
with open("public_key.pem", "rb") as pub_key_file:
    public_key = RSA.import_key(pub_key_file.read())
    cipher_rsa = PKCS1_OAEP.new(public_key)
    enc_aes_key = cipher_rsa.encrypt(aes_key)

# 3. Save the encrypted AES key to a file
with open("encrypted_aes_key.pem", "wb") as enc_aes_key_file:
    enc_aes_key_file.write(enc_aes_key)

print("Encrypted AES key saved successfully!")
