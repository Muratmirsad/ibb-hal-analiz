'''
Created Date: Saturday, April 15th 2023, 8:15:38 pm
Program Name: ibb-hal-analiz.py
Author: Murat Mirsad Dırağa

            github.com/muratmirsad
'''

import csv
import requests
from bs4 import BeautifulSoup
import subprocess

print("\n-----       version 1.1       -----\n")
print("'''\nCreated Date: Saturday, April 15th 2023, 8:15:38 pm\nProgram Name: ibb-hal-analiz.py\nAuthor: Murat Mirsad Dırağa\n\n            github.com/muratmirsad\n'''\n")
print("   Hoş geldiniz.\n")
while True:
    print("\033[32m")
    print("   [1] Veri indirme.")
    print("   [2] Veri karşılaştırma.")
    print("\033[31m", end="")
    print("   [3] Çıkış.")
    print("\033[37m")
    
    key = int(input("\n   Yapmak istediğiniz işlemi seçin: "))

    subprocess.call('cls', shell=True)
    subprocess.call('clear', shell=True)

    if key == 1:
        print("   Veri indiriciye hoşgeldin.\n")
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
        print("\n  ", day + ".csv dosyası oluşturuldu.\n")

    elif key == 2:
        print("   Veri karşılaştırıcıya hoşgeldin.\n")
        file_1 = input("   İlk tarihi girin (yıl-ay-gün): ")
        file_2 = input("   İkinci tarihi girin (yıl-ay-gün): ")

        file_1 = file_1 + ".csv"
        file_2 = file_2 + ".csv"

        low_prices_1= []
        high_prices_1 = []
        low_prices_2 = []
        high_prices_2 = []

        price_changes = []
        products = []

        print(file_1, end=" ")
        print("  -  ", end=" ")
        print(file_2)
        print("\n\nFiyat değişimleri")

        with open(file_1, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                product_name = row[0]
                products.append(product_name)

                low_prices = float(row[2].replace(" TL", "").replace(",", "."))
                high_prices = float(row[3].replace(" TL", "").replace(",", "."))

                low_prices_1.append(low_prices)
                high_prices_1.append(high_prices)

        with open(file_2, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                product_name = row[0]

                if product_name in products:
                    index = products.index(product_name)

                    low_prices = float(row[2].replace(" TL", "").replace(",", "."))
                    high_prices = float(row[3].replace(" TL", "").replace(",", "."))

                    low_prices_1.append(low_prices)
                    high_prices_2.append(high_prices)

                    price_changes_low = low_prices - low_prices_1[index]
                    price_changes_high = high_prices - high_prices_1[index]

                    if price_changes_low != 0:
                        price_changes.append(price_changes_low)
                        print("\nÜrün:", products[index])
                        
                        if price_changes_low < 0:
                            print("\033[91m", end=" ")
                        else:
                            print("\033[92m", end=" ")

                        print("Düşük fiyat farkı:", price_changes_low)
                        print("\033[0m")

                    if price_changes_high != 0:
                        price_changes.append(price_changes_high)
                        print("\nÜrün:", products[index])

                        if price_changes_high < 0:
                            print("\033[91m", end=" ")
                        else:
                            print("\033[92m", end=" ")

                        print("Yüksek fiyat farkı:", price_changes_high)
                        print("\033[0m")

                else:
                    low_prices = float(row[2].replace(" TL", "").replace(",", "."))
                    high_prices = float(row[3].replace(" TL", "").replace(",", "."))

                    low_prices_2.append(low_prices)
                    high_prices_2.append(high_prices)

                    price_changes_low = low_prices
                    price_changes_high = high_prices

                    price_changes.append(price_changes_low)
                    price_changes.append(price_changes_high)

                    print("\nÜrün:", product_name)

                    if price_changes_low < 0:
                        print("\033[91m", end=" ")
                    else:
                        print("\033[92m", end=" ")

                    print("Düşük fiyat farkı:", price_changes_low)
                    print("\033[0m")

                    if price_changes_high < 0:
                        print("\033[91m", end=" ")
                    else:
                        print("\033[92m", end=" ")

                    print("Yüksek fiyat farkı:", price_changes_high)
                    print("\033[0m")
    elif key == 3:
        exit()