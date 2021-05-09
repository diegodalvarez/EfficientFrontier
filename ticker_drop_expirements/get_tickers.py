import os
import pandas as pd

directory_path = os.getcwd()
files = os.listdir(directory_path)
folders = []

for i in files:
   
    if i[0] == "1":
        folders.append(i)
        
file_paths = []

for j in folders:
    
    path = os.path.join(directory_path, j)
    file_paths.append(path)

#needs to be looped 

for p in range(len(file_paths)):
   
    test = file_paths[p]
    
    test_files = os.listdir(test)
    test_csv = []
    for k in test_files:
        
        if k[-1] == "v":
            test_csv.append(k)
    
    csv_paths = []
    for l in test_csv:
        
        path = os.path.join(test, l)
        csv_paths.append(path)
    
    counter = 0
    
    output_csv = pd.DataFrame()
    empty_list = [0] * 378
    
    #needs to be looped
    for o in csv_paths:
        
        print(o)
        csv_path_test = o
        df = pd.read_csv(csv_path_test, index_col = 0)
        df = df.drop(['ret', 'stdev', 'sharpe'], axis = 1)
        cols = df.columns.tolist()
        ticker_count = test_files[counter][:-4] + "_tickers"
        output_csv[ticker_count] = empty_list
        output_csv[ticker_count] = pd.Series(cols)
        counter += 1
    
    output_path = os.path.join(test, "spceficific_tickers.csv")    
    output_csv.to_csv(output_path, index = False)