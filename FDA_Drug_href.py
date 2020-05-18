
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
href_rows = []
for link in new_links:   
    link = link.replace("®", "%C2%AE")
    html = urlopen(link)
    bsObj_href = BeautifulSoup(html, "lxml")
    #bsObj_href = BeautifulSoup (html.decode('utf-8', 'ignore'))
    div_href = bsObj_href.find("div",{"id":"accordion"})
    href_rows.append(div_href.findAll("tr"))

print(href_rows)
csvFile = open("drug_shortage_href.csv", 'wt', newline='')
writer = csv.writer(csvFile)
try:
    for row in href_rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.get_text())
        writer.writerow(csvRow)

finally:
    csvFile.close()