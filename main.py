import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
tester = 0
def append_info():
    all_about_people = soup.find_all("tr")
    for i in all_about_people:
        i = str(i)[20:-30]
        number = str(i)[0:8]
        name = str(i)[29: 1 + str(i).rfind(".")]
        streett = str(i)[str(i).find('"adr">'): str(i).find(', <nobr>')].replace('"adr">', "")
        homee = str(i)[str(i).find(', <nobr>'):].replace('<nobr>', "").replace(",", "").replace('</td><td class="adr">',
                                                                                                '')
        print(streett, homee, name, number)
        appending(streett, homee, name, number)
def clean(all_about_homes):
    for i in all_about_homes:
        s, k = str(i).find(">"), str(i).rfind("<")
        name_of_homes.append(str(i)[s:k].replace(">",""))
        s, k = str(i).find('"'), str(i).rfind('"')
        links_of_homes.append(str(i)[s + 1 :k])
name_of_streets = []
links_of_streets = []
name_of_homes = []
links_of_homes = []
conn = sqlite3.connect('novopolotsk_tel.sqlite')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS peoples(street TEXT, home TEXT, name TEXT, number TEXT)""")
conn.commit()
def appending(street, home, name, number):
    cursor.execute(f"""INSERT INTO peoples VALUES(?,  ?,  ?,  ?)""", (street, home, name, number))
    conn.commit()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("–disable-infobars")
chrome_options.add_argument("–enable-automation")
chrome_options.add_argument("–start-maximized")
driver = webdriver.Chrome(r"C:\Users\user\PycharmProjects\новополоцк\venv\Scripts\chromedriver.exe", chrome_options=chrome_options)
driver.get("https://spravochnik109.link/byelarus/vityebskaya-oblast/gorod-novopolotsk/novopolotsk?serchStreet=%21")
html = driver.page_source
soup = BeautifulSoup(html, 'html5lib')
all_about_streets = soup.find_all("a")
all_about_streets_c = all_about_streets[23:58]
all_about_streets, all_about_streets_c = all_about_streets_c, 0
for i in all_about_streets:
    s, k = str(i).find(">"), str(i).rfind("<")
    name_of_streets.append(str(i)[s:k].replace(">",""))
    s, k = str(i).find('"'), str(i).rfind('"')
    links_of_streets.append(str(i)[s + 1 :k])
iii = -1
ii = 0 #для параметра page в #начинаем перебор информации внутри дома -> ->
#перебираем ссылки на улицы ->
for i in range(len(links_of_streets)):
    driver.get("https://spravochnik109.link/byelarus/vityebskaya-oblast/gorod-novopolotsk/novopolotsk?serchStreet=%21")
    html = driver.page_source
    soup = BeautifulSoup(html, 'html5lib')
    all_about_homes = (soup.find_all("a"))[23:-1]
    clean(all_about_homes)
    driver.get("http:" + links_of_streets[i][0:links_of_streets[i].find("?")+1] + links_of_streets[i][links_of_streets[i].find("Street="):links_of_streets[i].find("Street=")+8].lower())
    html = driver.page_source
    soup = BeautifulSoup(html, 'html5lib')
    div = str(soup.find_all("div"))[str(soup.find_all("div")).find("1-"):str(soup.find_all("div")).find("1-") + 10]
    print(div)
    shag = int(str(div)[2:str(div).find(" ")])
    maxx = int(str(div)[str(div).find("из")+3::])
    tek = 0
    try:
        while tek < maxx:
            tek += 15
            append_info()
            driver.find_element_by_xpath('//*[@id="main"]/div[5]/div/div[3]/a[4]').click()
            html = driver.page_source
            soup = BeautifulSoup(html, 'html5lib')
    except:
        try:
            driver.find_element_by_xpath('//*[@id="dismiss-button"]').click()
        except:
            pass
        print(tek)



cursor.execute("""SELECT * FROM peoples""")
conn.commit()
print(cursor.fetchall())
