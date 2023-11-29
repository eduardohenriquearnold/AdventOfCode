def getNloop(key, subject_number, rem=20201227):
    """Given a public key, obtains number of loops by brute-force"""

    Nmax = 10**8
    v = 1
    for i in range(Nmax):
        v = v * subject_number
        v = v % rem
        if v == key:
            return i + 1

    return None


def encrypt(subject_number, N, rem=20201227):
    """Encrypt a value using key and subject"""

    v = 1
    for _ in range(N):
        v = v * subject_number
        v = v % rem
    return v


# Inputs
pk1 = 11349501
pk2 = 5107328

# Get N loops from each public key and compute encryption key
n1 = getNloop(pk1, 7)
n2 = getNloop(pk2, 7)
key = encrypt(pk2, n1)
assert encrypt(pk2, n1) == encrypt(pk1, n2)

print(f"P1: key {key}")
