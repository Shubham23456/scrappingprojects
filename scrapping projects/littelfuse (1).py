import csv
from lib2to3.pgen2 import driver

from bs4 import BeautifulSoup
#from msedge.selenium_tools import Edge, EdgeOptions
from pandas import options


def get_url(search_term):
    template = 'https://www.amazon.com/s?k={}'
    search_term = search_term.replace(' ', '+')

    # Add Term Query To URL
    url = template.format(search_term)

    # Add Page Query Placeholder
    url += '&page={}'

    return url


def extract_record(item):
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')

    try:
        price = item.find('span', 'a-price').find('span', 'a-offscreen').text
    except AttributeError:
        return

    try:
        rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
    except AttributeError:
        rating = ''
        review_count = ''

    image = item.find('img', {'class': 's-image'}).get('src')
    result = (description, price, rating, review_count, url, image)
    return result


'''Run Main Program Routine'''


def main(search_term):
    # Startup The Webdriver
    #options = EdgeOptions()
    options.use_chromium = True
    #driver = Edge(options=options)

    records = []
    url = get_url(search_term)

    for page in range(1, 3):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)

    driver.close()

    # Save Results To CSV File
    with open('Results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'Reviews Count', 'URL', 'Image Link'])
        writer.writerows(records)
        main('ultrawide monitor')