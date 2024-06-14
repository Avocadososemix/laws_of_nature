from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

class law():
    def __init__(self):
        self.clause_number = "temp" # pykalä numero
        self.clause_title = "temp" # pykälä otsikko
        self.clause_text = "temp" # pykälä teksti


def save_page_source(page_source:str, output_file:str):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(page_source)


def process_page_source(page_source: str):
    law_list = []
    soup = BeautifulSoup(page_source, "html.parser")
    div_element = soup.find("div", id="document")
    if div_element:
        contents = div_element.contents
        substrings = []
        substrings = str(contents).split("</div><h5>") 
    
        for substring in substrings:
            new_law = law()
            start_index = substring.find(">") + 1
            end_index = substring.find("§")
            new_law.clause_number = substring[start_index:end_index].strip()
            
            if "<p>" in new_law.clause_number:
                continue
            
            start_index = substring.find('<h5 class="ot">') + len('<h5 class="ot">')
            end_index = substring.find('</h5>', start_index)
            new_law.clause_title = BeautifulSoup(substring[start_index:end_index].strip(), features="html.parser").get_text()

            start_index = substring.find('<p class="py">') + len('<p class="py">')
            end_index = substring.rfind('</p>', start_index)
            new_law.clause_text = BeautifulSoup(substring[start_index:end_index].strip(), features="html.parser").get_text()

            law_list.append(new_law)
            
        return law_list

    else:
        print("Div element with id 'document' not found")


def scrape_website(url):
    # Configure Chrome options
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode

    # Set path to chromedriver as per your configuration
    service = Service(ChromeDriverManager().install())

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        driver.implicitly_wait(10) # wait 10 seconds for page to load
        return driver.page_source

    except Exception as e:
        print("Failed to retrieve the webpage:", str(e))

    finally:
        driver.quit()


def main():
    url = "https://finlex.fi/fi/laki/ajantasa/2011/20110646?search%5Btype%5D=pika&search%5Bpika%5D=ymp%C3%A4rist%C3%B6"
    page_source = scrape_website(url)
    print("Scraping completed.")
    law_list = process_page_source(page_source)
    from contextlib import redirect_stdout
    with open('laws.txt', 'w', encoding='utf-8') as f:
        with redirect_stdout(f):
            for law in law_list:
                print(law.clause_number, "- ", law.clause_title, "\n", law.clause_text, "\n\n")
    
if __name__ == "__main__":
    main()