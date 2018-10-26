import csv
import codecs

with open('test.csv', 'wb') as f:
    f.write(codecs.BOM_UTF8)

with open('test.csv', 'a') as f:
    csvwriter = csv.writer(f, dialect='excel')
    csvwriter.writerow(['a', 'b'])