from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import getpass

if __name__ == '__main__':
    # Open the browser and go to the SSC login page
    driver = webdriver.Chrome('C:/Users/Feridoun/Documents/Personal Projects/chromedriver.exe')
    driver.get('https://ssc.adm.ubc.ca/')
    element = driver.find_element(By.CLASS_NAME, 'span6')
    btn = element.find_element(By.CSS_SELECTOR, 'a[href="/sscportal/servlets/SRVSSCFramework"]')
    btn.click()

    # Enter the username and password
    while True:
        username = input("Enter your CWL username: ")
        password = getpass.getpass('Enter your password: ')
        element = driver.find_element(By.ID, 'username')
        element.send_keys(username)
        element = driver.find_element(By.ID, 'password')
        element.send_keys(password)
        btn_login = driver.find_element(By.NAME, 'submit')
        btn_login.click()
        time.sleep(5)
        
        # Check if the login was successful
        if(driver.current_url == 'https://ssc.adm.ubc.ca/sscportal/servlets/SRVSSCFramework'):
            break
        else:
            print("Incorrect username or password. Please try again.\n")
    

    print("Login successful!\n")

    #go to grades page
    grades_summary = driver.find_element(By.CSS_SELECTOR, 'a[href="SSCMain.jsp?function=SessGradeRpt"]')
    grades_summary.click()

    #find the corresponding grade
    # code = input("Enter the course code (eg. CPEN): ")
    # course = input("Enter the course number (eg. 221): ")

    time.sleep(5)
    top = driver.find_element(By.CLASS_NAME, 'container')
    next1 = top.find_element(By.ID, 'content-main')
    iframe = next1.find_element(By.ID, 'iframe-main')
    tabs = iframe.find_element(By.ID, 'tabs')

    # all = driver.find_element(By.ID, 'tabs-all')
    # table = all.find_element(By.ID, 'allSessionsGrades')
    # entries = table.find_elements(By.CLASS_NAME, 'listRow')

    # count = 0

    # for entry in entries:
    #     print(entry.text + count)
    #     count += 1

    
    time.sleep(10)

