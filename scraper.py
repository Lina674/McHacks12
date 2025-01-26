from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set up Chrome options
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")  # Disable GPU for headless (optional)


def get_title_prizes_companies(url):
    service = Service(r".\static\assets\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    driver.get(url)
    driver.implicitly_wait(10)

    title = driver.title.split(":")[0]
    

    prizes = driver.find_elements(By.CSS_SELECTOR, ".prize-title div")
    prize_titles = [prize.text for prize in prizes]

    #companies = driver.find_elements(By.CSS_SELECTOR, "article#judges i")
    #companies_text = [p.text for p in companies]

    image = driver.find_element(By.CSS_SELECTOR, ".header-image a img")
    image_src = image.get_attribute("src")

    driver.quit()
    # return (title, prize_titles, companies_text, image_src)
    return (title, prize_titles, image_src)



# t,p,c,i = get_title_prizes_companies("https://mchacks-12.devpost.com/?ref_feature=challenge&ref_medium=discover")
# print(t,c,p,i)

# driver.get("https://mcgill-physics-hackathon-2023.devpost.com/")
# driver.get("https://mchacks-12.devpost.com/?ref_feature=challenge&ref_medium=discover")
# driver.get("https://hack-mcwics-2025.devpost.com/?ref_feature=challenge&ref_medium=discover")