import sys
import requests, fake_useragent  # pip install requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

def p(text, *args):
    print(text, *args, sep=' / ', end='\n') 

def write_json(data, path = None):
    with open(path, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_html(url_page = None):
    ua = fake_useragent.UserAgent() 
    user = ua.random
    header = {'User-Agent':str(user)}
    try:
        page = requests.get(url_page, headers = header, timeout = 10)
        return page.text
    except Exception as e:
        print(sys.exc_info()[1])
        return False

def main():
    start = datetime.now()	

    # ----- book
    html_body = get_html('https://akniga.org/index/top/')
    
    soup = BeautifulSoup(html_body, 'lxml')
    content_list = soup.find('div', class_='content__main__articles')
    
    # content__main__articles--item
    selection_list = content_list.find_all('div', class_='content__main__articles--item')
    
    links = []
    for book in selection_list:
        b_id = book.get('data-id')
        b_img = book.find('div', class_='pull-left').find('img').get('src')
        b_title = book.find('h2')
        b_link = b_title.parent.get('href')
        b_descrip = b_title.parent.find('span', class_='description__article-main').text.replace('Эксклюзив', '').strip()
        b_type = book.find('a', class_='section__title').text.strip()
        b_type_url = book.find('a', class_='section__title').get('href')
        b_autor = book.find('span', class_='link__action link__action--author').find('a')

        p(b_id, b_title.text.strip(), b_link, b_img, b_descrip, b_type)

        row = {}
        row['id'] = b_id
        row['title'] = b_title.text.strip()        
        row['url'] = b_link
        row['img'] = b_img
        row['text'] = b_descrip
        row['type'] = b_type
        row['type_url'] = b_type_url
        row['autor'] = b_autor.text.strip()
        row['autor_url'] = b_autor.get('href')

        links.append(row)
    
    write_json(links, './json/books.json')
    # ----- end book

    end = datetime.now()
    print(str(end-start))


if __name__ == '__main__':
	main() 