# Imports
import selenium
import selenium.common.exceptions
from ast import literal_eval
from html import unescape
from pyautogui import hotkey, write
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep


class SeleniumManager:
    driver: selenium.webdriver

    def __init__(self, driver: selenium.webdriver):
        self.driver = driver

    def login(self, username: str, password: str, link="https://www.datacamp.com/users/sign_in",
              timeout=15):
        '''
        Logs into datacamp.
        username: Username or email for login
        password: Corresponding password for login
        link: The URL of the login page
        timeout: How long before the program quits when it cannot locate an element
        '''

        self.driver.get(link)
        print("Website Loaded")

        # Username find and enter
        try:
            user_log = WebDriverWait(self.driver, timeout=timeout).until(lambda d: d.find_element(By.ID, "user_email"))
            user_log.send_keys(username)
            print("Username Entered")
        except selenium.common.exceptions.ElementNotInteractableException:  # Might not be necessary
            print("Username Error")
            return
        except selenium.common.exceptions.TimeoutException:
            print("Username Field Timed Out Before Found")
            return

        # Next button click
        self.driver.find_element(By.XPATH, '//*[@id="new_user"]/button').click()
        sleep(0.2)  # Might not be necessary
        print("Clicked Next")

        # Password find and enter
        try:
            user_pass = WebDriverWait(self.driver, timeout=timeout).until(
                lambda d: d.find_element(By.ID, "user_password"))
            user_pass.send_keys(password)
            print("Password Entered")
        except selenium.common.exceptions.ElementNotInteractableException:
            print("Password Error")
            return
        except selenium.common.exceptions.TimeoutException:
            print("Password Field Timed Out Before Found")
            return

        # Sign in button click
        self.driver.find_element(By.XPATH, '//*[@id="new_user"]/div[1]/div[3]/input').click()
        print("Signed In")

        # Finds the user profile to ensure that the login was registered
        try:
            WebDriverWait(self.driver, timeout=timeout) \
                .until(lambda d: d.find_element(By.XPATH,
                                                '//*[@id="single-spa-application:@dcmfe/mfe-app-atlas-header"]/nav/div[4]/div[2]/div/button'))
            print("Sign In Successful")
        except selenium.common.exceptions.TimeoutException:
            print("Error Verifying Sign In")

    def get_solutions(self, link: str) -> list:
        '''
        Uses a datacamp assignment link to get all the solutions for a chapter
        link: The URL of the page
        '''
        self.driver.get(link)
        script = self.driver.find_element(By.XPATH, "/html/body/script[1]").get_attribute("textContent")
        script = unescape(script)
        solutions = []
        for segment in script.split(",["):
            if ',"solution",' in segment and '"type","NormalExercise","id"' in segment:
                # Slices solution from src code
                solution = segment[segment.find('"solution","') + 12: segment.find('","type"')]
                # Formats solution into usable strings/code
                solution = literal_eval('"' + unescape(literal_eval('"' + solution + '"')) + '"')
                solutions.append(solution)
                #print(segment)
        return solutions

    # TODO: If possible identify the exercise by the page's responses
    # Might be easier just to try every answer
    def get_first_solution(self, solutions: list):
        pass

    # Clicks the got it button
    def solve_video_exercise(self, timeout: int) -> bool:
        solved_exercise = False
        try:
            got_it_button = WebDriverWait(self.driver, timeout=timeout) \
                .until(lambda d: d.find_element(By.XPATH, '//*[@id="root"]/div/main/div[1]/section/div[2]/button[2]'))
            got_it_button.click()
            print("Got it button clicked")
            solved_exercise = True
            return solved_exercise
        except selenium.common.exceptions.TimeoutException:
            print("Got it button not found before timeout, most likely was not a video exercise")
            return solved_exercise

    # Clicks on the python script, doing ctrl + a, inputting the solution, clicking the next button
    def solve_normal_exercise(self, solution: str, timeout: int) -> bool:
        solved_exercise = False
        try:
            script_textfield = WebDriverWait(self.driver, timeout=timeout) \
                .until(lambda d: d.find_element(By.XPATH, '//*[@id="gl-editorTabs-files/script.py"]/div/div/div[1]/div/div/div[1]/div[2]/div[1]/div[4]'))
            script_textfield.click()
            print("Got it button clicked")
            hotkey("ctrl", "a")
            write(solution)
        except selenium.common.exceptions.TimeoutException:
            print("Python script not found, most likely not a normal exercise")
            return solved_exercise

        try:
            submit_answer_button = WebDriverWait(self.driver, timeout=timeout) \
                .until(lambda d: d.find_element(By.XPATH, '//*[@id="gl-editorTabs-files/script.py"]/div/div/div[2]/div[2]/button[3]'))
            sleep(3)  # Might not be necessary TODO: Fix this
            submit_answer_button.click()
            print("Submit Answer button clicked")
            solved_exercise = True
            return solved_exercise
        except selenium.common.exceptions.ElementNotInteractableException:
            print("Submit Answer button couldn't be clicked")
        except selenium.common.exceptions.TimeoutException:
            print("Submit Answer button not found, most likely not a normal exercise")
            return solved_exercise

    def solve_tab_exercises(self, solutions: list, timeout: int):
        pass

    def solve_multiple1(self, timeout: int):
        pass

    # There are different multiple choice problems, this one has the python script open with it
    def solve_multiple2(self, timeout: int):
        solved_exercise = False
        try:
            # Gets the length of the child elements (the multiple choice options) in the parent element
            multiple_choice_options = len(self.driver.find_elements_by_xpath('//*[@id="gl-aside"]/div/aside/div/div/div/div[2]/div[2]/div/div/div[2]/ul/*'))
            for i in range(0, multiple_choice_options):
                radio_input_button = WebDriverWait(self.driver, timeout=3) \
                    .until(lambda d: d.find_element(By.XPATH, f'//*[@id="gl-aside"]/div/aside/div/div/div/div[2]/div[2]/div/div/div[2]/ul/li[{i + 1}]/div/div/label'))
                radio_input_button.click()
                print("Clicked a radio button")
                try:
                    submit_button = WebDriverWait(self.driver, timeout=3) \
                        .until(lambda d: d.find_element(By.XPATH, '//*[@id="gl-aside"]/div/aside/div/div/div/div[2]/div[2]/div/div/div[2]/div/div[1]/button'))
                    submit_button.click()
                    print("Clicked the submit button")
                    continue_button = WebDriverWait(self.driver, timeout=5) \
                        .until(lambda d: d.find_element(By.XPATH, '//*[@id="gl-aside"]/div/aside/div[2]/div/div[3]/button'))
                    continue_button.click()
                    print("Clicked the continue button")
                    solved_exercise = True
                    return solved_exercise
                except selenium.common.exceptions.ElementNotInteractableException:
                    print("Continue or submit button couldn't be clicked")
                except selenium.common.exceptions.TimeoutException:
                    print("Continue or submit button not found")
                sleep(1)  # Might not be necessary
        except selenium.common.exceptions.ElementNotInteractableException:
            print("Radio input button couldn't be clicked")
            return solved_exercise
        except selenium.common.exceptions.TimeoutException:
            print("Radio input button not found, most likely not a multiple choice exercise")
            return solved_exercise

