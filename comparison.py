def compare ():
    file1 = open('resultsFromGCC.txt', 'r') 
    Lines1 = file1.readlines() 
    
    file2 = open('results.txt', 'r') 
    Lines2 = file2.readlines() 

    
    file3 = open('./Compare results.txt', 'w') 

    i = 1
    while i < len(Lines1):
        if (Lines1[i] == Lines2[i]):
            msg = f'success, "{Lines1[i].rstrip()}" | "{Lines2[i].rstrip()}"\n'
            file3.write(msg)
        else:
            msg = f'failure, "{Lines1[i].rstrip()}" | "{Lines2[i].rstrip()}"\n'
            file3.write(msg)
            print(msg)
        i += 1