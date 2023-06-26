#!/usr/bin/env python

import csv
import requests
from bs4 import BeautifulSoup

url = 'https://salaires.dev'
output_file = 'salaires.dev_data.csv'

response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

table = soup.find('table')

table_data = []
for row in table.find_all('tr'):
    row_data = []
    for index, cell in enumerate(row.find_all(['th'])):
        cell_text = ''
        # Some cells contain spans, separate them
        for span in cell.find_all('span'):
            span_text = span.get_text(strip=True)
            # Replace 'en €' by 'en k€'
            if '€' in span_text:
                span_text = span_text.replace('€', 'K€')
            cell_text += span_text + ' '
        cell_text = cell_text.strip()
        row_data.append(cell_text)
    for index, cell in enumerate(row.find_all(['td'])):
        # All salaries are stated in k€ which elastic will mistake as a string during ingestion
        # Convert those to numbers by removing trailing "k"
        if index == 3:
            value = cell.get_text(strip=True)
            if value.endswith('K'):
                value = value[:-1]
            row_data.append(value)
        else:
            row_data.append(cell.get_text(strip=True))
    table_data.append(row_data)

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(table_data)
