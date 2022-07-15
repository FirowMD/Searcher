import requests
from bs4 import BeautifulSoup
import sys

help_message = """
Pass file with request and get google search results!
Example: python3 main.py "python"
"""

def get_google_page_info(html):
    titles = []
    soup = BeautifulSoup(html, 'html.parser')
    for h3 in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):
        titles.append(h3.text)
    
    links = []
    for div in soup.find_all('div', class_='egMi0 kCrYT'):
        s = div.a['href']
        links.append(s[7:])

    descriptions = []
    for div in soup.find_all('div', class_='Gx5Zad fP1Qef xpd EtOod pkphOe'):
        temp = []
        for div2 in div.find_all('div', class_='BNeawe s3v9rd AP7Wnd'):
            for div3 in div2.find_all('div', class_='BNeawe s3v9rd AP7Wnd'):
                temp.append(div3.prettify())

        tempstr = ''.join(temp)
        if tempstr not in descriptions:
            descriptions.append(tempstr)

    return titles, links, descriptions

def get_html_by_url(url):
    headers = { 'accept-language': 'en;q=0.9' }
    response = requests.get(url, headers=headers)
    return response.text

def get_google_url(query):
    template = 'https://www.google.com/search?q={}&oq={}&sourceid=chrome&ie=UTF-8'
    return template.format(query, query)

def get_google_html(query):
    url = get_google_url(query)
    return get_html_by_url(url)

def create_html(html_title, titles, links, descriptions):
    html = ''
    html += '<hr>\n'
    html += '<h1>{}</h1>\n'.format(html_title)
    html += '<hr>\n'
    for i in range(len(titles)):
        html += '<h2><a href="{}">{}</a></h2>\n'.format(links[i], titles[i])
        html += '<p>{}</p>\n'.format(descriptions[i])
    return html

def write_file(html, filename):
    with open(filename, 'wb') as f:
        f.write(html.encode('utf-8'))

def handle_query(query):
    html = get_google_html(query)
    titles, links, descriptions = get_google_page_info(html)
    write_file(html, query + '.tmp.html')
    return create_html(query, titles, links, descriptions)

def transform_queries_to_html(queries):
    res_html = ''
    for i in queries:
        res_html += handle_query(i.replace('\n', ''))
    
    write_file(res_html, 'results.html')

def main():
    try:
        input_fname = sys.argv[1]
        with open(input_fname, 'r') as f:
            queries = f.readlines()
    except Exception as e:
        print(help_message)
        print(e)
        return
    
    transform_queries_to_html(queries)

main()
