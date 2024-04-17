import csv
import requests
from bs4 import BeautifulSoup
import os

MESSAGES = {
    "welcome": "\n-----       version-1.2       -----\n'''\nCreated Date: Saturday, April 15th 2023, 8:15:38 pm\nLast Update: April 17th 2024\nProgram Name: ibb-hal-analiz.py\nAuthor: Murat Mirsad Dırağa\n\n            github.com/muratmirsad\n'''\n\n   Hoş geldiniz.\n",
    "options": "\033[32m   [1] Veri indirme.\n   [2] Veri karşılaştırma.\n\033[31m   [3] Çıkış.\n\033[37m",
    "data_downloader": "   Veri indiriciye hoşgeldin.\n",
    "data_comparator": "   Veri karşılaştırıcıya hoşgeldin.\n",
    "file_created": "\n   {}.csv dosyası oluşturuldu.\n",
    "file_comparison": "{} - {}\n\nFiyat değişimleri",
    "product_change": "\nÜrün: {}",
    "price_change": "\033[91m" if True else "\033[92m",
    "end_color": "\033[0m"
}

def display_message(message_key, *args):
    print(MESSAGES[message_key].format(*args))

def get_data():
    display_message("data_downloader")
    day = input("   Verisini istediğiniz tarihi girin (yıl-ay-gün): ")
    url = f"https://tarim.ibb.istanbul/inc/halfiyatlari/gunluk_fiyatlar.asp?tarih={day}&kategori=5&tUsr=M3yV353bZe&tPas=LA74sBcXERpdBaz&tVal=881f3dc3-7d08-40db-b45a-1275c0245685&HalTurId=2"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    data_table = soup.find("table")

    with open(f"{day}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        headers = [header.text.strip() for header in data_table.find_all("th")]
        writer.writerow(headers)

        for row in data_table.find_all("tr"):
            row_data = [cell.text.strip() for cell in row.find_all("td")]
            if row_data:
                writer.writerow(row_data)
    display_message("file_created", day)

def handle_data():
    display_message("data_comparator")
    file_1 = input("   İlk tarihi girin (yıl-ay-gün): ") + ".csv"
    file_2 = input("   İkinci tarihi girin (yıl-ay-gün): ") + ".csv"

    low_prices_1, high_prices_1, low_prices_2, high_prices_2 = [], [], [], []
    price_changes, products = [], []

    display_message("file_comparison", file_1, file_2)

    def process_file(file_path, low_prices, high_prices):
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                product_name, low_price, high_price = row[0], float(row[2].replace(" TL", "").replace(",", ".")), float(row[3].replace(" TL", "").replace(",", "."))
                products.append(product_name)
                low_prices.append(low_price)
                high_prices.append(high_price)

    process_file(file_1, low_prices_1, high_prices_1)
    process_file(file_2, low_prices_2, high_prices_2)

    for product_name, low_price_1, high_price_1, low_price_2, high_price_2 in zip(products, low_prices_1, high_prices_1, low_prices_2, high_prices_2):
        low_price_change, high_price_change = low_price_2 - low_price_1, high_price_2 - high_price_1
        if low_price_change != 0:
            display_message("product_change", product_name)
            print(MESSAGES["price_change"] if low_price_change < 0 else MESSAGES["price_change"], "Düşük fiyat farkı:", low_price_change, MESSAGES["end_color"])
        if high_price_change != 0:
            display_message("product_change", product_name)
            print(MESSAGES["price_change"] if high_price_change < 0 else MESSAGES["price_change"], "Yüksek fiyat farkı:", high_price_change, MESSAGES["end_color"])

def main_func():
    print(MESSAGES["welcome"])

    while True:
        print(MESSAGES["options"])

        key = int(input("\n   Yapmak istediğiniz işlemi seçin: "))
        os.system('cls' if os.name == 'nt' else 'clear')

        if key == 1:
            get_data()
        elif key == 2:
            handle_data()
        elif key == 3:
            break

if __name__ == "__main__":
    main_func()
