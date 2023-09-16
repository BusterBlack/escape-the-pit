import numpy as np
import csv

output = [["New Selfish","New Selfless","New Collective", "Survived Selfish", "Survived Selfless", "Survived Collective"]]

# parameter data for 6 variables
for a in range(0, 91, 5):
    for b in range(0, (91 - a), 5):
        for c in range(0, (91 - a - b), 5):
            for d in range(0, (91 - a - b - c), 5):
                for e in range(0, (91 - a - b - c - d), 5):
                    f = 90 - a - b - c - d - e
                    output.append((a, b, c, d, e, f))


with open('parametersSweepDataMode2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(output)
