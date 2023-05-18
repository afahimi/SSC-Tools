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
from flask import Flask
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# def sendEmail(course: str, grade: str, email: str) -> None:
#     # Set up the browser
#     browser = webdriver.Chrome('C:/Users/Feridoun/Documents/Personal Projects/chromedriver.exe')
#     browser.get('https://mail.protonmail.com/login')

#     time.sleep(5)

#     # Log in
#     email_input = browser.find_element(By.CLASS_NAME, 'field-two-container field-two--bigger')
#     email_input.send_keys('ssc.scripts@proton.me')
#     password_input = browser.find_element_by_name('password')
#     password_input.send_keys('ssc.scripts123123')
#     password_input.send_keys(Keys.RETURN)

#     # Compose the email
#     compose_button = browser.find_element_by_xpath('//div[contains(text(), "Compose")]')
#     compose_button.click()
#     to_input = browser.find_element_by_name('to')
#     to_input.send_keys(email)
#     subject_input = browser.find_element_by_name('subject')
#     subject_input.send_keys(f'Grade Notification for {course}')
#     body_input = browser.find_element_by_xpath('//div[@aria-label="Message Body"]')
#     body_input.send_keys(f'Dear Student,\n\nYour grade for the course {course} has been released. Your grade is: {grade}.\n\nThank you.')
#     send_button = browser.find_element_by_xpath('//button[@title="Send"]')
#     send_button.click()

#     # Close the browser
#     browser.quit()

def sendEmail(course: str, grade: str, email: str) -> None:
    sender_email = 'ssc.scripts@gmail.com'
    sender_password = 'dsscbrbrmdwtcojo'
    recipient_email = email

    subject = f'Grade Notification for {course}'
    message = f'''Dear Student,

Your grade for the course {course} has been released. Your grade is: {grade}.

You can find your grade on the SSC website: https://cas.id.ubc.ca/ubc-cas/login?TARGET=https%3A%2F%2Fssc.adm.ubc.ca%2Fsscportal%2Fservlets%2FSSCMain.jsp%3Ffunction%3DSessGradeRpt

This email is automated. Please do not reply.

Thank you.
'''

    # Create a multipart message and set headers
    email = MIMEMultipart()
    email['From'] = sender_email
    email['To'] = recipient_email
    email['Subject'] = subject

    # Add the message body to the email
    email.attach(MIMEText(message, 'plain'))

    # Send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(email)
        print(f'Email sent successfully to {recipient_email}.')
    except smtplib.SMTPException as e:
        print(f'Error sending email to {recipient_email}: {e}')





def checkGrade(driver: webdriver, grades: list[int], email) -> None:
    url = driver.current_url
    count = 0
    while True:
        driver.get(url)
        WebDriverWait(driver, timeout=15).until(EC.frame_to_be_available_and_switch_to_it("iframe-main"))


        search = driver.find_element(
                        by=By.ID, value="allSessionsGrades")
        search = search.find_elements(
            by=By.XPATH, value="//tbody/tr/td[1]")
        print("searching for: " + str(grades) + " " + str(count))
        
        for i in search:
            if i.text in grades:
                parent = i.find_element(by=By.XPATH, value="..")
                grade = parent.find_element(by=By.XPATH, value="td[3]")
                if not(grade.text == " " or grade.text == ""):
                    print("found grade")
                    grades.remove(i.text)
                    sendEmail(i.text, grade.text, email)
                    count = 0
                    if len(grades) == 0:
                        return
        count += 1
        time.sleep(1)


# Usage example
# course = 'Mathematics'
# grade = 'A'
# recipient_email = 'amin.f1000@gmail.com'
# sendEmail(course, grade, recipient_email)


if __name__ == '__main__':
    username = info.username
    password = info.password
    grades = info.grades
    email = info.email
    # Open the browser and go to the SSC login page
    driver = webdriver.Chrome('C:/Users/Feridoun/Documents/Personal Projects/chromedriver.exe')
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

    t1 = Thread(target=checkGrade, args=(driver, grades, email))
    t1.start()

    
    time.sleep(10)

