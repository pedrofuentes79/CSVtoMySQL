filename = "testnull.csv"
import csv
from utils import check_keywords, space_remover

with open(filename) as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for row in reader:
        print(row)


