def parseArray(str):
    arr = []
    lines = str.split('\n')
    for line in lines:
        if(len(line) > 0):
            arr.append(line.split()[-1])
    arr.sort()
    return arr
    
def variantCompare(str1, str2):
    arr1 = parseArray(str1)
    arr2 = parseArray(str2)

    arrLength = len(arr1)

    result = True

    if len(arr1) != len(arr2):
        result = False
        print('Check Result: ' + str(result))

        if not result:
            for v in arr1:
                print(v)
            print('-'*20)
            for v in arr2:
                print(v)
        
        return

    for i in range(0, arrLength):
        if arr1[i] != arr2[i]:
            result = False
            print('Item mismatch: ' + arr1[i] + ' >>> ' + arr2[i])
            break

    print('Check Result: ' + str(result))

    if not result:
        for v in arr1:
            print(v)
        for v in arr2:
            print(v)

variantCompare('''
1EL04
27504
31509
62649
68712
''',
'''
 INFO : Add variant into pack --> 1EL04
 INFO : Add variant into pack --> 27504
 INFO : Add variant into pack --> 31509
 INFO : Add variant into pack --> 62649
 INFO : Add variant into pack --> 68712
''')
