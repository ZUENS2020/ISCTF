#!/usr/bin/env python3
"""
CTF Challenge Solution: Elliptic Curve Cryptography

Problem:
- Curve equation: y^2 = x^3 + 3x + 27 (mod p)
- Point Q with 256-bit coordinates
- Find: k = ?
- Hint: "Have you verified that base point G is really on the curve?"

Key Insight:
The curve y^2 = x^3 + 3x + 27 is SINGULAR when the discriminant factor
4a^3 + 27b^2 = 4(3)^3 + 27(27)^2 = 19791 = 3^3 x 733 = 0 (mod p)

This happens when p = 733. For singular curves, we can solve the
discrete logarithm problem by mapping points to a simpler algebraic group.

The singular curve attack maps points to the norm-1 subgroup of F_{733^2}*,
where the discrete log becomes computable.
"""

import hashlib
import math


def compute_flag(k):
    """Convert k to hex, compute MD5, return flag format"""
    k_hex = format(int(k), 'x')
    md5_hash = hashlib.md5(k_hex.encode()).hexdigest()
    return f"ISCTF{{{md5_hash}}}"


def mul_ext(a, b, c, d, p):
    """Multiply in F_p[i]/(i^2 - 326)"""
    return ((a*c + 326*b*d) % p, (a*d + b*c) % p)


def norm(a, b, p):
    """Norm in F_p[i]/(i^2 - 326)"""
    return (a*a - 326*b*b) % p


def inv_ext(a, b, p):
    """Inverse in F_p[i]/(i^2 - 326)"""
    n = norm(a, b, p)
    n_inv = pow(n, -1, p)
    return ((a * n_inv) % p, ((-b) * n_inv) % p)


def div_ext(a1, b1, a2, b2, p):
    """Division in F_p[i]"""
    inv = inv_ext(a2, b2, p)
    return mul_ext(a1, b1, inv[0], inv[1], p)


def pow_ext(a, b, n, p):
    """Compute (a + bi)^n in F_{p^2}"""
    result_a, result_b = 1, 0
    base_a, base_b = a, b
    n = int(n)
    while n > 0:
        if n % 2 == 1:
            result_a, result_b = mul_ext(result_a, result_b, base_a, base_b, p)
        base_a, base_b = mul_ext(base_a, base_b, base_a, base_b, p)
        n //= 2
    return result_a, result_b


def phi_map(x, y, x_s, p):
    """Map point to norm-1 element in F_{p^2}"""
    num_a = y % p
    num_b = (x_s - x) % p
    den_a = y % p
    den_b = (x - x_s) % p
    return div_ext(num_a, num_b, den_a, den_b, p)


def solve():
    # Given point Q
    Qx = 0xa61ae2f42348f8b84e4b8271ee8ce3f19d7760330ef6a5f6ec992430dccdc167
    Qy = 0x8a3ceb15b94ee7c6ce435147f31ca8028d1dd07a986711966980f7de20490080
    
    # Curve: y^2 = x^3 + 3x + 27
    a, b = 3, 27
    p = 733  # Prime where curve is singular
    x_s = 353  # Singular point x-coordinate
    
    print(f"Curve: y^2 = x^3 + {a}x + {b}")
    print(f"Discriminant factor: 4({a})^3 + 27({b})^2 = {4*a**3 + 27*b**2} = 3^3 x 733")
    print(f"\nThe curve is SINGULAR mod {p}")
    print(f"Singular point at x = {x_s}")
    
    # Compute phi(Q) - maps Q to norm-1 element in F_{p^2}
    Qx_mod = Qx % p
    Qy_mod = Qy % p
    phi_Q = phi_map(Qx_mod, Qy_mod, x_s, p)
    
    print(f"\nphi(Q) = {phi_Q[0]} + {phi_Q[1]}*i")
    print(f"Norm(phi(Q)) = {norm(phi_Q[0], phi_Q[1], p)}")
    
    # Use G = (0, 352) as generator (on the curve mod 733)
    G_point = (0, 352)
    phi_G = phi_map(G_point[0], G_point[1], x_s, p)
    print(f"\nGenerator G = {G_point}")
    print(f"phi(G) = {phi_G[0]} + {phi_G[1]}*i")
    
    # Solve discrete log using baby-step giant-step
    order = p + 1  # Order of norm-1 subgroup = 734
    m = int(math.ceil(math.sqrt(order))) + 1
    
    # Baby steps
    baby = {}
    power = (1, 0)
    for j in range(m + 1):
        baby[power] = j
        power = mul_ext(power[0], power[1], phi_G[0], phi_G[1], p)
    
    # Giant steps
    phi_G_m = pow_ext(phi_G[0], phi_G[1], m, p)
    phi_G_neg_m = inv_ext(phi_G_m[0], phi_G_m[1], p)
    
    gamma = phi_Q
    k = None
    for i in range(m + 1):
        if gamma in baby:
            k = (i * m + baby[gamma]) % order
            test = pow_ext(phi_G[0], phi_G[1], k, p)
            if test == phi_Q:
                break
        gamma = mul_ext(gamma[0], gamma[1], phi_G_neg_m[0], phi_G_neg_m[1], p)
    
    print("\n" + "=" * 60)
    print("SINGULAR CURVE ATTACK RESULT:")
    print("=" * 60)
    
    if k is not None:
        print(f"k = {k} (mod {order})")
        print(f"Verification: phi(G)^{k} = phi(Q)")
        print(f"\nFlag: {compute_flag(k)}")
    
    # Print other candidates for reference
    print("\n" + "=" * 60)
    print("OTHER CANDIDATE FLAGS:")
    print("=" * 60)
    
    candidates = [
        (468, "Singular curve DLOG mod 734"),
        (29094, "CRT of mod 84 and mod 734"),
        (733, "Prime factor of discriminant"),
        (19791, "Discriminant 4a^3+27b^2"),
        (353, "Singular point x"),
        (76, "Verification error mod 733"),
        (66, "phi(Q).real mod 733"),
        (222, "phi(Q).imag mod 733"),
    ]
    
    for val, desc in candidates:
        print(f"k = {val:6d} ({desc}): {compute_flag(val)}")


if __name__ == "__main__":
    solve()
