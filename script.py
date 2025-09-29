import subprocess

import json



open('score.txt', 'w').close() #clean file



NUMBER_GAMES=5



#VARS RANGE

A=[-1,0]

B=[0,1]

C=[-1,0]

D=[-1,0]

E=[-1,0]



CHANGE=0.5



#valores atuais

a=A[0]

b=B[0]

c=C[0]

d=D[0]

e=E[0]



counter=0



while 1:

    counter+=1

    for i in range(NUMBER_GAMES):

        subprocess.call(['python3', 'student.py'])



    f = open('vars.json',)

    vars = json.load(f)

    f.close()



    med=0

    f = open("score.txt", "r")

    for x in f:

        med+=int(x)

    med=med/NUMBER_GAMES

    f.close()

    open('score.txt', 'w').close() #clean file



    f = open("games.txt", "a") #a=append

    f.write("game["+str(counter)+"] stats="+str(vars)+" media="+str(med)+"\n")

    f.close()



    #mudar as vars

    a+=CHANGE

    if a>A[1]:

        a=A[0]

        b+=CHANGE

    if b>B[1]:

        b=B[0]

        c+=CHANGE

    if c>C[1]:

        c=C[0]

        d+=CHANGE

    if d>D[1]:

        d=D[0]

        e+=CHANGE

    if e>E[1]:

        quit()



    data={"a":a,"b":b,"c":c,"d":d,"e":e}



    with open('vars.json', 'w') as f:

        json.dump(data, f)