data = dict()

data2 = {
    'name' : 'haider',
    'age' : 26
}

print(data)
print(data2)

#using bool

res = not bool(data)
res2 = not bool(data2)

print(f"Result 1 : {res} \n Result 2 : {res2} ")

def dataa(x):
    if x == 2:
        print("x == 2")
        return
    print("it runs !!")

dataa(2)