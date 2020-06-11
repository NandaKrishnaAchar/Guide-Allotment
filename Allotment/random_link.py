import random
import string
import math

def randomlink(n):
    ran=random.randrange(8, 13)
    random.seed(n)
    lettersAndDigits = string.ascii_letters + string.digits
    password=''.join(random.choice(lettersAndDigits) for i in range(ran))
    passwordList = list(password)
    random.SystemRandom().shuffle(passwordList)
    password = ''.join(passwordList)
    return password
#print(randomlink(9508))
