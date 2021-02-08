# compare_csv

Compare rows of big data files


run:

python compare.py path_file1 path_file2 columns_keys columns_to_compare

nr_column_key -> number of columns of key values that link rows in file1 and file2
nr_columns_to_analise -> number of columns to compare between files


Output:

-1 file per column with diferences between the two files ("header" + name of column.csv)


-File with rows of each file that doesnt appear in the other (key searching) - extrafile1.csv and extrafile2.csv
