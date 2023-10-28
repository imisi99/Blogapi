import csv

#To create a new csv file 

header = ["title","body","author"]

with open("data.csv","w") as file:
    writer = csv.writer(file)
    writer.writerow(header)

header = ["firstname","lastname","username","email","password"]

with open("u_data.csv","w") as file:
    writer = csv.writer(file)
    writer.writerow(header)