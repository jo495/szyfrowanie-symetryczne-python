import argparse
from cryptography.fernet import Fernet

parser = argparse.ArgumentParser(description='Szyfruje i deszyfruje pliki')
parser.add_argument('mode', type=str, help='enc - szyfrowanie, dec - deszyfrowanie')
parser.add_argument('file_path', type=str, help='ścieżka do pliku lub do zaszyfrowanego pliku')
parser.add_argument('param_file_path', nargs="?", default="default_flag", type=str,
                    help='ścieżka do pliku z parametrami, potrzebne tylko dla deszyfrowania')
args = parser.parse_args()

if args.mode == 'enc':
    key = Fernet.generate_key()
    f = Fernet(key)
    try:
        text_file = open(args.file_path + ".aes", "xb")
        text_file.write(f.encrypt(open(args.file_path, "br").read()))
        text_file.close()
        text_file = open(args.file_path + ".params", "xb")
        text_file.write(key)
        text_file.close()
        print("Plik zaszyfrowano")
    except:
        print("Plik o takiej nazwie został już zaszyfrowany. Jesli chcesz zaszyfrowac ponownie, usun pliki z "
              "rozszerzeniami .aes i .params")
if args.mode == 'dec':
    key = open(args.param_file_path, "br").read()
    f = Fernet(key)
    encrypted_file = open(args.file_path, "br").read()
    decrypted_file = f.decrypt(encrypted_file)
    try:
        text_file = open(args.file_path[0:-4], "xb")  # [0:-4] ucina .aes
        text_file.write(decrypted_file)
        text_file.close()
        print("Plik odszyfrowano")
    except:
        print("Plik o nazwie " + args.file_path[0:-4] + " już istnieje. Aby zapisac rozszyfrowany "
                                                        "plik pod tą nazwą, musisz usunac istniejacy plik z folderu.")

