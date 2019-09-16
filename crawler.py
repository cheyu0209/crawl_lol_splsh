from urllib.request import urlopen, urljoin, Request
from bs4 import BeautifulSoup
import requests, re, os, time

def crawl(url):
    req = Request(url, headers=headers)
    response = urlopen(req)
    return response.read()

# 取得圖片網址
def parse(html):
    soup = BeautifulSoup(html, features='lxml')
    
    skins = soup.find_all('a', { 'class': 'skins cboxElement',
                                             'href': re.compile(r'^(https://).+?(\.jpg)$') })

    skin_urls = list(set([ i['href'] for i in skins ]))
    #skin_titles = list([ i.split('/')[-1] for i in skin_urls ])
    #[ print(skin_titles[i], '\t', skin_urls[i]) for i in range(len(skin_urls)) ]

    #return skin_titles, skin_urls
    return skin_urls

# 下載圖片
def downloads(img_urls):
    os.makedirs('./downloads/', exist_ok=True)
    
    for img_url in img_urls:
        img_nm = img_url.split('/')[-1]
        r = requests.get(img_url, stream=True)
        with open('./downloads/%s' % img_nm, 'wb') as f:
            for chunk in r.iter_content(chunk_size=512):
                f.write(chunk)
            print('%s downloads successfully.' %img_nm)

base_url = 'https://na.leagueoflegends.com/en/news/game-updates/patch'
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0' }

req = Request(base_url, headers=headers)
html = urlopen(req).read()

soup = BeautifulSoup(html, features='lxml')

# 分頁頁數
pages = soup.find_all('a', { 'title': re.compile(r'Go to page .+?') })
max_page = int( pages[-1].get_text() )

for j in range(max_page):
    page_html = crawl(urljoin(base_url, '?page=%s' % j))

    soup = BeautifulSoup(page_html, features='lxml')

    # 分頁主題
    title_frame = soup.find('div', { 'class': re.compile(r'^view .+?') })
    titles = title_frame.find_all('a', { 'href': re.compile(r'^/en/news/game-updates/patch/patch-\d+(-notes)$') })
    sub_url = list(set([ i['href'] for i in titles ]))
    #print(sub_url)

    for i in sub_url:
        html = crawl(urljoin(base_url, i))
        #time.sleep(3)
        skin_urls = parse(html)
        [ print(i) for i in skin_urls ]
        #downloads(skin_urls)