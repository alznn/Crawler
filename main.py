from bs4 import BeautifulSoup
from requests import get
from fake_useragent import UserAgent
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from xml.dom import minidom

ua = UserAgent()
def lovely_soup(u):
    r = get(u, headers={'User-Agent': ua.chrome})
    return BeautifulSoup(r.text, 'lxml')

def getPostData(Current_Soup):
    tittle_id = "_2SdHzo12ISmrC8H86TgSCp _29WrubtjAcKqzJSPdQqQ4h"
    content_id = "_292iotee39Lmt0MkQZ2hPV RichTextJSON-root"
    title = Current_Soup.find('div', {'class': tittle_id})
    content = Current_Soup.find('div', {'class': content_id})
    return title.text,content.text,

def getComment(Current_Soup):
    top3_comment = []
    for td in soup.findAll('div', {'class': '_292iotee39Lmt0MkQZ2hPV RichTextJSON-root'}):
        comment = td.findAll('p', {'class': '_1qeIAgB0cPwnLhDF9XSiJM'})
        comments = ' '.join([c.text for c in comment])
        top3_comment.append(comments)
    return top3_comment

def convertoxml(pd_tittle,pd_content,pd_commnet1,pd_commnet2,pd_commnet3):
    data = ET.Element('xml')
    for i in range(3):
        post = ET.SubElement(data, 'post')
        ET.SubElement(post, "title").text = pd_tittle[i]
        ET.SubElement(post, "content").text = pd_content[i]
        ET.SubElement(post, "comment").text = pd_commnet1[i]
        ET.SubElement(post, "comment").text = pd_commnet2[i]
        ET.SubElement(post, "comment").text = pd_commnet3[i]
    rough_string = ElementTree.tostring(data, 'utf-8')
    reparsed = minidom.parseString(rough_string)


    file = open('result.xml', "w", encoding='utf8')
    file.write(reparsed.toprettyxml(indent="  ")[23:])
    file.close()

    return reparsed, reparsed.toprettyxml(indent="  ")[23:]
# query = input()
query = "coronavirus"
link = 'https://www.reddit.com/search/?q='
soup = lovely_soup(link+query)
# print(soup.text)
hrefs = []
for td in soup.findAll('div', {'class': 'QBfRw7Rj8UkxybFpX-USO'}):
    artlink = td.findAll('a', {'class': 'SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE'})
    for a in artlink:
        hrefs.append(a['href'])
pd_tittle = []
pd_content = []
pd_commnet1 = []
pd_commnet2 = []
pd_commnet3 = []
s_reparsed = ''
for href in hrefs[0:3]:
    reddit = 'https://www.reddit.com'
    print(reddit+href)
    page_soup = lovely_soup(reddit+href)
    try:
        t,c = getPostData(page_soup)
        top3_comment = getComment(page_soup)
    except:
        title =  page_soup.find('h1', {'class': '_eYtD2XCVieq6emjKBH3m'})
        t = title.text
        c = ''
        top3_comment = getComment(page_soup)
    # print(title.text)
    pd_tittle.append(t)
    pd_content.append(c)
    pd_commnet1.append(top3_comment[0])
    pd_commnet2.append(top3_comment[1])
    pd_commnet3.append(top3_comment[2])
convertoxml(pd_tittle,pd_content,pd_commnet1,pd_commnet2,pd_commnet3)