import hashlib
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

#------------------------------------------------------------------------
# Merkle fa létrehozása a tranzakciók listája alapján
def build_merkle_tree(transactions):
    if len(transactions) == 0: # Ha nincs tranzakció egy üres listát ad vissza
        return []
    if len(transactions) == 1: # Ha van akkor a hash-ét
        return [hashlib.sha256(transactions[0].encode()).hexdigest()]

    new_transactions = [] # Tranzakciók kombinálása a Merkle fa következő rétegének létrehozásához
    for i in range(0, len(transactions), 2):
        if i + 1 < len(transactions):
            combined = transactions[i] + transactions[i + 1]
        else:
            combined = transactions[i]
        new_transactions.append(hashlib.sha256(combined.encode()).hexdigest())

    return build_merkle_tree(new_transactions) # Felépíti a Merkle fát az új réteggel
#------------------------------------------------------------------------
# Osztály, amely egy blokkot jelöl a blokkláncban
class Block:
    def __init__(self, index, previous_hash, timestamp, merkle_root, nonce, data, hash, signature):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.merkle_root = merkle_root
        self.nonce = nonce
        self.data = data
        self.hash = hash
        self.signature = signature
#------------------------------------------------------------------------
#SHA-256 kiszámítása
def calculate_hash(index, previous_hash, timestamp, merkle_root, nonce, data):
    #Konkatenálás 1 stringgé
    value = str(index) + str(previous_hash) + str(timestamp) + str(merkle_root) + str(nonce) + str(data)
    return hashlib.sha256(value.encode()).hexdigest() #Visszaadja a konkatenált string SHA-256 hash-ét
#------------------------------------------------------------------------
#Genesis blokk létrehozása és visszaadása, ez a blokklánc első blokkja
def create_genesis_block():
    return Block(0, "0", int(time.time()), "", 0, "Genesis Block",
                 calculate_hash(0, "0", int(time.time()), "", 0, "Genesis Block"), b"")
#------------------------------------------------------------------------
#Új blokk létrehozása az előző és a megadott alapján
def create_new_block(previous_block, data, private_key):
    index = previous_block.index + 1
    timestamp = int(time.time())
    merkle_tree = build_merkle_tree(data)
    merkle_root = merkle_tree[-1] if merkle_tree else ""
    nonce = 0
    while True:
        nonce += 1
        hash_attempt = calculate_hash(index, previous_block.hash, timestamp, merkle_root, nonce, data)
        if hash_attempt.startswith("0000") or hash_attempt.startswith("00000"):
            break

    #Aláírás létrehozása a blokk hash-hez
    signature = private_key.sign(
        str(hash_attempt).encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    #Visszaadja az új blokkot attribútjaival
    return Block(index, previous_block.hash, timestamp, merkle_root, nonce, data, hash_attempt, signature)
#------------------------------------------------------------------------
#Privát és publikus kulcsok generálása a blokkok aláírásához
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key() #Public kulcs megszerzése a privát kulcsból
#------------------------------------------------------------------------
#Ellenőrzi, hogy a kulcsok létrejöttek-e
if private_key and public_key:
    #Inicializálja a blokkláncot a genesis blokkal
    blockchain = [create_genesis_block()]
    previous_block = blockchain[0] #Az előző blokk beállítása genesis blokkra

    num_blocks_to_add = 3 #A blokkok száma amit hozzáad a blokklánchoz
    transactions = [] #Lista, hogy a tranzakciók megmaradjanak

    for i in range(num_blocks_to_add):
        #Új tranzakció létrehozása
        new_data = [f"Transaction #{i + 1} - Sender: Alice, Recipient: Bob, Amount: 10 BTC"]
        transactions.extend(new_data) #Az új tranzakció hozzáadása a listához
        new_block = create_new_block(previous_block, new_data, private_key) #Új blokk létrehozása
        blockchain.append(new_block) #Új blokk hozzáadása a blokklánchoz
        previous_block = new_block #Előző blokk frissítése
        print(f"Block #{new_block.index} added to the blockchain.")
        print(f"Hash: {new_block.hash}")
        print(f"Signature: {new_block.signature.hex()}\n")

    print("Blockchain verification:")
    for block in blockchain:
        print(f"Block #{block.index}")
        print(f"Hash: {block.hash}")
        print(f"Previous hash: {block.previous_hash}")
        print(f"Merkle root: {block.merkle_root}")
        print(f"Nonce: {block.nonce}")
        print(f"Transactions: {block.data}")
        print(f"Signature: {block.signature.hex()}\n")
else:
    print("Error: Keys are not generated.")
