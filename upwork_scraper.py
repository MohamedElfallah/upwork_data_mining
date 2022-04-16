from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common import keys
from selenium.webdriver.chrome.options import Options
import json


class Freelancer():
    def __init__(self, country, hourly_price, total_earning, hourly_jobs, fixed_price_jobs, hours_worked, job_success, description, category):
        self.country = country,
        self.hourly_price = hourly_price
        self.total_earning = total_earning
        self.hourly_jobs = hourly_jobs
        self.fixed_price_jobs = fixed_price_jobs
        self.hours_worked = hours_worked
        self.job_success = job_success
        self.description = description
        self.category = category

    def __str__(self):
        json_rep = {"country": self.country, "hourly_price": self.hourly_price, "total_earning": self.total_earning, "hourly_jobs": self.hourly_jobs,
                    "fixed_price_jobs": self.fixed_price_jobs, "hours_worked": self.hours_worked, "job_success": self.job_success, "description": self.description, "category": self.category}
        return json.dumps(json_rep)


# Mapping categories and their ID (ID passed as a parameter in request sent to server)
categories = {"Accounting & Consulting": 531770282584862721,
              "Admin Support": 531770282580668416,
              "Data Science & Analytics": 531770282580668420,
              "Design & Creative": 531770282580668421,
              "Engineering & Architecture": 531770282584862722,
              "IT & Networking": 531770282580668419,
              "Legal": 531770282584862723,
              "Sales & Marketing": 531770282580668422,
              "Translation": 531770282584862720,
              "Web, Mobile & Software Dev": 531770282580668418,
              }

if __name__ == "__main__":
    for category_ in categories:
        for page in range(1, 51):
            s = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=s)
            driver.get(
                f"https://www.upwork.com/search/profiles/?category_uid={categories[category_]}&page={page}")
            driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, features="lxml")
            cards = soup.find_all(
                "div", class_="up-card-section up-card-hover")
            for card in cards:
                hourly_jobs_ = ""
                fixed_price_jobs_ = ""
                hours_worked_ = ""
                try:
                    container = card.find("div", class_="profile-stats mb-10")
                    parent = container.find("div", class_="popper-content").div
                    children = parent.findChildren("p")
                    hourly_jobs_, fixed_price_jobs_, hours_worked_ = [
                        child.text for child in children]
                except:
                    pass
                total_earning_ = ""
                job_success_ = ""
                try:
                    container = card.find("div", class_="profile-stats mb-10")
                    total_earning_ = container.find(
                        "p", class_="mb-0").strong.text
                except:
                    pass
                try:
                    container = card.find("div", class_="profile-stats mb-10")
                    job_success_ = container.find(
                        "div", class_="up-job-success-bar").span.text
                except:
                    pass
                freelancer = Freelancer(
                    country=card.find(
                        "span", class_="d-inline-block vertical-align-middle").text,
                    hourly_price=card.find(
                        "div", class_="grid-col-1 grid-col-sm-1 justify-self-start nowrap").strong.span.text,
                    hourly_jobs=hourly_jobs_,
                    fixed_price_jobs=fixed_price_jobs_,
                    hours_worked=hours_worked_,
                    total_earning=total_earning_,
                    job_success=job_success_,
                    description=card.find(
                        "div", class_="up-line-clamp-v2 clamped").text,
                    category=category_,
                )
                with open("data5.json", "a") as file:
                    file.write(str(freelancer)+",\n")
            driver.quit()
            print(f"processed category: {category_}  & page:{page} ")
            time.sleep(60)
