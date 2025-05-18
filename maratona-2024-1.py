import string

s = '''5
Lanca menina, lanca todo esse perfume Desbaratina
Nao da pra ficar imune
Ao teu amor que tem cheiro de coisa maluca
Vem ca, meu bem
Me descola um carinho'''

linhas = list(filter(lambda linha: len(linha) != 0, s.split('\n')))
linhas = linhas[1:]

def parse(f, a):
    return [len(list(filter(f, linha))) for linha in linhas]

q = parse(lambda c: c in string.ascii_letters)
d = parse(lambda c: c in string.digits)
w = parse(lambda c: c.isspace())
p = parse(lambda c: c in string.punctuation)

# print(linhas)
# print(q, d, w, p)

for n in zip(q, d, w, p):
    print(*n)
