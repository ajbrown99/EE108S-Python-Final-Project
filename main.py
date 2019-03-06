from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

login = open("data.txt", "r")
data = login.read().strip().split("\n")
user_, pass_ = data[0:2]
classes = data[2:]

driver = webdriver.Firefox()

driver.get("https://utdirect.utexas.edu/apps/registrar/course_schedule/20192")


def login():
    """
    Login sequence
    """

    if driver.title == "UT EID Login":
        username = driver.find_element_by_xpath("//input[@id='IDToken1']")
        password = driver.find_element_by_xpath("//input[@id='IDToken2']")
        loginbutton = driver.find_element_by_xpath("//input[@name='Login.Submit']")

        username.send_keys(user_)
        password.send_keys(pass_)
        loginbutton.click()


def createClasses():
    """
    Takes the user specified classes and instantiates them as objects.
    """
    classList = []
    for c in classes:
        # Waits until page loaded to retrieve dropdown
        dropDown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//select[@id='fos_cn']")))
        deptSelect = Select(dropDown)
        courseNumber = driver.find_element_by_xpath("//input[@id='course_number']")
        courseNumber.clear()
        submit = driver.find_elements_by_xpath("//div[@class='submit_button']/input")[4]
        department, number = c.split(" ")

        if len(department) == 2:
            department = department[0] + " " + department[1]
        for option in deptSelect.options:
            if department in option.text:
                deptSelect.select_by_visible_text(option.text)
                courseNumber.send_keys(number)
                submit.click()
                classList.append(instantiateClass())
                break
    return classList


def instantiateClass():
    sections = []

    # Waits until the sections have loaded
    classSections = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/td/a")))
    for section in classSections:
        sections.append(section.text)
    driver.back()
    return sections


if __name__ == "__main__":
    login()
    print(createClasses())
