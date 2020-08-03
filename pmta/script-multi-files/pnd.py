import pandas as pd
from collections import Counter
import shutil, os
import sys
from glob import glob

# genre_esp
def upload_email(fichier):
    try:
        print (fichier)
        df = pd.read_csv("incsv/"+fichier)
        df['dsnStatus'][df['dsnStatus']=='2.0.0 (success)']

        df1 = df.to_csv("outcsv/"+fichier,columns=['rcpt'], index=False)
        print(df['rcpt'].count())
    except:
        pass

    return True


# run program
print("*****************************************************************************")
print("************************ Start Samir Program ********************************")
print("*****************************************************************************\n")
#folder = raw_input("type folder name please :")
arr = os.listdir("incsv")
for t_file in arr :
    upload_email(t_file)
    shutil.move("incsv/"+t_file, 'archives')

stock_file = sorted(glob("outcsv/*.csv"))
print(stock_file)

print("*****************************************************************************")
print("************************ nombre de tout les emails **************************")
print("*****************************************************************************\n")

dfinal = pd.concat((pd.read_csv(file).assign(filename = file) for file in stock_file), ignore_index = True)
dfinal.to_csv("outcsv/final.csv",columns=['rcpt'], index=False)
print(dfinal['rcpt'].count())

print("\n*****************************************************************************")
print("************************ Fin Samir Program **********************************")
print("*****************************************************************************")
