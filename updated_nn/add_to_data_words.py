base_type = str(input('0 - Плохая\n1 - Хорошая\n\n')).replace('0', 'bad').replace('1', 'good')
path = f"data/training/{base_type}_words.txt"

s = True
words = []
while s:
    s = str(input('Слово: '))
    if s:
        words.append(s.lower() + '\n')

with open(path, 'r', encoding='utf-8') as f:
    data = f.readlines()

with open(path, 'w', encoding='utf-8') as f:
    for i in sorted(list(set(words+data))):
        f.write(i)
