import os
import glob
import pandas as pd
import csv
import numpy as np
from time import process_time
import math

def csv_to_txt():
    # Aumenta o limite que a biblioteca csv consegue abrir arquivos. 300mb.
    csv.field_size_limit(300 * 1024 * 1024)

    path = "../data"
    all_files = glob.glob(os.path.join(path, "*.csv"))
    if(len(all_files)==0):
        pass
    else:
        # Função para remover espaços e tabulações extras e substituí-los por um único espaço
        def remove_spaces_and_tabs(input_string):
            return ' '.join(input_string.split())

        for file in all_files:
            file_original = os.path.basename(file)
            file_txt = os.path.join(path, file_original[:-4] + ".txt")
            
            with open(file, "r", encoding="utf-8") as csv_file, open(file_txt, "w",encoding="utf-8") as txt_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    # Remove espaços e tabulações extras e substituir por um único espaço
                    cleaned_row = [remove_spaces_and_tabs(field) for field in row]
                    
                    #Escreve os campos no arquivo txt separados por espaços
                    txt_file.write(" ".join(cleaned_row) + "\n")

            print(f"Dados do arquivo '{file}' foram processados e salvos em '{file_txt}'")
            # Remove os arquivos .csv após a conversão
            os.remove(file)

def dictonary_name_users():
    
    file_path = "../data/dictonary_user.txt"
    if os.path.exists(file_path):
        pass

    else:
        df = pd.read_csv("./data/user_user.txt",sep=" ") # open file
        df = df[["userA","userB"]].copy() # Create dataframe from df (all data) just with [userA, userB] columns
        unique_names = pd.unique(df.values.flatten()) # unique values in dataframe
        #data_2 = [str(i) for i in df["userB"].values]    # List of name in userB column
        #data_T = data_1 + data_2                         # List of all of users

        N = len(unique_names)                            # Total number of users
        dict_users = np.arange(0,N,1)                    # Create range to dictionary of users_names
        dictonary = [f"{i:06d}" for i in dict_users]     # dictonary with number [0, N] with same digitals number

        dict_converted = {}                              # Dictonary with {name:cod_name}
        dict_converted["name"] = unique_names
        dict_converted["cod_name"] = dictonary
        df1 = pd.DataFrame(data=dict_converted)
        df1.to_csv(file_path,sep=" ",index=False)


def mapping_users(Num_samples_I,Num_samples_F):
    newpath = f"../data/filter_S_I_{Num_samples_I}_S_F_{Num_samples_F}/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    df1 = pd.read_csv("../data/dictonary_user.txt", sep=" ")
    
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    
    df1['cod_name'] = df1['cod_name'].astype(str).str.zfill(6)
    
    new_file = newpath+f"user_user_NumSI_{Num_samples_I}_NumSF_{Num_samples_F}.txt"
    
    ter_ = 50 # To save of i multiply 50

    # If  file with changers exist -> open it
    if(os.path.exists(new_file)):
        df = pd.read_csv(new_file, sep=" ")
    
    # Else -> open original file
    else:
        df = pd.read_csv("../data/user_user.txt", sep=" ")
    
    for i in range(Num_samples_I,Num_samples_F):
        t1_start = process_time() 

        df.replace(to_replace=df1['name'].values[i],value=df1['cod_name'].values[i],inplace=True)

        t1_stop = process_time()
        
        print(f"term = {i}, rest = {(Num_samples_F-Num_samples_I)-i} | time= {(t1_stop-t1_start):.5f}s, estimated_time_to_finish={((t1_stop-t1_start)*((Num_samples_F-Num_samples_I)-i)):.5f}s")
        if(i/ter_ % 1==0 and i!=0):
            df.to_csv(newpath+f"user_user_NumSI_{Num_samples_I}_NumSF_{Num_samples_F}.txt",sep=" ",index=False)
        
    hist_file = pd.DataFrame(data={"time":[Num_samples_F - Num_samples_I]})
    hist_file.to_csv(newpath+"hist_user_user.txt",sep=" ",index=False)
    df.to_csv(new_file,sep=" ",index=False)
    
def split_user_user():
    