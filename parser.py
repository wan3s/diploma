import sys

ITER_LIMIT = 1000

newLineCounter = 0
inputStream = sys.stdin.read().split('\n')
res_arr = []
for line in inputStream:
    dialogues = line.split('\t')[2].split('</span>')
    clear_dialogues = []
    for item in dialogues:
        newLineCounter += 1
        while item.find('>') > item.find('<') != -1:
            item = item[:item.find('<')] + ' ' + item[item.find('>') + 1:]
        if len(item.strip()) > 0 and item.find(':') != -1:
            pair = item.split(':')
            if len(clear_dialogues) > 0 and clear_dialogues[-1][0] == pair[0]:
                clear_dialogues[-1][1] += ' ' + pair[1]
            else:
                clear_dialogues.append(pair)
    for i in range(len(clear_dialogues)):
        tmp_res = {
            'src': clear_dialogues[i][1],
            'dst': clear_dialogues[i + 1][1] if i + 1 < len(clear_dialogues) else ''
        }
        res_arr.append(tmp_res)
    if newLineCounter >= ITER_LIMIT:
        break

print(res_arr)