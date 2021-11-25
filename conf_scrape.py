import json
import requests
from bs4 import BeautifulSoup
import time

class Connection:
    def __init__(self):
        self.session=requests.Session()
    def connect(self,url):
        try:
            response=self.session.get(url)
        except Exception as error:
            print("An error occurred!!!")
        else:
            #print(str(response.content))
            return response

def fetch_from_core():
    baseurl="http://portal.core.edu.au/conf-ranks/?search=&by=rank&source=CORE2021&sort=atitle&page="
    page_num = 1
    data = []
    while True:
        ulink=baseurl + str(page_num)
        page_num +=1 
        # print(ulink)
        con1=Connection()
        response=con1.connect(ulink)
        if response is None:
            return False
        s1=BeautifulSoup(response.content,"html.parser")
        my_title = s1.find("title")
        if my_title is not None:
            break
        confs = s1.find_all("tr", class_="evenrow")
        for conf in confs:
            cols = conf.find_all("td")
            cols = [col.text.strip() for col in cols]
            new_conf = dict()
            new_conf["Standard Name"] = cols[0]
            new_conf["Acronym"] = cols[1]
            if len(cols[3]) <= 2:
                new_conf["Rank"] = cols[3]
                data.append(new_conf)
        confs = s1.find_all("tr", class_="oddrow")
        for conf in confs:
            cols = conf.find_all("td")
            cols = [col.text.strip() for col in cols]
            new_conf = dict()
            new_conf["Standard Name"] = cols[0]
            new_conf["Acronym"] = cols[1]
            if len(cols[3]) <= 2:
                new_conf["Rank"] = cols[3]
                data.append(new_conf)
    # for conf in data:
    #    print(conf)
    json_data = json.dumps(data)
    write_file = open("Ranks/rank4.json", "w")
    write_file.write("[")
    flag = 0
    for line in data:
        if flag == 0:
            flag = 1
            json.dump(line, write_file, indent=4)
            write_file.write("\n")
        else:
            write_file.write(",")
            json.dump(line, write_file, indent=4)
            write_file.write("\n")

    write_file.write("]")
    write_file.close()
    return True

# print("Welcome")
# fetch_from_core()
