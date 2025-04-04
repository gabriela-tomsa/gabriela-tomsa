import hashlib
import time

target_hash = "0e000d61c1735636f56154f30046be93b3d71f1abbac3cd9e3f80093fdb357ad"

def get_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

upper_case = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lower_case = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'
special_chars = '!@#$'

recursion_count = 0

def backtrack(password, upper, lower, digit, special):
    global recursion_count
    recursion_count += 1

    # Am eliminat afișarea progresului
    # if recursion_count % 100000 == 0:
    #     print(f"Apeluri recursive: {recursion_count}, Parola partiala: {password}")

    if len(password) == 6:
        if upper == 1 and lower == 3 and digit == 1 and special == 1:
            candidate_hash = get_hash(password)
            if candidate_hash == target_hash:
                print(f"Parola găsită: {password}")
                print(f"Număr apeluri recursive: {recursion_count}")
                return True
        return False

    for char in upper_case:
        if upper < 1:
            if backtrack(password + char, upper + 1, lower, digit, special):
                return True

    for char in lower_case:
        if lower < 3:
            if backtrack(password + char, upper, lower + 1, digit, special):
                return True

    for char in digits:
        if digit < 1:
            if backtrack(password + char, upper, lower, digit + 1, special):
                return True

    for char in special_chars:
        if special < 1:
            if backtrack(password + char, upper, lower, digit, special + 1):
                return True

    return False

start_time = time.time()

found = backtrack('', 0, 0, 0, 0)

end_time = time.time()

if not found:
    print("Parola nu a fost găsită.")
else:
    print(f"Timp de execuție: {end_time - start_time} secunde")
