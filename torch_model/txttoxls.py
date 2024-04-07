import csv

with open("tmp.log") as file:
    lines = file.readlines()
    # print(lines)

csv_list = []  
for line in lines:
    # print(line.strip().split())
    csv_list.append(line.strip().split(None, 6))

print(csv_list)
with open('output.csv', mode='w', newline='') as f:
    writer = csv.writer(f)
    for row in csv_list:
        writer.writerow(row)





 
