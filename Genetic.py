import random,sys
def initializeBoard():
    board=[]
    total=4
    #total=int(input("\nEnter the total number of pouplations: "))
    for population in range(total):
        array2=[]
        for i in range(8):
            array=[]
            for j in range(8):
                array.append(0)
            array2.append(array)
        board.append(array2)
    return board
def placeQueens():
    for k in range(len(board)):
        for j in range(8):
            i=random.randint(0,7)
            board[k][i][j]=1
    return board
def fitnessFunction(board,strings):
    fitnessValues=[]
    for eachBoard in range(len(board)):
        fitnessVal=0
        for eachCol in range(8):
            right=eachCol+1
            while right<8:
                if board[eachBoard][7-int(strings[eachBoard][eachCol])+1][right]==1:
                    fitnessVal+=1
                right+=1
            upperDig=7-int(strings[eachBoard][eachCol])
            right=eachCol+1
            while upperDig>=0 and right<8:
                if board[eachBoard][upperDig][right]==1:
                    fitnessVal+=1
                right+=1
                upperDig-=1
            downDig=7-int(strings[eachBoard][eachCol])+2
            right=eachCol+1
            while downDig<8 and right<8:
                if board[eachBoard][downDig][right]==1:
                    fitnessVal+=1
                downDig+=1
                right+=1
        #print("\nFitness Value: "+str(fitnessVal))
        fitnessValues.append(fitnessVal)
    return fitnessValues 
def getStrings(board):
    strings=[]
    for i in range(len(board)):
        string=""
        for j in range(8):
            for k in range(8):
                if board[i][k][j]==1:
                    string+=str(7-k+1)
                    break
        strings.append(string)
    return strings
def getProbabilities(fitnessVals):
         probs=[]
         for i in range(len(fitnessVals)):
             probs.append(fitnessVals[i]/sum(fitnessVals))
         return probs
def sortProbabilities(prob):
    new=0
    leastProbs={}
    for i in range(len(prob)):
        if prob[i]==max(prob):
            #print("\nDiscarding board number: "+str(i+1)+". Since it is having the maximum probability of "+str(prob[i])+".")
            new=i
        else:
            leastProbs[i]=prob[i]
    leastProbs[new]=min(prob)
    return sorted(leastProbs.items(),key=lambda kv:(kv[1], kv[0]))
def crossOver(sort,strings):
    temp=[]
    sorts=sort
    for i,j in sorts:
        temp.append(strings[i])
    if len(temp)<4:
        for i in range(4-len(temp)):
            temp.append(strings[i])
    a=temp[0]
    temp[0]=temp[0][:3]+temp[2][3:len(temp[2])]
    temp[2]=temp[2][:3]+a[3:len(a)]
    b=temp[1]
    temp[1]=temp[1][:5]+temp[3][5:len(temp[3])]
    temp[3]=temp[3][:5]+b[5:len(b)]
    return temp
def mutation(newStrings):
    mutatedStrings=[]
    for eachString in newStrings:
        mutate=""
        change=""
        for i in range(1,len(eachString)+1):
            repeat=eachString[i-1]
            if mutate.__contains__(repeat):
                change=eachString[i-1]
            mutate+=str(eachString[i-1])
        for j in range(1,9):
            if not mutate.__contains__(str(j)):
                mutate=mutate.replace(change,str(j),1)
                break
        mutatedStrings.append(mutate)
    return mutatedStrings
def makeBoard(mutated):
    board=initializeBoard()
    for k in range(len(mutated)):
        for j in range(8):
            i=int(mutated[k][j])-1
            board[k][i][j]=1
    return board
def printBoard(board,strings):
    for k in range(len(board)):
        print("\nBoard No.: "+str(k+1))
        print("========================================================================")
        for i in range(8):
            print("\t"+str(i+1),end="")
        print("\t||")
        for i in range(8):
            print("_________",end="")
        print()
        for i in range(8):
            print(str(7-i+1)+" |",end="")
            for j in range(8):
                #print("\t"+str(board[k][i][j]),end="")
                if board[k][i][j]==1:
                    print("\tQ",end="")
                else:
                    print("\t-",end="")
            print("",end="\t||\n")
        print("========================================================================")
        print("\nString: "+strings[k])
threshold=float(input("\nEnter the threshold probability to stop: "))
board=[]
board=initializeBoard()
board=placeQueens()
strings=getStrings(board)
fitnessVals=fitnessFunction(board,strings)
prob=getProbabilities(fitnessVals)
print("\n\n__________________________________________________________")
print("Strings\t\tFitness Values\t\tProbabilities\t||")
print("==========================================================")
for i in range(4):
    print(strings[i]+"\t\t"+str(fitnessVals[i])+"\t\t"+str('%.6f'%prob[i])+"\t||")
sort=sortProbabilities(prob)
for i in prob:
    #printBoard(board,strings)
    if i<=threshold:
        printBoard(board,strings)
        sys.exit()
newStrings=crossOver(sort,strings)
mutated=mutation(newStrings)
endLoop=False
for iteration in range(5000):
    print("\nIteration Number: "+str(iteration+1)+"\n")
    board=makeBoard(mutated)
    fitnessVals=fitnessFunction(board,strings)
    prob=getProbabilities(fitnessVals)
    print("__________________________________________________________")
    print("Strings\t\tFitness Values\t\tProbabilities\t||")
    print("==========================================================")
    for i in range(4):
        print(strings[i]+"\t\t"+str(fitnessVals[i])+"\t\t"+str('%.6f'%prob[i])+"\t||")
    print("__________________________________________________________\n")
    sort=sortProbabilities(prob)
    for i,j in sort:
        if j<=threshold:
            endLoop=True
            break
    if endLoop==True:
        break
    newStrings=crossOver(sort,strings)
    mutated=mutation(newStrings)
    strings=mutated  
printBoard(board,strings)