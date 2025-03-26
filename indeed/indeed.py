from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import xlsxwriter 
                          
print("Enter a Job title")
user_name = input() 
driver = webdriver.Chrome()
driver.get("https://www.indeed.ca/")
element = driver.find_element_by_id("text-input-what")
element.send_keys(user_name)
element.send_keys(Keys.RETURN)
page_count = driver.find_element_by_id('searchCountPages').text
pagecount = int(page_count.replace(' ','').split('of')[1].split('jobs')[0].replace(',',''))
flag = True
next_page_old = ''
final_data = []


workbook = xlsxwriter.Workbook('IndeedJobs.xlsx') 
worksheet = workbook.add_worksheet()


worksheet.write(0, 0, "title")
worksheet.write(0, 1, "Url")
worksheet.write(0, 2, "Author")
worksheet.write(0, 3, "Location")
row = 1
      

while(flag):
	next_page = driver.find_elements_by_class_name("np")[-1]
	next_page_count = next_page.find_element_by_xpath('../..').get_attribute('href').split('start=')[1]
	if next_page_old:
		next_page_old_count = next_page_old.split('start=')[1]
		if int(next_page_count) <= int(next_page_old_count):
			flag = False
	jobs =  driver.find_elements_by_class_name("jobsearch-SerpJobCard")
	for job in jobs:
		job_title = job.find_elements_by_class_name('jobtitle')
		title =job_title[0].get_attribute('title')
		job_url = job_title[0].get_attribute('href')
		job_author = job.find_elements_by_class_name('company')
		job_location = job.find_elements_by_class_name('location')
	
		final_data.append({'title':title,'url':job_url,'author':job_author[0].text,'location':job_location[0].text})
		worksheet.write(row, 0, title)
		worksheet.write(row, 1, job_url)
		worksheet.write(row, 2, job_author[0].text)
		worksheet.write(row, 3, job_location[0].text)
		row += 1
	if('Next' in next_page.text or 'next' in next_page.text):
		next_page_old = next_page.find_element_by_xpath('../..').get_attribute('href')
		driver.get("%s"%next_page.find_element_by_xpath('../..').get_attribute('href'))

print("Final Data :: ",final_data)
workbook.close() 
driver.close()