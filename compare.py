import csv
import sys
import time
from operator import itemgetter
from collections import OrderedDict
import numpy as np

import pandas as pd


def get_data(filename, col):

    file_col = pd.read_csv(filename,usecols=col)

    return file_col


def concat_df(df_key, df_col):
        df_concat = pd.concat([df_key['key'], df_col], axis=1)
        return df_concat
    
def main(argv):
    start = time.time()
    if len(argv)>5:
        sys.exit("Run1: python compare.py path_file1 path_file2 0,1(number_of_columns_separated_by_comma) 0,1,2(number_of_columns_separated_by_comma)")
    try:

        keys = argv[3].split(",")
        keys = [int(i)-1 for i in keys]
        
        columns = argv[4].split(",")
        columns = [int(i)-1 for i in columns]
        
        read_cols = keys + columns
        
    except Exception as e:
        print(e)
        sys.exit("Run2: python compare.py path_file1 path_file2 0,1(number_of_columns_separated_by_comma) 0,1,2(number_of_columns_separated_by_comma)")




    

    #create df with key in column, is col 0 + _ + col 1
    file1 = pd.read_csv(argv[1], index_col=False, usecols=keys)
    file1 = file1.applymap(str)
    file1.insert(1,'del',"_")
    #concat all columns to one named key
    file1["key"] = file1.values.sum(axis=1)

    file2 = pd.read_csv(argv[2], index_col=False, usecols=keys)
    file2 = file2.applymap(str)
    file2.insert(1,'del',"_")
    file2["key"] = file2.values.sum(axis=1)
    file2.head()


    #just convert to df because when  grab only one columns this put in series type
    extra_df1 = file1["key"].to_frame()

    extra_df2 = file2["key"].to_frame()
    
    #generate column similar to left join sql
    extra1 = extra_df1.merge(extra_df2.drop_duplicates(), on=['key'], how='left', indicator=True)
    #takes only left only, in this case df1 present
    extra1 = extra1.loc[extra1['_merge'] == "left_only"]
    extra1.to_csv("extrafile_1.csv")

    extra2 = extra_df2.merge(extra_df1.drop_duplicates(), on=['key'], how='left', indicator=True)
    extra2 = extra2.loc[extra2['_merge'] == "left_only"]
    extra2.to_csv("extrafile_2.csv")

    print("Extra files done")
        
    for col in columns: #run every columns and build one csv per row
        
        
        read_cols = []

        #read_cols = keys
        read_cols.append(int(col))
        
        file1_col = get_data(argv[1], read_cols)
        file2_col = get_data(argv[2], read_cols)

        #get name of column
        colname = file1_col.columns[0]
        print("Processing: " + colname)
    
        #contact df with key + df with values
        df1 = concat_df(file1, file1_col)
        df2 = concat_df(file2, file2_col)



        df1.columns = ["key", "data"]
        df2.columns = ["key", "data"]

        #generate dataframe with cols: key, value_file1, value_file2
        df = pd.merge(df1,df2[['key','data']],on='key')
        df = df.rename(columns={"data_x":"file_1","data_y":"file_2"})

        #grab all instances where value_file1 != value_file2
        df = df[df["file_1"]!=df["file_2"]]

        #convert to string all fields, necessary for next step
        df =  df.applymap(str)

        #remove mirror values ex: AB = BA or 21 13 = 13 21
        df_r = df.loc[pd.DataFrame(np.sort(df[['key','file_1', 'file_2']],1),index=df.index).drop_duplicates(keep=False).index]
        df_r.to_csv("header_"+ colname+".csv")
        
        end = time.time()
        print("Time spend: ")
        print(end-start)
        





    end = time.time()
    print("Time spend: ")
    print(end - start)

if __name__ == "__main__":
    main(sys.argv)
            
            
        