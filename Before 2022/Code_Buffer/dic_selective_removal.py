'''
    Be careful while iterating the python dictionaries.
    for in in dict:
        dict.pop(i)
    is wrong way!
'''

dict = {('fan', 1994): 10, ('fan2', 1995): 100}

to_remove = []

for i in dict:
    if i[1] < 2000:
        to_remove.append(i)
for i in to_remove:
    dict.pop(i)

print(dict)
