import re, collections
import timeit


start = timeit.default_timer()

f=open("ffff.txt",'w',encoding="utf-8")

def get_vocab(filename):
    vocab = collections.defaultdict(int)
    with open(filename, 'r', encoding='utf-8') as fhand:
        for line in fhand:
            words = line.strip().split()
            for word in words:
                vocab[' '.join(list(word)) + ' </w>'] += 1
    return vocab


def get_stats(vocab):
    pairs = collections.defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols)-1):
            pairs[symbols[i],symbols[i+1]] += freq
    return pairs
    
def merge_vocab(pair, v_in):
    v_out = {}
    bigram = re.escape(' '.join(pair))
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
    for word in v_in:
        w_out = p.sub(''.join(pair), word)
        v_out[w_out] = v_in[word]
    return v_out

#vocab = {'l o w </w>' : 5, 'l o w e r </w>' : 2,'n e w e s t </w>':6, 'w i d e s t </w>':3}
vocab = get_vocab('10000.txt')

num_merges = 100

for i in range(num_merges):
    pairs = get_stats(vocab)
    if not pairs:
        break
    best = max(pairs, key=pairs.get)
    vocab = merge_vocab(best, vocab)
    f.write("---------------------------------------------\n")
    f.write(str('\nIter: {}\n'.format(i)))
    f.write(('\nBest pair: {}\n'.format(best)))
    f.write("\n")
    f.write(str(vocab))
    f.write("---------------------------------------------\n")
    

    
stop = timeit.default_timer()
print('Time: ', stop - start) 


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

lines = []
with open('ffff.txt') as main_file:
    for line in main_file:
        lines.append(line)

for i, group in enumerate(chunks(lines, n=5000), start=1):
    with open('ffffFile%d.txt' % i, mode="w") as out_file:
        for line in group:
            out_file.write(line)

            
#References: 
#----https://www.aclweb.org/anthology/P16-1162/
#----https://leimao.github.io/blog/Byte-Pair-Encoding/
#----https://stackoverflow.com/questions/53754354/how-do-i-split-a-text-file-into-multiple-text-files-by-25-lines-using-python

