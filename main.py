# This is a cipher created by me. It's based on Vigenere cipher, but with a twist. It also scrambles the alphabet based on the key, which means the key itself also changes based on the key itself.
# The length of the message also changes depending on the key.
# It adds as many characters as there are in the key in places of the index of the key characters.
# But it adds letters based on the scrambled alphabet, so you can't guess the key even if you knew which characters are being added.
# The biggest flaws with this cipher are statistical analysis and PEBKAC with short keys.
import hashlib


def scramble_alphabet(key_code):
    scrambled_alphabet = list(alphabet)
    current_seed = None

    for index, key_number in enumerate(key_code):
        if current_seed is None:
            current_seed = int(key_number)
        else:
            current_seed *= index + int(key_number)

    # Convert the seed into a cryptographic hash state (Hash-DRBG approach)
    seed_bytes = str(current_seed).encode("utf-8")

    # Cryptographically secure Fisher-Yates shuffle using SHA-256
    n = len(scrambled_alphabet)
    for i in range(n - 1, 0, -1):
        seed_bytes = hashlib.sha256(seed_bytes).digest()
        rand_int = int.from_bytes(seed_bytes[:4], "big")
        j = rand_int % (i + 1)
        scrambled_alphabet[i], scrambled_alphabet[j] = (
            scrambled_alphabet[j],
            scrambled_alphabet[i],
        )

    return "".join(scrambled_alphabet)


def encrypt_character(plain_character, key_character, scrambled_alphabet):
    key_character_code = scrambled_alphabet.index(key_character)
    plain_character_code = scrambled_alphabet.index(plain_character)

    # Combine plain + key, and loop back to zero at character_count
    cipher_character_code = (plain_character_code + key_character_code) % len(scrambled_alphabet)

    # return the character of cipher_character_code
    return scrambled_alphabet[cipher_character_code]


def decrypt_character(cipher_character, key_character, scrambled_alphabet):
    key_character_code = scrambled_alphabet.index(key_character)
    cipher_character_code = scrambled_alphabet.index(cipher_character)

    # Combine plain + key, and loop back to zero at character_count
    plain_character_code = (cipher_character_code - key_character_code) % len(scrambled_alphabet)

    # Turn cipher_code back into a character
    return scrambled_alphabet[plain_character_code]


def encrypt(string, key):
    key_code = []

    # get index of each character of the key
    for character in key:
        key_code.append(str(alphabet.index(character)))

    # scramble the alphabet
    scrambled_alphabet = scramble_alphabet(key_code)

    cipher = ""

    for (character_index, character) in enumerate(string):
        # add 'fake' characters in places of the indexes that correspond to the key
        while str(len(cipher)) in key_code:
            cipher += scrambled_alphabet[len(cipher)]

        # get correct key character
        key_index = character_index % len(key)
        key_character = key[key_index]

        # encrypt a character
        cipher += encrypt_character(character, key_character, scrambled_alphabet)

    return cipher


def decrypt(string, key):
    key_code = []

    # get index of each character of the key
    for character in key:
        key_code.append(str(alphabet.index(character)))

    # scramble the alphabet
    scrambled_alphabet = scramble_alphabet(key_code)

    plain = ""

    for (character_index, character) in enumerate(string):
        # skip the 'fake' characters in places of the indexes that correspond to the key
        if str(character_index) in key_code:
            continue

        # get correct key character
        key_index = len(plain) % len(key)
        key_character = key[key_index]

        # decrypt a character
        plain += decrypt_character(character, key_character, scrambled_alphabet)

    return plain


alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 !@#$%^&*()-_+=`~;:'[]{}|<>,./?\"\\"

# Menu for inputting data
available_actions = {'encrypt': encrypt, 'decrypt': decrypt}
while True:
    print("What do you want to do? ('encrypt', 'decrypt', 'exit')")
    action = input(">>> ").lower()
    if action in available_actions:
        print(f"\nWhat is the message you want to {action}?")
        message = input(">>> ")
        print("\nWhat is the key?")
        key = input(">>> ")
        answer = available_actions[action](message, key)
        print(f"\n{action.title()}ed message (surrounded by «»): «{answer}»\n")
    elif action == "exit":
        print("\nExiting!\n")
        break
    else:
        print("\nInvalid action!\n")
        continue
