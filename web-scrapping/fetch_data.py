from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

# Path to the ChromeDriver executable
driver_path = "/home/joao/src/chromedriver-linux64/chromedriver"  # Correct path to the executable

# Configure Selenium WebDriver
options = Options()
options.add_argument("--headless")  # Run in headless mode (no browser window)
service = Service(driver_path)  # Use the full path to the executable
driver = webdriver.Chrome(service=service, options=options)

# Example usage
driver.get("https://fiis.com.br/resumo/")
print(driver.title)

# Wait until the page's JavaScript rendering is complete
wait = WebDriverWait(driver, 20)
wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

# Get the page source and parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Extract all rows from the table using BeautifulSoup
table = soup.find('table', class_='default-fiis-table__container__table')  # Find the table by its class
rows = []

# Extract the header
header = [th.text.strip() for th in table.find_all('th')]
rows.append(header)

# Extract data rows
for row in table.find_all('tr')[1:]:  # Skip the header row
    cells = [cell.text.strip() for cell in row.find_all('td')]
    if cells:
        print(rows)
        rows.append(cells)

# Save extracted data to a CSV file
with open("fiis_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(rows)

# Close the driver
driver.quit()

print("Data extracted and saved to fiis_data.csv")