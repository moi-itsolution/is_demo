import random
import json

a = list('abcd')

z = []
for i in range(0,10):
    temp = {
        'id': i + 1,
        'name': str(i) * 5,
        'type': random.choice(a)
    }
    z.append(temp)

with open('temp.json', 'w') as f:
    json.dump(z, f)