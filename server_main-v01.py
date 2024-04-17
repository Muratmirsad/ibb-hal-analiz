import csv
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



MESSAGES = {
    "welcome": "\n-----       server-0.2       -----\n'''\nCreated Date: Saturday, April 15th 2023\nLast Update: April 17th 2024\nProgram Name: server_main.py\nAuthor: Murat Mirsad Dırağa\n\n            github.com/muratmirsad\n'''\n\n",
    "file_created": "\n{}.csv created.\n",
    "file_comparison": "{} - {}\n\nFiyat değişimleri",
    "product_change": "\nÜrün: {}",
    "price_change": "",
    "end_color": "",
    "mail_sent": "\nEmail sent!"
}

def display_message(message_key, *args):
    print(MESSAGES[message_key].format(*args))

def get_data():
    get_day = datetime.today()
    day = get_day.strftime("%Y-%m-%d")
    
    url_fruit = f"https://tarim.ibb.istanbul/inc/halfiyatlari/gunluk_fiyatlar.asp?tarih={day}&kategori=5&tUsr=M3yV353bZe&tPas=LA74sBcXERpdBaz&tVal=881f3dc3-7d08-40db-b45a-1275c0245685&HalTurId=2"
    url_vegetable = f"https://tarim.ibb.istanbul/inc/halfiyatlari/gunluk_fiyatlar.asp?tarih={day}&kategori=6&tUsr=M3yV353bZe&tPas=LA74sBcXERpdBaz&tVal=881f3dc3-7d08-40db-b45a-1275c0245685&HalTurId=2"

    response = requests.get(url_fruit)
    soup = BeautifulSoup(response.text, "html.parser")
    data_table = soup.find("table")

    with open(f"{day}_meyve.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        headers = [header.text.strip() for header in data_table.find_all("th")]
        writer.writerow(headers)

        for row in data_table.find_all("tr"):
            row_data = [cell.text.strip() for cell in row.find_all("td")]
            if row_data:
                writer.writerow(row_data)
    display_message("file_created", day)

    response = requests.get(url_vegetable)
    soup = BeautifulSoup(response.text, "html.parser")
    data_table = soup.find("table")

    with open(f"{day}_sebze.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        headers = [header.text.strip() for header in data_table.find_all("th")]
        writer.writerow(headers)

        for row in data_table.find_all("tr"):
            row_data = [cell.text.strip() for cell in row.find_all("td")]
            if row_data:
                writer.writerow(row_data)
    display_message("file_created", day)

def handle_data():
    get_day = datetime.today()
    day = get_day.strftime("%Y-%m-%d")


    low_prices_1, high_prices_1, low_prices_2, high_prices_2 = [], [], [], []
    price_changes, products = [], []

    array_tmp = ["fiyat_degisiklikleri_meyve.txt", "fiyat_degisiklikleri_sebze.txt", "_meyve", "_sebze"]

    for i in range(2):
        file_1 = day + array_tmp[i + 2] + ".csv"
        file_2 = "2024-03-14" + array_tmp[i + 2] + ".csv" #"2024-3-13" + ".csv" #! YAPILMADI
    
        with open(array_tmp[i], "w") as f:
            f.write(MESSAGES["file_comparison"].format(file_1, file_2) + "\n")

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
                    f.write(MESSAGES["product_change"].format(product_name) + "\n")
                    f.write("Düşük fiyat farkı: " + str(low_price_change) + "\n")
                if high_price_change != 0:
                    f.write(MESSAGES["product_change"].format(product_name) + "\n")
                    f.write("Yüksek fiyat farkı: " + str(high_price_change) + "\n")

def read_env_file(filename):
    with open(filename, "r") as file:
        for line in file:
            key, value = line.strip().split("=")
            os.environ[key] = value

def send_email():
    read_env_file(".env")

    sender_email = os.environ.get("SENDER_MAIL")
    sender_password = os.environ.get("SENDER_PASS")
    receiver_email = os.environ.get("RECEIVER_MAIL")
    smtp_server = os.environ.get("SMTP_SERVER")
    smtp_server_port = os.environ.get("SMTP_SERVER_PORT")

    print("SENDER_MAIL:", sender_email)
    print("SENDER_PASS:", sender_password)
    print("RECEIVER_MAIL:", receiver_email)
    print("SMTP_SERVER:", smtp_server)
    print("SMTP_SERVER_PORT:", smtp_server_port)

    server = smtplib.SMTP(smtp_server, smtp_server_port)
    server.starttls()
    server.login(sender_email, sender_password)

    subject = "Fiyat Değişiklikleri"
    array_tmp = ["fiyat_degisiklikleri_meyve.txt", "fiyat_degisiklikleri_sebze.txt"]

    for i in range(2):
        with open(array_tmp[i], "r") as file:
            body = file.read()

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        server.sendmail(sender_email, receiver_email, message.as_string())

    print(MESSAGES["mail_sent"])

    server.quit()

def main_func():
    print(MESSAGES["welcome"])

    get_data()
    handle_data()
    send_email()

if __name__ == "__main__":
    main_func()
