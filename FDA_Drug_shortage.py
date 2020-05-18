from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

html = urlopen(
    "https://www.accessdata.fda.gov/scripts/drugshortages/default.cfm")
bsObj = BeautifulSoup(html, "lxml")

# list for all rows with all values
data = []

# get table on main page
table = bsObj.find('table', {'id': 'cont'})

# work with every row separatelly
for row in table.find_all("tr")[1:]:  # use `[0:]` to skip header
    # get columns only in this row
    cols = row.find_all('td')

    # get name and url from first column
    link = cols[0].find('a', href=True)
    name = link.text.strip()
    url = link['href']
    url = "https://www.accessdata.fda.gov/scripts/drugshortages/" + url
    url = url.replace(" ", "%20").replace("®", "%C2%AE")
    print('name:', name)
    print('url:', url)

    # get status from second column
    status = cols[1].text.strip()
    print('status:', status)

    # subpage
    html = urlopen(url)
    bsObj_href = BeautifulSoup(html, "lxml")
    subtable = bsObj_href.find("table")
    if not subtable:
        data.append([name, status, link, '', '', '', ''])
        print('---')
    else:
        for subrows in subtable.find_all(
                'tr')[1:]:  # use `[0:]` to skip header
            #print(subrows)
            subcols = subrows.find_all('td')
            presentation = subcols[0].text.strip()
            availability = subcols[1].text.strip()
            related = subcols[2].text.strip()
            reason = subcols[3].text.strip()
            data.append([
                name, status, link, presentation, availability, related, reason
            ])
            print(presentation, availability, related, reason)
            print('---')

    print('----------')

with open("FDA_drug_shortage.csv", 'wt', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # write header - one row - using `writerow` without `s` at the end
    #writer.writerow(['Name', 'Status', 'Link', 'Presentation', 'Availability', 'Related', 'Reason'])

    # write data - many rowr - using `writerows` with `s` at the end
    writer.writerow([
        'Name', 'Status', 'Link', 'Presentation', 'Availability', 'Related',
        'Reason'
    ])
    writer.writerows(data)

# no need to close because it use `with`