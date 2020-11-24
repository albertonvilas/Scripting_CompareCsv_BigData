import csv
import sys
import time
from operator import itemgetter


def read_file(path_file):
    with open(path_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        file_read = [list(row) for row in csv_reader]
        
    return file_read

def val_select(list_values, columns):
    list_out = []
    for i in columns:
        list_out.append(list_values[i-1])
    return(list_out)

def value_exist(value,dict_check):
    exist = False
    key = value[3] + value[5]
    elemB=""
    if key in dict_check:
        elemB = dict_check[key]
        exist = True
       
    return exist,elemB

def write_to_file(file_write, row):        
    f = open(file_write,'a')
    writer = csv.writer(f, delimiter = ',')
    writer.writerow(row)
    f.close()
    
def main(argv):
    start = time.time()
    if len(argv)>4:
        print(argv)
        sys.exit("Run1: python compare.py path_file1 path_file2 0,1,2(number_of_columns_separated_by_comma)")
    try:
        file1 = read_file(argv[1])
        file2 = read_file(argv[2])
        columns = argv[3].split(",")
        columns = [int(i) for i in columns]

    except Exception as e:
        print(e)
        sys.exit("Run2: python compare.py path_file1 path_file2 0,1,2(number_of_columns_separated_by_comma)")

    end = time.time()
    print("Read time spend: ")
    output = open('output.csv', 'w')
    output.truncate()

    extra1= open('extra_file1.csv', 'w')
    extra1.truncate()

    extra2= open('extra_file2.csv', 'w')
    extra2.truncate()

    file1_dict = {x[3]+x[5]:x for x in file1}
    file2_dict = {x[3]+x[5]:x for x in file2}
    print(len(file1))
    print(len(file2))
    print("DICTS:")
    print(len(file1_dict))
    print(len(file2_dict))

    n_files = 0




    for row in file1:
        i=val_select(row,columns)
        
        n_files +=1
        if n_files%100==0:
            print("Rows read file1: " + str(n_files) + " Number total rows file1: " + str(len(file1)))
            end = time.time()
            print(end - start)


        boolean, elem = value_exist(row,file2_dict)
        if boolean == True:
            j= val_select(elem,columns)


            if i != j:
                val = ",".join(i)
                val2 = ",".join(j)
                line = row[3]+","+ row[5]+","+val + ","+ elem[3]+ "," + elem[5]+ "," + val2
                line = line.split(",")
                write_to_file("output.csv", line)
                    
        else:
            write_to_file("extra_file1.csv", row)
                        
    
    n_files=0
    
    for row2 in file2:
        n_files +=1
        if n_files%100==0:
            print("Rows read file2: " + str(n_files) + " Number total rows file2: " + str(len(file2)))

        boolean, elem = value_exist(row2,file1_dict)
        if boolean == False:
            write_to_file("extra_file2.csv", row2)


    end = time.time()
    print("Time spend: ")
    print(end - start)

if __name__ == "__main__":
    main(sys.argv)
            
            
        