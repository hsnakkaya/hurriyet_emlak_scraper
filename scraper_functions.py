import time
import datetime
import csv
import requests
from bs4 import BeautifulSoup


def emlak_spider(il_var, ilce_var=[]):

    sleep_time = 0.5
    ilce_count = len(ilce_var)

    with open('emlak_results.csv', mode='w', encoding='utf-8', newline='') as file:
        csv_writer = csv.writer(file)

        report = open('scraper_report.txt', 'a+')
        report.write(str(datetime.datetime.now()) + '   -   scraper started\n')
        print(str(datetime.datetime.now()) + '   -   scraper started')

        for y in range(len(il_var)):

            report.write(str(datetime.datetime.now()) + '   -    scraping ' + il_var[y] + '\n')
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

            row_to_write = ['aciklama', 'sehir', 'semt', 'mahalle', 'ilan tarihi', 'oda sayisi', 'alan', 'kira', 'url']
            csv_writer.writerow(row_to_write)

            for x in range(len(ilce_var)):

                entry_count = 0

                url = 'https://www.hurriyetemlak.com/konut-kiralik/' \
                      + il_var[y] + '-' + ilce_var[x] + '/listeleme?pageSize=50&view=catalog&page=' + str(1)

                source_code = requests.get(url)

                time.sleep(sleep_time)

                plain_text = source_code.text
                soup = BeautifulSoup(plain_text, "html.parser")

                count = soup.find('div', class_='fl count-title').find('strong')
                # print(count.text)

                s = count.text
                s = s.replace('.', '')

                pages = int(s) // 50
                if int(s) % 50 > 0:
                    pages += 1

                # print(pages)

                for a in soup.findAll('div', class_='col-lg-12 mt-1 box list-container list-container-projects'):

                    url = a.find('a', class_='overlay-link')
                    entry_url = 'https://www.hurriyetemlak.com' + url.get('href')

                    title = a.find('h2', class_='title')
                    # print('aciklama: ', title.text.strip())

                    location = a.find('li', class_='location')
                    c = 0
                    for b in location.findAll('span'):
                        tag = ['sehir: ', 'semt: ', 'mahalle: ']
                        # print(tag[c], b.string)
                        row_to_write[c + 1] = b.string
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

                    row_to_write[0] = title.text.strip()

                    row_to_write[4] = date.string
                    row_to_write[5] = room.string
                    row_to_write[6] = square.text
                    row_to_write[7] = price.string
                    row_to_write[8] = entry_url
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

                        location = a.find('li', class_='location')
                        c = 0
                        for b in location.findAll('span'):
                            tag = ['sehir: ', 'semt: ', 'mahalle: ']
                            # print(tag[c], b.string)
                            row_to_write[c + 1] = b.string
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

                        row_to_write[0] = title.text.strip()

                        row_to_write[4] = date.string
                        row_to_write[5] = room.string
                        row_to_write[6] = square.text
                        row_to_write[7] = price.string
                        row_to_write[8] = entry_url
                        csv_writer.writerow(row_to_write)

                        entry_count += 1

                report.write(str(datetime.datetime.now()) + '   -   ' + ilce_var[x] + ': ' + str(pages) +
                             ' pages ' + str(entry_count) + ' entries' + '\n')
                print(str(datetime.datetime.now()) + '   -   ' + il_var[y] + '/' + ilce_var[x] + ': ' + str(pages) +
                      ' pages ' + str(entry_count) + ' entries')

    report.write(str(datetime.datetime.now()) + '   -   ' + 'scraping done')
    print(str(datetime.datetime.now()) + '   -   ' + 'scraping done')
    file.close()
    report.close()




