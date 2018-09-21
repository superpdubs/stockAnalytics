import random

    class Verfication:

        def generate_code(self):
            num = random.randint(100,999)
            cap1 = chr(random.randint(65,90))
            cap2 = chr(random.randint(65,90))
            low = chr(random.randint(97,122))
            vercode = cap1 + str(num) + cap2 + low
            return vercode