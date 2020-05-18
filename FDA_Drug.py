
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

html = urlopen(
    "https://www.accessdata.fda.gov/scripts/drugshortages/default.cfm")
bsObj = BeautifulSoup(html, "lxml")


table = bsObj.find('table', id="cont")
rows = table.findAll("tr")


links =  [a['href'] for a in table.find_all('a', href=True) if a.text]
new_links = []
for link in links:
    new_links.append(("https://www.accessdata.fda.gov/scripts/drugshortages/"+link).replace(" ", "%20"))


for link in new_links:
    
    
    html = urlopen(link)
    bsObj_href = BeautifulSoup(html, "lxml")
    div_href = bsObj_href.find("div",{"id":"accordion"})
    table_href = bsObj_href.find("table",{"class":"table-bordered table-striped footable"})
    print(table_href)
    href_rows = table_href.findAll("tr")
   


csvFile = open("drug_shortage.csv", 'wt', newline='')
writer = csv.writer(csvFile)
try:
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.get_text())
        writer.writerow(csvRow)

finally:
    csvFile.close()
