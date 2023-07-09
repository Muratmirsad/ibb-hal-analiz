'''
Created Date: Saturday, April 15th 2023, 5:07:32 pm
Author: Murat Mirsad Dırağa

            github.com/muratmirsad
'''

import csv
import requests
from bs4 import BeautifulSoup

day = input("   Verisini istediğiniz tarihi girin (yıl-ay-gün): ")

url = f"https://tarim.ibb.istanbul/inc/halfiyatlari/gunluk_fiyatlar.asp?tarih={day}&kategori=5&tUsr=M3yV353bZe&tPas=LA74sBcXERpdBaz&tVal=881f3dc3-7d08-40db-b45a-1275c0245685&HalTurId=2"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
data_table = soup.find("table")

with open(f"{day}.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    headers = []
    for header in data_table.find_all("th"):
        headers.append(header.text.strip())
    writer.writerow(headers)

    for row in data_table.find_all("tr"):
        row_data = []
        for cell in row.find_all("td"):
            row_data.append(cell.text.strip())
        if row_data:
            writer.writerow(row_data)
