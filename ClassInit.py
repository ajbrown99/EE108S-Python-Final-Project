from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from selenium.common.exceptions import TimeoutException, NoSuchElementException

from ClassObj import UTClass


class ClassGetter:
    def __init__(self):
        login = open("data.txt", "r")
        self.classes = [clazz.strip() for clazz in login.read().strip().split("\n")]

        opts = Options()
        opts.headless = True
        self.driver = webdriver.Firefox(options=opts)

        self.driver.get("https://utdirect.utexas.edu/apps/registrar/course_schedule/20192")

    def login(self, un, pw):
        """
        Login sequence
        """

        if self.driver.title == "UT EID Login":
            userN = self.driver.find_element_by_xpath("//input[@id='IDToken1']")
            passW = self.driver.find_element_by_xpath("//input[@id='IDToken2']")
            loginButton = self.driver.find_element_by_xpath("//input[@name='Login.Submit']")

            userN.send_keys(un)
            passW.send_keys(pw)
            loginButton.click()

    def createClasses(self):
        """
        Takes the user specified classes and instantiates them as objects.
        """
        classList = []
        for c in self.classes:

            # Waits until page loaded to retrieve dropdown
            dropDown = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//select[@id='fos_cn']")))
            deptSelect = Select(dropDown)

            # Input for course number
            courseNumber = self.driver.find_element_by_xpath("//input[@id='course_number']")
            courseNumber.clear()

            # Submit button
            submit = self.driver.find_elements_by_xpath("//div[@class='submit_button']/input")[4]
            department, number = c.split(" ")

            # Parse the department string
            if len(department) == 2:
                department = department[0] + " " + department[1]

            # Find the department you are looking for
            for option in deptSelect.options:
                if department == option.text.split("-")[0].strip():
                    deptSelect.select_by_visible_text(option.text)
                    courseNumber.send_keys(number)
                    submit.click()
                    classSectionObject = self.instantiateClass(department + " " + number)
                    if classSectionObject:
                        classList.append(classSectionObject)
                    break
        return classList

    def instantiateClass(self, classNameNumber):
        """
        Instantiates all sections of a given class
        """
        sections = []

        # Waits until the sections have loaded
        try:
            classSections = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr")))[1:]
        except (TimeoutException, NoSuchElementException):
            print("No sections available for " + classNameNumber + ".\n")
            self.driver.back()
            return

        for section in classSections:

            try:
                unique = section.find_element_by_xpath(".//td[@data-th='Unique']/a").text

                days = section.find_elements_by_xpath(".//td[@data-th='Days']/span")
                hours = section.find_elements_by_xpath(".//td[@data-th='Hour']/span")
                times = [[elem.text for elem in days], [elem.text for elem in hours]]

                room = section.find_element_by_xpath(".//td[@data-th='Room']/span").text

                prof = section.find_element_by_xpath(".//td[@data-th='Instructor']").text

                status = section.find_element_by_xpath(".//td[@data-th='Status']").text

                newSection = UTClass(classNameNumber, unique, times, room, prof, status)
                sections.append(newSection)
            except (TimeoutException, NoSuchElementException):
                continue

        self.driver.back()
        return sections
