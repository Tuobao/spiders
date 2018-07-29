name = 'Swaroop'

if name.startswith('Swa'):
    print('yes, the string starts with "Swa"')

if 'a' in name:
    print('yes, it contains the string "a"')

if name.find('war'):
    print("yes")

delimiter = '_*_'
lists = ['apple', 'mango', 'carrot', 'banana']
print(delimiter.join(lists))
