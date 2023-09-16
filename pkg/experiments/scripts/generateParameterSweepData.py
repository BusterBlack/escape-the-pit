import numpy as np
import csv

output = [["selfish","selfless","collective"]]

for i in range(0,91):
    for j in range(90,0,-1):
        if i == 90:
            j=0
            l=0
            output.append([i,j,l])
            break
        if (j-i)<0:
            break
        j=j-i
        l=90-j-i
        output.append([i,j,l])

with open('parametersSweepData.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(output)

