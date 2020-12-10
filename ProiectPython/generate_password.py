import string
import random
import json
import sys
import getopt


def lista_cuvinte_dupa_lungime(cuvinte, nr_litere):
    dictionar = {cuv: len(cuv) for cuv in cuvinte if len(cuv) <= nr_litere}
    return list(dictionar.keys())


def adauga_caracter_special(parola):  # adaugam caracter special daca nu are deja
    if not ('!' in parola or '?' in parola or '#' in parola or '@' in parola):
        changed = random.randint(1, len(parola) - 1)
        parola = parola[0:changed] + random.choice('!@?#') + parola[changed + 1:len(parola)]
    return parola


def cu_dictionar(argv):  # cand se cere generarea unei parole folosind un dictionar salvat local
    inputfile = ' s'
    try:
        opts, args = getopt.getopt(argv, "u:h", ["use_dict=", "help"])
    except getopt.GetoptError:
        print("Usage: generate_password.py --use_dict <input_dictionary>")
        sys.exit(0)
    if opts:
        for opt, arg in opts:
            if opt in ["-h", "--help"]:
                print("Usage: generate_password.py --use_dict <input_dictionary>")
                sys.exit(0)
            elif opt in ["-u", "--use_dict"]:
                inputfile = arg
    else:
        print("Usage: generate_password.py --use_dict <input_dictionary>")
        sys.exit(0)

    try:
        with open(inputfile) as f:
            data = f.read()
    except FileNotFoundError:
        print("Fisierul nu exista!")
        sys.exit(0)
    try:
        dictionar = json.loads(data)
    except json.JSONDecodeError:
        print("Fisierul este invalid")
        sys.exit(0)

    cuvinte = list(dictionar.keys())
    lungimi = list(dictionar.values())
    lungime_max = max(lungimi)
    lungime = random.randint(12, 18)
    parola = ''
    while len(parola) < lungime:
        if lungime - len(parola) >= lungime_max:
            parola += random.choice(cuvinte)
        else:
            cuvinte = lista_cuvinte_dupa_lungime(cuvinte, lungime - len(parola))
            parola += random.choice(cuvinte)

    parola = adauga_caracter_special(parola)
    print(parola)


def fara_dictionar(): # cand se cere generarea unei parole din alfanumerice random
    symbols = '!?#@'
    characters = string.ascii_letters + string.digits + symbols
    capital = string.ascii_uppercase
    lungime = random.randint(12, 18)
    parola = random.choice(capital)
    while len(parola) < lungime:
        parola += random.choice(characters)
    parola = adauga_caracter_special(parola)
    print(parola)


def main(argv):
    if (len(argv)) != 0:
        cu_dictionar(argv)
    else:
        fara_dictionar()


if __name__ == "__main__":
    main(sys.argv[1:])
