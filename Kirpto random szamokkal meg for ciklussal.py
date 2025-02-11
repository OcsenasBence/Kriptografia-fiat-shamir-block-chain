import random
from sympy import nextprime

def generate_random_prime(bit_length):
    random_number = random.getrandbits(bit_length)
    return nextprime(random_number)

# A protokoll inicializálása.
# Generál két prím számot, p-t és q-t, majd ezek szorzatából számítja az n értéket.
def setup():
    bit_length = 3
    p = generate_random_prime(bit_length)
    q = generate_random_prime(bit_length)
    n = p * q
    x_values = [random.randint(1, n - 1) for _ in range(5)]  # Generate multiple x values
    y_squared_values = [(x ** 2) % n for x in x_values]

    print(f"Setup:\n  p = {p}, q = {q}, n = {n}")
    for i, (x, y_squared) in enumerate(zip(x_values, y_squared_values)):
        print(f"  x[{i}] = {x}, y^2[{i}] = {y_squared}")

    return n, x_values, y_squared_values

# Egy véletlen értéket, r-t generál a prover részéről, és kiszámítja a t-t.
# Kiírja r és t értékét, valamint visszaadja ezeket.
def prover(n):
    r = random.randint(1, n - 1)
    t = (r ** 2) % n
    print(f"Prover:\n  r = {r}, t = {t}")
    return t, r

# Kiírja a kihívást és visszaadja annak értékét.
def verifier():
    c = random.randint(0, 1)
    print(f"Verifier:\n  Challenge c = {c}")
    return c

# Kiírja és visszaadja a válaszként kiszámított s értéket.
def prover_response(r, x, c, n):
    s = (r * (x ** c)) % n
    print(f"Prover Response:\n  s = {s}")
    return s

# Az ellenőrző igazolja, hogy a kapott válasz helyes-e.
# Kiírja az egyenlet bal (LHS) és jobb (RHS) oldalát,
# majd visszatér a hitelességi ellenőrzés eredményével (True vagy False).
def verifier_verification(s, t, y_squared, c, n):
    lhs = (s ** 2) % n
    rhs = (t * (y_squared ** c)) % n
    print(f"Verifier Verification:\n  LHS = {lhs}, RHS = {rhs}")
    return lhs == rhs

# Összekapcsolja az egyes lépéseket, és végrehajtja a protokollt.
def main():
    n, x_values, y_squared_values = setup()
    for i, (x, y_squared) in enumerate(zip(x_values, y_squared_values)):
        print(f"\nProtocol iteration for x[{i}] and y^2[{i}]\n")
        for _ in range(5):  # Repeat the protocol 5 times for each x value
            t, r = prover(n)
            c = verifier()
            s = prover_response(r, x, c, n)
            verification_result = verifier_verification(s, t, y_squared, c, n)
            if not verification_result:
                print("Verification failed: The prover does not know 'x'.")
                return
    print("Verification successful: The prover knows all 'x' values.")

# Ha a protokoll helyes, akkor The prover knows 'x'-et ad vissza.
# Ha a protokoll hibát tartalmaz akkor The prover does not know 'x'-et ad vissza.
if __name__ == "__main__":
    main()