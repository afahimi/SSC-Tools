from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass
from threading import Thread
import smtplib
from info import info



def checkGrade(driver: webdriver, grades: list[int]) -> None:
    #driver.navigate().refresh()
    url = driver.current_url
    while True:
        driver.get(url)
        WebDriverWait(driver, timeout=15).until(EC.frame_to_be_available_and_switch_to_it("iframe-main"))


        search = driver.find_element(
                        by=By.ID, value="allSessionsGrades")
        search = search.find_elements(
            by=By.XPATH, value="//tbody/tr/td[1]")
        
        for i in search:
            if i.text in grades:
                print("Grade found!")
                sendEmail(i.text)
                return

        time.sleep(1)



if __name__ == '__main__':
    username = info.username
    password = info.password
    grades = info.grades
    email = info.email
    # Open the browser and go to the SSC login page
    driver = webdriver.Chrome('./chromedriver.exe')
    #driver.get('https://ssc.adm.ubc.ca/')
    driver.get("https://cas.id.ubc.ca/ubc-cas/login?TARGET=https%3A%2F%2Fssc.adm.ubc.ca%2Fsscportal%2Fservlets%2FSSCMain.jsp%3Ffunction%3DSessGradeRpt")
    # element = driver.find_element(By.CLASS_NAME, 'span6')
    # btn = element.find_element(By.CSS_SELECTOR, 'a[href="/sscportal/servlets/SRVSSCFramework"]')
    # btn.click()

    # Enter the username and password
    while True:
        element = driver.find_element(By.ID, 'username')
        element.send_keys(username)
        element = driver.find_element(By.ID, 'password')
        password = getpass.getpass("Enter your password: ")
        element.send_keys(password)
        btn_login = driver.find_element(By.NAME, 'submit')
        btn_login.click()
        time.sleep(5)
        
        # Check if the login was successful
        if(driver.current_url.startswith("https://ssc.adm.ubc.ca/sscportal/servlets/")):
            break
        else:
            print("Incorrect username or password. Please try again.\n")
    

    print("Login successful!\n")

    # WebDriverWait(driver, timeout=15).until(
    # EC.frame_to_be_available_and_switch_to_it("iframe-main"))

    t1 = Thread(target=checkGrade, args=(driver, "CPEN 212"))
    t1.start()

    

    #go to grades page
    # grades_summary = driver.find_element(By.CSS_SELECTOR, 'a[href="SSCMain.jsp?function=SessGradeRpt"]')
    # grades_summary.click()

    #find the corresponding grade
    # code = input("Enter the course code (eg. CPEN): ")
    # course = input("Enter the course number (eg. 221): ")

    # time.sleep(5)
    # top = driver.find_element(By.CLASS_NAME, 'container')
    # next1 = top.find_element(By.ID, 'content-main')
    # iframe = next1.find_element(By.ID, 'iframe-main')
    # tabs = driver.find_element(By.CLASS_NAME, 'pageContent ui-tabs ui-widget ui-widget-content ui-corner-all')
    # search = driver.find_element(By.ID, "allSessionsGrades")
    # search = search.find_elements(By.XPATH, "//tbody/tr/td[1]")

    # all = driver.find_element(By.ID, 'tabs-all')
    # table = all.find_element(By.ID, 'allSessionsGrades')
    # entries = table.find_elements(By.CLASS_NAME, 'listRow')

    # count = 0

    # for entry in entries:
    #     print(entry.text + count)
    #     count += 1

    
    time.sleep(10)

