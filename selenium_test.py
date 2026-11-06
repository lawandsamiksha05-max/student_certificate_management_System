from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://web.whatsapp.com")

input("Scan the QR code and press Enter...")

print("WhatsApp opened successfully!")

driver.quit()