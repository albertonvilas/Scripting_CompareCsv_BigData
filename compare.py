import csv
import sys
import time
from operator import itemgetter
from collections import OrderedDict

import pandas as pd

def read_file(path_file, colums):
    #with open(path_file, 'r') as csv_file:
    #    csv_reader = csv.reader(csv_file, delimiter=',')
    #    file_read = [list(row) for row in csv_reader]
    
    print("build dataframe")
    data = pd.read_csv(path_file, header=None ,usecols=colums)
    print("dataframe to list")
    file_read = data.values.tolist()
    
    return file_read

def create_dict(keys, col, file_list):
    new_dict={}
    for row in file_list:
        unique = str(row[0])+ "_"+ str(row[1])
        if unique not in new_dict: #key nao encontrada no dict e portanto adicionada
            
            new_dict[unique] = str(row[col])
        else: #key ja registada no dict e portanto append dos valores
            
            value = new_dict[unique]
            new_dict[unique] = value+ "_" +str(row[col])
    
    return new_dict

def writer_to_file(file_write, row):       
    """
    Write row to csv (file_write)

    row: list with values of row to write
    """ 
    f = open(file_write,'a')
    writer = csv.writer(f, delimiter = ',')
    writer.writerow(row)
    f.close()

def output_csv(name_file):
    """
    Sorted namefile: normal values first; duplicates in the end (values like-> key: 21_23_45 )

    name_file: csv name
    """
    with open(name_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        correct_csv = [list(row) for row in csv_reader]

    first = []
    last = []
    for i in correct_csv:
        if i not in last or i not in first:
            try:
                if "_" in i[2] or "_" in i[5]:
                    last.append(i)
                else:
                    first.append(i)
            except:
                first.append(i)

    output = open(name_file,'w')
    output.truncate()
    writer = csv.writer(output, delimiter = ',')
    for row in first:
        writer.writerow(row)
    for row in last:
        writer.writerow(row)
    output.close()

def extra_rows(file_list_a, file_dict_b, keys ,filename):

    """
    Output in filename.csv rows of file_list_a that doesnt appear in file_dict_b (search by key)


    file_list_a : file with keys to search
    file_dict_b : file where the keys from file_list_a will be search
    keys: list with numbers of columns of key
    filename: name of output pull
    """
    for row in file_list_a: #search keys doesnt exist in other file
        key = str(row[0])+ "_"+ str(row[1])
        if key not in file_dict_b:
            writer_to_file(filename,row)

    
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
        print("reading_file1")
        file1 = read_file(argv[1], read_cols)

        print("reading_file2")
        
        file2 = read_file(argv[2], read_cols)


        
    except Exception as e:
        print(e)
        sys.exit("Run2: python compare.py path_file1 path_file2 0,1(number_of_columns_separated_by_comma) 0,1,2(number_of_columns_separated_by_comma)")

    end = time.time()
    print("Read time spend: ")
    print(end-start)


    
    for col in columns: #run every columns and build one csv per row

        n_files = 0
        
        index_col = read_cols.index(col) #search position of col in list of all readable cols
        name_file = 'header_'+str(file1[0][index_col])+'.csv'
        output = open(name_file, 'w')
        output.truncate()
        writer = csv.writer(output, delimiter = ',')
        
        file1_dict = create_dict(keys,index_col,file1)
        file2_dict = create_dict(keys,index_col,file2)
        end = time.time()
        print("Create dict time spend: ")
        print(end-start)

        for row in file1:
            
            n_files +=1
            if n_files%100==0:
                print("Rows read: " + str(n_files) + " Number total rows file1: " + str(len(file1)))
                end = time.time()
                print(end - start)


            keyA = str(row[0])+ "_"+ str(row[1])
            

            if keyA in file2_dict:
                elemA = file1_dict[keyA]
                elemB = file2_dict[keyA]
                valueA = sorted(elemA.split("_"))
                valueB = sorted(elemB.split("_"))
                #list to string to write
                valueA_str = '_'.join([str(elem) for elem in valueA])
                valueB_str = '_'.join([str(elem) for elem in valueB])
                keyA = keyA.replace("_",",")

                if valueA_str != valueB_str:
                    
                    line = keyA + "," + valueA_str + "," + keyA + "," + valueB_str
                    line = line.split(",")
                    writer.writerow(line)

        output.close()
        
            
        output_csv(name_file) #modify csv to correct output

    
    
    print("Creating extra_file 1") 
    filename = 'extra_file1.csv'
    output_extra = open(filename, 'w')
    output_extra.truncate()
    extra_rows(file1,file2_dict,keys,filename)
    
    print("Creating extra_file 2")
    filename = 'extra_file2.csv'
    output_extra = open(filename, 'w')
    output_extra.truncate()
    extra_rows(file2,file1_dict,keys,filename)                  
    
    end = time.time()
    print("Time spend: ")
    print(end - start)

if __name__ == "__main__":
    main(sys.argv)
            
            
        