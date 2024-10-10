import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import time
from selenium.webdriver.common.keys import Keys
import sys
from collections import deque


contact1 = +6285187966052
contact2 = +6285187966050
# Path ke file daftar nomor dan balasan
RESPONSES_FILE = os.path.join(os.getcwd(), '../data/bola.json')

# Load messages from JSON file
def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        messages = json.load(file)
    return messages


# Fungsi untuk membaca kontak dari file
def read_contacts_from_file(file_path):
    with open(file_path, 'r') as file:
        contacts = [line.strip() for line in file if line.strip()]  # Membaca setiap baris dan menghapus whitespace
    return contacts

# Ambil message
messages = read_json_from_file(RESPONSES_FILE)

# Inisialisasi antrian untuk pesan
antrian = deque(messages)

# Inisialisasi dua driver (misalnya, Chrome) untuk dua akun WhatsApp
options1= Options()
options1.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver1 = webdriver.Chrome(options=options1)

options2= Options()
options2.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
driver2 = webdriver.Chrome(options=options2)

# Navigasi ke WhatsApp Web
driver1.get("https://web.whatsapp.com")
driver2.get("https://web.whatsapp.com")

# Tunggu hingga halaman WhatsApp Web terbuka
WebDriverWait(driver1, 30).until(
    EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Chat']"))
)
WebDriverWait(driver2, 30).until(
    EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Chat']"))
)

# Fungsi untuk mencari kontak berdasarkan nomor telepon
def search_contact(driver, phone_number):
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div/div/p"))
    )
    search_box.click()
    search_box.send_keys(phone_number)
    time.sleep(2)
    search_box.send_keys(Keys.RETURN)
    
# Fungsi untuk mengirim pesan
def send_message(driver, message):
    input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@aria-placeholder='Ketik pesan']"))
    )
    input_box.send_keys(message)
    input_box.send_keys(Keys.RETURN)

def akses_data():
    if antrian:
        return antrian.popleft()  # Ambil objek dari depan antrian
    else:
        print("Semua objek telah diakses.")
        sys.exit()  # Menghentikan aplikasi


while antrian:  # Selama masih ada pesan di antrian
    # Akun 1 mengirim pesan
    message = akses_data()  # Ambil pesan dari antrian
    search_contact(driver1, contact2)
    send_message(driver1, message)
    time.sleep(2)

    if not antrian:  # Periksa apakah antrian masih ada
        break  # Keluar dari loop jika tidak ada pesan tersisa

    # Akun 2 mengirim pesan (respon)
    message = akses_data()  # Ambil pesan dari antrian
    search_contact(driver2, contact1)
    send_message(driver2, message)
    time.sleep(2)

# Menutup driver setelah selesai
driver1.quit()
driver2.quit()
