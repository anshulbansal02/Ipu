from ast import literal_eval as make_tuple
import requests

bases = ["http://ggsipu.ac.in/ExamResults/",
         "http://ggsipu.ac.in/ExamResults/",
         "http://ggsipu.ac.in/ExamResults/",
         "http://ggsipu.ac.in/ExamResults/",
         "http://ipu.ac.in/"]

with open('./files_page5.txt', 'r', encoding="utf-8") as results_files:
    urls = [make_tuple(f)[0] for f in results_files.readlines()]


urls = urls[100:]

for i in range(len(urls)):
    url = bases[4]+urls[i]
    k = requests.head(url)

    if k.headers['Content-Type'] == 'application/pdf':
        print(k.headers['Content-Type'])
    else:
        print(i, url)
        break
