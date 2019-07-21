import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pyautogui
from tkinter import filedialog, Tk
import os
from selenium.webdriver.common.keys import Keys


class EasyApplyBot:

    MAX_APPLICATIONS = 30

    def __init__(self):
        self.options = self.browser_options()
        self.browser = webdriver.Chrome(chrome_options=self.options)
        self.start_linkedin()

    def browser_options(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("user-agent=Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393")
        return options

    def start_linkedin(self):
        self.browser.get("https://linkedin.com/login")
        self.browser.find_element_by_id('username').send_keys('')
        #insert email into the string here
        self.browser.find_element_by_id('password').send_keys('')
        #insert password into the string here
        self.browser.find_element_by_id('password').send_keys(Keys.RETURN)
        self.browser.get('https://www.linkedin.com/jobs/')

    def fill_data(self):
        self.browser.set_window_size(0, 0)
        self.browser.set_window_position(2000, 2000)
        os.system("reset")


        # position = input('Enter the desired job title : ')
        # self.position = position.replace(" ", "%20")
        self.position = "web%20developer"

        # print("Location codes: \n[1] GLOBAL\n[2] Country\n[3] State\n[4] City")
        # location_code = input('Enter the location code: ')
        # if location_code == "1":
        #     location = "Worldwide"
        # elif location_code == "2":
        #     location = input('Enter the country name: ')
        # elif location_code == "3":
        #     location = input('Enter the state name: ')
        # elif location_code == "4":
        #     location = input('Enter the city name: ')
        # self.location = "&location=" + location.replace(" ", "%20") + "&sortBy=DD"
        self.location = "&location=new%20york&sortBy=DD"

        # print("\nPlease select your curriculum\n")
        # time.sleep(1)
        # root = Tk()
        # self.resumeloctn = filedialog.askopenfilename(parent=root, initialdir="/",
                                                    #   title='Please select your curriculum')

        # root.destroy()

    def start_apply(self):
        self.fill_data()
        self.applications_loop()

    def applications_loop(self):
        count_application = 0
        count_job = 0
        jobs_per_page = 0

        os.system("reset")

        self.browser.set_window_position(0, 0)
        self.browser.maximize_window()
        self.browser, _ = self.next_jobs_page(jobs_per_page)

        while count_application < self.MAX_APPLICATIONS:
            # sleep to make sure everything loads, add random to make us look human.
            time.sleep(random.uniform(3.5, 6.9))

            page = BeautifulSoup(self.browser.page_source, 'lxml')

            jobs = self.get_job_links(page)

            if not jobs:
                print("Jobs not found")
                break

            for job in jobs:
                count_job += 1
                job_page = self.get_job_page(job)

                if self.got_easy_apply(job_page):
                    string_easy = "* has Easy Apply Button"
                    triggerButton = self.browser.find_element_by_class_name("jobs-apply-button--top-card")
                    time.sleep(0.5)
                    triggerButton.click()
                    time.sleep(1.5)
                    # self.send_resume()
                    submitButton = page.find("button", class_="jobs-apply-form__submit-button")
                    time.sleep(0.5)
                    hitSubmit = self.browser.find_element_by_class_name("jobs-apply-form__submit-button")
                    hitSubmit.click()
                    print("applied")

                    if submitButton:
                        time.sleep(0.5)
                        hitSubmit = self.browser.find_element_by_class_name("jobs-apply-form__submit-button")
                        hitSubmit.click()
                        string_easy=("applied")

                    else:
                        findcontinue = page.find("button", class_="continue-btn")

                        if findcontinue:
                            continuebutton = self.browser.find_element_by_class_name("continue-btn")
                            continuebutton.click()

                    count_application += 1

                else:
                    string_easy = "* Doesn't have Easy Apply Button"

                position_number = str(count_job + jobs_per_page)
                print(f"\nPosition {position_number}:\n {self.browser.title} \n {string_easy} \n")

                if count_job == len(jobs):
                    jobs_per_page = jobs_per_page + 25
                    count_job = 0
                    print("Going to next jobs page !")
                    self.avoid_lock()
                    self.browser, jobs_per_page = self.next_jobs_page(jobs_per_page)

        self.finish_apply()

    def get_job_links(self, page):
        links = []
        for link in page.find_all('a'):
            url = link.get('href')

            if url:
                if '/jobs/view' in url:
                    links.append(url)
        return set(links)

    def get_job_page(self, job):
        root = 'www.linkedin.com'
        if root not in job:
            job = 'https://www.linkedin.com'+job
        self.browser.get(job)
        self.job_page = self.load_page(sleep=0.5)
        return self.job_page

    def got_easy_apply(self, page):
        button = page.find("button", class_="jobs-apply-button--top-card artdeco-button--3 artdeco-button--primary jobs-apply-button artdeco-button ember-view")
        return len(str(button)) > 4

    def get_easy_apply_button(self):
        button_class = "jobs-apply-button--top-card artdeco-button--3 artdeco-button--primary jobs-apply-button artdeco-button ember-view"
        button = self.job_page.find("div", class_=button_class)
        triggerButton = self.browser.find_element_by_class_name("jobs-apply-button--top-card artdeco-button--3 artdeco-button--primary jobs-apply-button artdeco-button ember-view")
        time.sleep(0.5)
        triggerButton.click()
        time.sleep(1.5)


    # def easy_apply_xpath(self):
    #     button = self.get_easy_apply_button()
    #     button_inner_html = str(button)
    #     list_of_words = button_inner_html.split()
    #     next_word = [word for word in list_of_words if "ember" in word and "id" in word]
    #     ember = next_word[0][:-1]
    #     xpath = '//*[@'+ember+']/button'
    #     return xpath

    # def click_button(self, xpath):
    #     triggerDropDown = self.browser.find_element_by_xpath(xpath)
    #     time.sleep(0.5)
    #     triggerDropDown.click()
    #     time.sleep(1.5)

    # def send_resume(self):
    #     self.browser.find_element_by_xpath('//*[@id="file-browse-input"]').send_keys(self.resumeloctn)
    #     submit_button = None
    #     time.sleep(1)
    #     while not submit_button:
    #         if language == "en":
    #             submit_button = self.browser.find_element_by_xpath("//*[contains(text(), 'Submit application')]")
    #         elif language == "pt":
    #             submit_button = self.browser.find_element_by_xpath("//*[contains(text(), 'Enviar candidatura')]")
    #     submit_button.click()
    #     time.sleep(random.uniform(1.5, 2.5))

    def load_page(self, sleep=1):
        scroll_page = 0
        while scroll_page < 4000:
            self.browser.execute_script("window.scrollTo(0,"+str(scroll_page)+" );")
            scroll_page += 200
            time.sleep(sleep)

        if sleep != 1:
            self.browser.execute_script("window.scrollTo(0,0);")
            time.sleep(sleep * 3)

        page = BeautifulSoup(self.browser.page_source, "lxml")
        return page

    def avoid_lock(self):
        x, _ = pyautogui.position()
        pyautogui.moveTo(x+200, None, duration=1.0)
        pyautogui.moveTo(x, None, duration=0.5)
        pyautogui.keyDown('ctrl')
        pyautogui.press('esc')
        pyautogui.keyUp('ctrl')
        time.sleep(0.5)
        pyautogui.press('esc')

    def next_jobs_page(self, jobs_per_page):
        self.browser.get(
            "https://www.linkedin.com/jobs/search/?f_LF=f_AL&keywords=" +
            self.position + self.location + "&start="+str(jobs_per_page))
        self.avoid_lock()
        self.load_page()
        return (self.browser, jobs_per_page)

    def finish_apply(self):
        self.browser.close()


if __name__ == '__main__':
  
    bot = EasyApplyBot()
    bot.start_apply()
