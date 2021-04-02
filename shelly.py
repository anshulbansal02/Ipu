import requests
from bs4 import BeautifulSoup
import time
import sqlite3


db_conn = sqlite3.connect('exam_results_urls.db')
db = db_conn.cursor()

table_name = 'result_files'

table_instances = db.execute(
    f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")

if not len(list(table_instances)):
    db.execute(f'''
    CREATE TABLE {table_name} (url text unique, title text, date text)
    ''')

base_url = "http://ggsipu.ac.in/ExamResults"
files_list_url = "http://ggsipu.ac.in/ExamResults/ExamResultsmain.htm"
page = requests.get(files_list_url)
soup = BeautifulSoup(page.content, 'lxml')
rows = soup.findAll('tr')


def parse_row(tr):
    td = tr.findAll('td')
    if td:
        urls = re.findall("href=(?:\"|')(.*?)(?:\"|')",
                          str(td[0]), re.IGNORECASE)
        if not urls:
            return
        url = urls[0]

        title = re.sub("\s{2,}", " ", re.sub("<.*?>", "", str(td[0]))).strip()
        date = re.search("\d{1,2}\-?\d{1,2}\-?\d{1,4}|$", str(td[1])).group()

        return url, title, date


parsed_rows = [parse_row(tr) for tr in rows]
parsed_rows = [x for x in parsed_rows if x]

for r in parsed_rows[::-1]:
    print(r[0])
    try:
        db.execute(f'INSERT INTO {table_name} VALUES {r} ')
        db_conn.commit()
    except:
        print("Error Caught")
        pass

db_conn.close()
