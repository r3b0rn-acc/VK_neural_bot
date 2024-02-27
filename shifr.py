import base64


# Кодирование строки по ключу
def encode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = "".join(encoded_chars)
    encoded_string = encoded_string.encode('utf-8')
    encoded = base64.urlsafe_b64encode(encoded_string).rstrip(b'=')
    return str(encoded).lstrip("b'").rstrip("'")


# Декодирование строки в соответсвии с ключом
def decode(key, string):
    string = base64.urlsafe_b64decode(string + b'===')
    string = string.decode('utf-8')
    decoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        decoded_c = chr((ord(string[i]) - ord(key_c)))
        decoded_chars.append(decoded_c)
    decoded_string = "".join(decoded_chars)
    return decoded_string
