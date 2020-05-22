import string
import random


def generete_code():
    return ''.join(random.choice(string.digits) for _ in range(4))