# Legacy methods
# def get_page_source(driver: selenium.webdriver, link: str) -> str:
#     '''
#     Returns the full HTML page source of a given link.
#     driver: Any selenium webdriver
#     link: The URL of the page
#     '''
#     driver.get(link)
#     return driver.page_source

# def get_page_ids(self, link: str) -> list:
#     '''
#     Uses a datacamp assignment link to get all the required IDs for an API lookup
#     driver: Any selenium webdriver
#     link: The URL of the page
#     '''
#     self.driver.get(link)
#
#     script = self.driver.find_element(By.XPATH, "/html/body/script[1]").get_attribute("textContent")
#     script = html.unescape(script)
#     ids = []
#     for p in script.split("],"):
#         if '"NormalExercise",' in p and '"id",' in p:
#             i_start = p.find('"id",') + 5
#             i_end = p[i_start:].find(",")
#             if i_end == -1: i_end = p[i_start:].find("]")
#             id = p[i_start:i_end + i_start]
#             ids.append(int(id))
#
#     return list(np.unique(ids))
#
# def api_lookup(self, ids: list,
#                api_link="https://campus-api.datacamp.com/api/exercises/{}/get_solution") -> list:
#     '''
#     Looks up a list of IDs and returns the API solution.
#     driver: Any selenium webdriver
#     ids: All IDs that will be looked up
#     api_link: A formattable string with place for an ID
#     '''
#     pages = []
#     for id in ids:
#         self.driver.get(api_link.format(id))
#         source = self.driver.find_element(By.XPATH, "/html/body/pre")
#         element = literal_eval(source.get_attribute("textContent"))
#         solution = html.unescape(element["solution"])
#         pages.append(solution)
#
#     return pages
