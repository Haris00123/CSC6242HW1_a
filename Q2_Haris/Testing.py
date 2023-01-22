import csv
import os

os.chdir('C:/Users/haris/Desktop/CSC_6242/HW1/Q2_Haris')
print(os.getcwd())

with open('data/movie_overview.csv',newline='',encoding='UTF-8-sig') as csvfile:
    reader=csv.reader(csvfile,delimiter=',')
    for row in reader:
        print(row)
        vals=(int(row[0]),row[1])