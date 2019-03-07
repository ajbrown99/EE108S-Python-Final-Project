from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

from utclassobj import UTClass

import time
from getpass import getpass


login = open("data.txt", "r")
classes = [clazz.strip() for clazz in login.read().strip().split("\n")]

opts = Options()
opts.headless = True
driver = webdriver.Firefox(options=opts)

driver.get("https://utdirect.utexas.edu/apps/registrar/course_schedule/20192")


def login(un, pw):
    """
    Login sequence
    """

    if driver.title == "UT EID Login":
        userN = driver.find_element_by_xpath("//input[@id='IDToken1']")
        passW = driver.find_element_by_xpath("//input[@id='IDToken2']")
        loginButton = driver.find_element_by_xpath("//input[@name='Login.Submit']")

        userN.send_keys(un)
        passW.send_keys(pw)
        loginButton.click()


def createClasses():
    """
    Takes the user specified classes and instantiates them as objects.
    """
    classList = []
    for c in classes:

        # Waits until page loaded to retrieve dropdown
        dropDown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//select[@id='fos_cn']")))
        deptSelect = Select(dropDown)

        # Input for course number
        courseNumber = driver.find_element_by_xpath("//input[@id='course_number']")
        courseNumber.clear()

        # Submit button
        submit = driver.find_elements_by_xpath("//div[@class='submit_button']/input")[4]
        department, number = c.split(" ")

        # Parse the department string
        if len(department) == 2:
            department = department[0] + " " + department[1]

        # Find the department you are looking for
        for option in deptSelect.options:
            if department in option.text:
                deptSelect.select_by_visible_text(option.text)
                courseNumber.send_keys(number)
                submit.click()
                classList.append(instantiateClass())
                break
    return classList


def instantiateClass():
    """
    Instantiates a given section of a class
    """
    sections = []

    # Waits until the sections have loaded
    classSections = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr")))[1:]

    for section in classSections:

        unique = section.find_element_by_xpath(".//td[@data-th='Unique']/a").text

        days = section.find_elements_by_xpath(".//td[@data-th='Days']/span")
        hours = section.find_elements_by_xpath(".//td[@data-th='Hour']/span")
        times = [[elem.text for elem in days], [elem.text for elem in hours]]

        room = section.find_element_by_xpath(".//td[@data-th='Room']/span").text

        prof = section.find_element_by_xpath(".//td[@data-th='Instructor']").text

        status = section.find_element_by_xpath(".//td[@data-th='Status']").text

        newSection = UTClass(unique, times, room, prof, status)
        sections.append(newSection)

    driver.back()
    return sections


if __name__ == "__main__":
    username = input("Enter your username: ")
    password = getpass(prompt="Enter your password: ")
    print("Loading Classes...\n")
    login(username, password)
    # print(createClasses())
    clazz = createClasses()
    for cls in clazz:
        for sec in cls:
            print(str(sec))
