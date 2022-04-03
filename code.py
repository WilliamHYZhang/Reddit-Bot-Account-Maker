from selenium import webdriver
from random import randint
from random import choice
from datetime import date
import requests
import string
import time
import names
import os
import re
def Find(string): 
    # findall() has been used  
    # with valid conditions for urls in string 
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
    return url 

def generateUser():
	#generates random username/password
	username = names.get_first_name()
	username += ''.join(str(randint(0,9))for i in range(randint(5,15)))
	password = ''.join(choice(string.ascii_letters+string.digits) for i in range(randint(10,20)))

	return username, password

def createAccount(username, password):
	profile = webdriver.FirefoxProfile()
	profile.set_preference("network.proxy.type", 1)
	profile.set_preference("network.proxy.socks", '127.0.0.1')
	profile.set_preference("network.proxy.socks_port", 9050)
	profile.set_preference("network.proxy.socks_remote_dns", True)
	profile.set_preference("browser.privatebrowsing.autostart", True)
	profile.update_preferences()
	driver = webdriver.Firefox(firefox_profile=profile)
	emailDriver = webdriver.Firefox(firefox_profile=profile)
	try:
		print('Creating account with username: ' + username + ' and password: ' + password + '...')

		print('Clearing all cookies...')
		driver.delete_all_cookies()

		print('Setting up anonymous web identity...')
		driver.get("https://old.reddit.com/register")

		print('Entering in username...')
		time.sleep(randint(1,5))
		driver.find_element_by_id('user_reg').click()
		driver.find_element_by_id('user_reg').send_keys(username)

		print('Entering in password...')
		time.sleep(randint(1,5))
		driver.find_element_by_id('passwd_reg').click()
		driver.find_element_by_id('passwd_reg').send_keys(password)

		print('Entering in password...')
		time.sleep(randint(1,5))
		driver.find_element_by_id('passwd2_reg').click()
		driver.find_element_by_id('passwd2_reg').send_keys(password)

		print('Retreiving email...')
		emailDriver.get('https://getnada.com')
		email = emailDriver.find_element_by_xpath('/html/body/div/div/div/div/div[2]/div/div[1]/div/div/p/span[1]/a/button').text

		print('Entering email...')
		driver.find_element_by_id('email_reg').send_keys(email)

		print('Solving captcha...')
		time.sleep(randint(10,15))
		apiKey = '' #Add your API key here!
		siteKey = '6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-JC'
		pageUrl = 'https://old.reddit.com/register'
		requestUrl = 'https://2captcha.com/in.php?key='+apiKey+'&method=userrecaptcha&googlekey='+siteKey+'&pageurl='+pageUrl
		print('Requesting 2captcha API...')
		resp = requests.get(requestUrl)
		if(resp.text[0:2] != 'OK'):
			print('Service error has occured. Error code: '+resp.text)
			return 
		captchaId = resp.text[3:]
		print('Submitted request successfully, waiting for 30 seconds until requesting return...')
		time.sleep(30)
		returnUrl = 'https://2captcha.com/res.php?key='+apiKey+'&action=get&id='+captchaId
		print('Requesting return...')
		resp = requests.get(returnUrl)
		if resp.text == 'CAPCHA_NOT_READY':
			while resp.text == 'CAPCHA_NOT_READY':
				print('Captcha is not ready, requesting again in 5 seconds...')
				time.sleep(5)
				resp = requests.get(returnUrl)
		elif resp.text[0:5] == 'ERROR':
			print('Service error has occured. Error code: '+resp.text)
			return
		ansToken = resp.text[3:]
		if ansToken == 'OR_CAPCHA_UNSOLVABLE':
			print('Service error has occured. Error code: '+resp.text)
			return
		print('Answer token recieved: '+ansToken)

		captchaInput = driver.find_element_by_id('g-recaptcha-response')
		driver.execute_script("arguments[0].setAttribute('style','visibility:visible;');", captchaInput)
		captchaInput.send_keys(ansToken)

		print('Submitting token')
		driver.find_element_by_xpath('/html/body/div[3]/div/div/div[1]/form/div[8]/button').click()

		print('Checking email...')
		time.sleep(15)
		emailDriver.get('https://getnada.com')
		time.sleep(15)
		emailDriver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/ul/li').click()
		time.sleep(15)
		frame = emailDriver.find_element_by_id('idIframe')
		emailDriver.switch_to.frame(frame)
		emailText = emailDriver.find_element_by_xpath('/html/body').text
		link = Find(emailText)
		link = link[0]
		print(link)
		emailDriver.switch_to.default_content()
		print('Verifying email...')
		print('Going to '+link+'...')
		driver.get(link)
		time.sleep(10)
		driver.get('https://old.reddit.com')
		print('Viewing reddit inbox...')
		driver.find_element_by_id('mail').click()
		time.sleep(5)

		print('Writing account info to file...')
		with open('accounts.out', 'a') as fout:
			fout.write('Date: '+str(date.today())+' '+username+' '+password+' '+email+'\n')

		print('Successfully created account!')
		driver.delete_all_cookies()
		print('Clearing cookies...')
		time.sleep(5)
		driver.close()
		emailDriver.close()
		return
	except:
		print('Error. Trying again...')
		driver.close()
		emailDriver.close()
		time.sleep(120)
		createAccount(username, password)
		return

def main():
	times = int(input('Enter number of accounts. \n'))
	for i in range(times):
		username, password = generateUser()
		os.system('service tor restart')
		createAccount(username, password)
		print('System cooldown')
		time.sleep(300)
main()
