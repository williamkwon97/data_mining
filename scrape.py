import csv

with open('/Users/williamkwon/Documents/data_mining/editors.csv',
          'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    for line in csv_reader:
        print(line[1])