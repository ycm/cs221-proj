import json

scholars = [
    'Zhengzhang',
    'Pan',
    'Shao',
    'Pulleyblank',
    'Li',
    'Karlgren'
]

with open('mc-initial-nucleus-coda.json') as f:
    mc = json.load(f)

print('character\tindex\ttone_label', end='\t')
for idx, s in enumerate(scholars):
    print(s + '_onset', end='\t')
    print(s + '_nucleus', end='\t')
    print(s + '_coda', end='')
    if idx + 1 != len(scholars):
        print('', end='\t')
print()
for char, d in mc.items():
    c, index = char[0], char[1:]
    tone = d['tone_label']
    print('{}\t{}\t{}\t'.format(c, index, tone), end='')
    for idx, s in enumerate(scholars):
        init = d[s]['initial']
        if not init:
            init = '∅'
        nuc = d[s]['nucleus']
        coda = d[s]['coda']
        if not coda:
            coda = '∅'
        print('{}\t{}\t{}'.format(init, nuc, coda), end='')
        if idx + 1 != len(scholars):
            print('', end='\t')
    print()

