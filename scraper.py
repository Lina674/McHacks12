from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


service = Service(r"C:\Users\linag\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")

driver = webdriver.Chrome(service=service)

driver.get('https://dawhacks2024.devpost.com/')
# driver.get("https://mcgill-physics-hackathon-2023.devpost.com/")
# driver.get("https://mchacks-12.devpost.com/?ref_feature=challenge&ref_medium=discover")
# driver.get("https://hack-mcwics-2025.devpost.com/?ref_feature=challenge&ref_medium=discover")

driver.implicitly_wait(10)

title = driver.title.split(":")[0]
print(title)

prizes = driver.find_elements(By.CSS_SELECTOR, ".prize-title div")

prize_titles = [prize.text for prize in prizes]
print(prize_titles)

# for title in prize_titles:
#     print(title)

companies = driver.find_elements(By.CSS_SELECTOR, "article#judges i")
companies_text = [p.text for p in companies]
print(companies_text)

driver.quit()
