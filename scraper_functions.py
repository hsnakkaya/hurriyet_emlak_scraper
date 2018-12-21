import time
import datetime
import csv
import requests
from bs4 import BeautifulSoup


def emlak_spider(il_var, ilce_var=[], add_headers=True):

    sleep_time = 2
    ilce_count = len(ilce_var)

    with open('emlak_results.csv', mode='a', encoding='utf-8', newline='') as file:
        csv_writer = csv.writer(file)

        print(str(datetime.datetime.now()) + '   -   scraper started')

        for y in range(len(il_var)):

            print(str(datetime.datetime.now()) + '   -   scraping ' + il_var[y])

            if ilce_count == 0:
                url2 = 'https://www.hurriyetemlak.com/konut-kiralik/' + il_var[y] + '/listeleme?pageSize=50'
                source_code2 = requests.get(url2)
                plain_text2 = source_code2.text
                soup2 = BeautifulSoup(plain_text2, "html.parser")

                i = 0
                ilce_var = []
                for x in soup2.findAll('select', class_='md'):
                    if i == 1:
                        for b in x.findAll('option'):
                            string = b.text.replace('İ', 'i')
                            string = string.lower()
                            string = string.replace('ğ', 'g')
                            string = string.replace('ü', 'u')
                            string = string.replace('ı', 'i')
                            string = string.replace('ş', 's')
                            string = string.replace('ö', 'o')
                            string = string.replace('ç', 'c')
                            ilce_var.append(string)
                    i += 1
                print(ilce_var)

            if add_headers:
                row_to_write = ['id', 'aciklama', 'sehir', 'semt', 'mahalle',
                                'ilan tarihi', 'oda sayisi', 'alan', 'kira', 'url']
                csv_writer.writerow(row_to_write)
            else:
                row_to_write = [0] * 10

            for x in range(len(ilce_var)):

                entry_count = 0

                url = 'https://www.hurriyetemlak.com/konut-kiralik/' \
                      + il_var[y] + '-' + ilce_var[x] + '/listeleme?pageSize=50&view=catalog&page=' + str(1)

                source_code = requests.get(url)

                time.sleep(sleep_time)

                plain_text = source_code.text
                soup = BeautifulSoup(plain_text, "html.parser")

                try:
                    count = soup.find('div', class_='fl count-title')
                    # print('type: ', type(count))
                    count = count.find('strong')

                    # print(count.text)

                    s = count.text
                    s = s.replace('.', '')

                    pages = int(s) // 50
                    if int(s) % 50 > 0:
                        pages += 1

                except Exception as e:
                    print(e)
                    pages = 1

                # print(pages)

                for a in soup.findAll('div', class_='col-lg-12 mt-1 box list-container list-container-projects'):

                    url = a.find('a', class_='overlay-link')
                    entry_url = 'https://www.hurriyetemlak.com' + url.get('href')

                    title = a.find('h2', class_='title')
                    # print('aciklama: ', title.text.strip())

                    listing_id = url.get('data-listing-id')
                    # print(listing_id)

                    location = a.find('li', class_='location')
                    c = 0
                    for b in location.findAll('span'):
                        tag = ['sehir: ', 'semt: ', 'mahalle: ']
                        # print(tag[c], b.string)
                        row_to_write[c + 2] = b.string
                        c += 1

                    date = a.find('li', class_='date').find('span')
                    # print('ilan tarihi: ', date.string)

                    room = a.find('li', class_='room').find('span')
                    # print('oda sayisi: ', room.string)

                    square = a.find('li', class_='square').find('span')
                    # print('alan: ', square.text)

                    price = a.find('li', class_='price').find('span')
                    # print('kira: ', price.string)

                    # print('-------')

                    row_to_write[0] = listing_id.strip()
                    row_to_write[1] = title.text.strip()

                    row_to_write[5] = date.string
                    row_to_write[6] = room.string
                    row_to_write[7] = square.text
                    row_to_write[8] = price.string
                    row_to_write[9] = entry_url
                    csv_writer.writerow(row_to_write)

                    entry_count += 1

                for page in range(pages-1):

                    url = 'https://www.hurriyetemlak.com/' \
                          'konut-kiralik/istanbul-' + ilce_var[x] + '/listeleme?pageSize=50&view=catalog&page=' + str(page+2)

                    source_code = requests.get(url)

                    time.sleep(sleep_time)

                    plain_text = source_code.text
                    soup = BeautifulSoup(plain_text, "html.parser")

                    for a in soup.findAll('div', class_='col-lg-12 mt-1 box list-container list-container-projects'):

                        url = a.find('a', class_='overlay-link')
                        entry_url = 'https://www.hurriyetemlak.com' + url.get('href')

                        title = a.find('h2', class_='title')
                        # print('aciklama: ', title.text.strip())

                        listing_id = url.get('data-listing-id')
                        # print(listing_id)

                        location = a.find('li', class_='location')
                        c = 0
                        for b in location.findAll('span'):
                            tag = ['sehir: ', 'semt: ', 'mahalle: ']
                            # print(tag[c], b.string)
                            row_to_write[c + 2] = b.string
                            c += 1

                        date = a.find('li', class_='date').find('span')
                        # print('ilan tarihi: ', date.string)

                        room = a.find('li', class_='room').find('span')
                        # print('oda sayisi: ', room.string)

                        square = a.find('li', class_='square').find('span')
                        # print('alan: ', square.text)

                        price = a.find('li', class_='price').find('span')
                        # print('kira: ', price.string)

                        # print('-------')

                        row_to_write[0] = listing_id.strip()
                        row_to_write[1] = title.text.strip()

                        row_to_write[5] = date.string
                        row_to_write[6] = room.string
                        row_to_write[7] = square.text
                        row_to_write[8] = price.string
                        row_to_write[9] = entry_url
                        csv_writer.writerow(row_to_write)

                        entry_count += 1

                print(str(datetime.datetime.now()) + '   -   ' + il_var[y] + '/' + ilce_var[x] + ': ' + str(pages) +
                      ' pages ' + str(entry_count) + ' entries')

    print(str(datetime.datetime.now()) + '   -   ' + 'scraping done')
    file.close()




