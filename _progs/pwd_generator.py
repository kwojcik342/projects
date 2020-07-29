import random
import sys
import string


def generate_pwd_mine(pwd_len):
    int_num = random.randint(1, pwd_len - 1)
    char_num = pwd_len - int_num
    pwd = ""

    for i in range(pwd_len):
        char_or_int = random.randint(1, 2)  # 1 - char / 2 - int
        if (char_or_int == 1 and char_num > 0) or (char_or_int == 2 and int_num == 0):
            if random.randint(1, 2) == 1:
                pwd += chr(random.randint(65, 90))
            else:
                pwd += chr(random.randint(97, 122))
            char_num -= 1
        elif (char_or_int == 2 and int_num > 0) or (char_or_int == 1 and char_num == 0):
            pwd += str(random.randint(0, 9))
            int_num -= 1

    return pwd


def generate_pwd_sample(pwd_len=5, chars=string.ascii_letters + string.digits + string.punctuation):
    return "".join(random.choice(chars) for i in range(pwd_len))


try:
    pwd_length = int(input("podaj ilość znaków w haśle (minimum 5): "))
except ValueError:
    print("nie podałeś liczby")
    sys.exit(-1)

if pwd_length < 5:
    pwd_length = 5


print("Twoje hasło: " + generate_pwd_mine(pwd_length))
print("Twoje hasło: " + generate_pwd_sample(pwd_length))
