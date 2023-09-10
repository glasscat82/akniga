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
    html_body = get_html('https://akniga.org/index/top/page1/')
    
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
        b_autors = book.find_all('span', class_='link__action link__action--author')
        b_favourite = book.find('span', class_='js-favourite-count').text.strip()
        b_counter_number = book.find('span', class_='counter-number').text.strip()
        
        b_series = b_autor = b_reader = None
        for index, autor in enumerate(b_autors, 0):   
            
            if index == 0:
                b_autor = autor.find('a')
            
            if index == 1:
                b_reader = autor.find('a')

            if index == 2:
                b_series = autor.find('a')

        row = {}
        row['id'] = b_id
        row['title'] = b_title.text.strip()
        row['url'] = b_link
        row['img'] = b_img
        row['text'] = b_descrip
        row['type'] = b_type
        row['type_url'] = b_type_url
        row['autor'] = b_autor.text.strip() if b_autor is not None else None
        row['autor_url'] = b_autor.get('href') if b_autor is not None else None
        row['reader'] = b_reader.text.strip() if b_reader is not None else None
        row['reader_url'] = b_reader.get('href') if b_reader is not None else None
        row['series'] = b_series.text.strip() if b_series is not None else None
        row['series_url'] = b_series.get('href') if b_series is not None else None
        row['favourite'] = b_favourite
        row['counter_number'] = b_counter_number

        links.append(row)
    
    write_json(links, './json/books.json')    
    # ----- end book

    end = datetime.now()
    print(str(end-start))


if __name__ == '__main__':
	main() 