#!/usr/bin/env python3
"""
Elliptic Curve CTF Challenge Analysis (椭圆曲线.py from task.zip)
================================================================

Problem Statement:
- Curve: y² = x³ + 3x + 27 (mod p)
- Point Q given as:
  x = 0xa61ae2f42348f8b84e4b8271ee8ce3f19d7760330ef6a5f6ec992430dccdc167
  y = 0x8a3ceb15b94ee7c6ce435147f31ca8028d1dd07a986711966980f7de20490080
- Find k such that Q = k * G for some generator G
- Flag format: ISCTF{MD5(hex(k))}

Analysis:
---------
1. Prime p derivation:
   Since p is not given, we derived it from: y² - x³ - 3x - 27 ≡ 0 (mod p)
   Factoring y² - x³ - 3x - 27 = -5 * 83 * 9907 * 2757375816847 * 106961300034120869 * p
   
2. Found prime p (647-bit):
   p = 349745548892267630513217405300372389049242377749180994181708157207037794536193406864637747598716507959563180409569310550017414871158929469506925586442211274717842740251523148075126041947482414153

3. Verified Q is on the curve y² = x³ + 3x + 27 (mod p) ✓

4. Curve properties analyzed:
   - Non-singular (discriminant = -316656 ≠ 0 mod p)
   - Non-anomalous (p*Q ≠ O, i.e., curve order ≠ p)
   - j-invariant = 186624/19791 ≈ 9.43 (not supersingular)
   - p+1 factors: 2 * 199 * 6495031 * 1071373465363 * (576-bit prime)

5. Attack attempts:
   - Smart's attack: Not applicable (curve not anomalous)
   - Pohlig-Hellman: Limited by large prime factor in order
   - MOV attack: Embedding degree analysis inconclusive
   - BSGS: k not found in range [1, 10000]

6. Open questions:
   - What is the intended generator G?
   - Is there additional problem context missing?
   - Could the problem be using a different prime p?

Note: This is an advanced ECDLP problem. The solution likely requires:
- SageMath for computing the exact curve order
- Or specific vulnerability not yet identified
- Or additional problem context (e.g., the generator point)
"""

from Crypto.Util.number import *
import hashlib

# Given point Q
x_Q = 0xa61ae2f42348f8b84e4b8271ee8ce3f19d7760330ef6a5f6ec992430dccdc167
y_Q = 0x8a3ceb15b94ee7c6ce435147f31ca8028d1dd07a986711966980f7de20490080

# Curve parameters
a = 3
b = 27

# Derived prime p
p = 349745548892267630513217405300372389049242377749180994181708157207037794536193406864637747598716507959563180409569310550017414871158929469506925586442211274717842740251523148075126041947482414153

# Verify point is on curve
def verify_point(x, y, a, b, p):
    return (y**2) % p == (x**3 + a*x + b) % p

print(f"Point Q verification: {verify_point(x_Q, y_Q, a, b, p)}")

# Helper functions for ECC operations
def modinv(a, m):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        return gcd, y1 - (b // a) * x1, x1
    g, x, _ = extended_gcd(a % m, m)
    return x % m if g == 1 else None

def point_add(P1, P2, a, p):
    if P1 is None: return P2
    if P2 is None: return P1
    x1, y1 = P1
    x2, y2 = P2
    if x1 == x2:
        if (y1 + y2) % p == 0:
            return None
        lam = ((3 * x1 * x1 + a) * modinv(2 * y1, p)) % p
    else:
        lam = ((y2 - y1) * modinv(x2 - x1, p)) % p
    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)

def point_mul(k, P, a, p):
    if k == 0:
        return None
    if k < 0:
        P = (P[0], (-P[1]) % p)
        k = -k
    result = None
    addend = P
    while k:
        if k & 1:
            result = point_add(result, addend, a, p)
        addend = point_add(addend, addend, a, p)
        k >>= 1
    return result

# Function to generate flag from k
def generate_flag(k):
    k_hex = hex(k)[2:]  # Remove '0x' prefix
    md5_hash = hashlib.md5(k_hex.encode()).hexdigest()
    return f"ISCTF{{{md5_hash}}}"

# If k is found, call generate_flag(k)
# Example: print(generate_flag(12345))

if __name__ == "__main__":
    print(f"Curve: y² = x³ + {a}x + {b} (mod p)")
    print(f"Prime p ({p.bit_length()} bits): {p}")
    print(f"Point Q: ({x_Q}, {y_Q})")
    print(f"\nTo solve: Find k such that Q = k * G for generator G")
    print(f"\nNote: Without knowing G or having a weak curve, this ECDLP")
    print(f"      cannot be solved with standard methods for such a large prime.")
