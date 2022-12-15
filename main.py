import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import time

links = []
job_titels = []
salarys = []
skils_f = []

page_count = 0

while True:

    resu = requests.get(f'https://www.freelancer.com/jobs/python/{page_count}/')

    sr = resu.content
    soup = BeautifulSoup(sr,'lxml') 
    
    count = soup.find("span",{"id":"total-results"})
    if page_count > (int(count.text) // 50):
        break
    job_titel = soup.find_all("a",{"class":"JobSearchCard-primary-heading-link"})
    #salary = soup.find_all("div",{"class":"JobSearchCard-secondary-price"})
    d = soup.find_all("div",{"class":"JobSearchCard-primary-heading"})

    for i in range(len(job_titel)):
        
        
        job_titels.append(job_titel[i].text.strip())
        
        links.append('https://www.freelancer.com'+d[i].find("a").attrs['href'])
    page_count += 1
    print('Page Switched')

for link in links:
    
    try:
            
        resu = requests.get(link)

        sr = resu.content
        
        soup = BeautifulSoup(sr,'lxml') 

        salary = soup.find("p",{"class":"PageProjectViewLogout-header-byLine"})

        skils_req = soup.find("p",{"class":"PageProjectViewLogout-detail-tags"})
        skills_text = ""
        for a in skils_req.find_all("a"):
            skills_text += a.text+" - "
        final_salarys = salary.text.strip().replace("Budget","")
        salarys.append(final_salarys.strip().replace("\n",""))
        skils_f.append(skills_text)
    except:
        pass

file_list = [job_titels,salarys,skils_f,links]

exported = zip_longest(*file_list)

with open("freelancer.csv","w") as myfile:
    wr = csv.writer(myfile)
    #Create Rows Title
    wr.writerow(["job title","Salarys", "SKils", "links"])
    #Append Info TO myfile
    wr.writerows(exported)