import time
import smtplib
import sys
from selenium import webdriver

# use your credentials
username = "howdy-user-name-here"
password = "howdy-password-here"

# class details
subjectAbbreviation = sys.argv[1]
courseNumber = sys.argv[2]
sectionNumber = sys.argv[3]

# container for HTML elements
elems = { 'howdyHome' : "//*[@id='top']/div/div/div[1]/div[3]/input",
		  'usernameBox' : "//*[@id='username']",
          'passwordBox' : "//*[@id='password']",
          'loginButton' : "//*[@id='loginCol1']/div[3]/button",
          'recordTab' : "My Record",
          'addDropButton' : "Add or Drop Classes",
          'termSubmit' : "/html/body/div[3]/form",
          'classSearch' : "/html/body/div[3]/form/input[20]",
          'advancedSearch' : "//*[@id='advCourseBtnDiv']/input",
          'subjectAbbreviation' : "//*[@id='subj_id']/option[@value='" + subjectAbbreviation + "']",
          'courseNumberBox' : "//*[@id='crse_id']",
          'sectionSearch' : "//*[@id='advCourseBtnDiv']/input",
          'sectionNumber' : "",
          'numberRemaining' : ""
         }

browser = webdriver.Chrome()
baseurl = "https://howdy.tamu.edu"
browser.get(baseurl)

startTime = time.time()
timesChecked = 0
errorCount = 0
while (True) :
	try:
		browser.find_element_by_xpath(elems['howdyHome']).click()
		browser.find_element_by_xpath(elems['usernameBox']).send_keys(username)
		browser.find_element_by_xpath(elems['passwordBox']).send_keys(password)
		browser.find_element_by_xpath(elems['loginButton']).click()
		browser.find_element_by_link_text(elems['recordTab']).click()
		browser.find_element_by_link_text(elems['addDropButton']).click()
		browser.switch_to_frame("content")
		browser.find_element_by_xpath(elems['termSubmit']).submit()
		browser.find_element_by_xpath(elems['classSearch']).click()
		browser.find_element_by_xpath(elems['advancedSearch']).click()
		browser.find_element_by_xpath(elems['subjectAbbreviation']).click()
		browser.find_element_by_xpath(elems['courseNumberBox']).send_keys(courseNumber)
		browser.find_element_by_xpath(elems['sectionSearch']).click()

		row = 3;
		while (True) :
			elems['sectionNumber'] = "body > div.pagebodydiv > form > table > tbody > tr:nth-child(" + str(row) + ") > td:nth-child(5) > a"
			if (browser.find_element_by_css_selector(elems['sectionNumber']).get_attribute('innerHTML')
				== sectionNumber) :
				elems['numberRemaining'] = "body > div.pagebodydiv > form > table > tbody > tr:nth-child(" + str(row) + ") > td:nth-child(13)"
				break
			row += 1

		numRem = browser.find_element_by_css_selector(elems['numberRemaining']).get_attribute('innerHTML')
		if (int(numRem) > 0) :
			print("yippee")
			fromAddr = 'gmail-address-here'
			toAddr = 'gmail-address-here'
			message = 'A spot opened up in ' + subjectAbbreviation + ' ' + courseNumber + '. Go claim it!'
			password = 'gmail-password-here'
			server = smtplib.SMTP('smtp.gmail.com:587')
			server.starttls()
			server.login(fromAddr, password)
			server.sendmail(fromAddr, toAddr, message)
			server.quit()
			break

		browser.get(baseurl)
		timesChecked += 1
		averageTime = (time.time() - startTime) / timesChecked
		print("Times checked: " + str(timesChecked) + ". Error count: "
			+ str(errorCount) + ". Average time between checks: " + str(averageTime) + " seconds")
	except:
		browser.get(baseurl)
		errorCount += 1
		averageTime = (time.time() - startTime) / timesChecked
		print("Times checked: " + str(timesChecked) + ". Error count: "
			+ str(errorCount) + ". Average time between checks: " + str(averageTime) + " seconds")