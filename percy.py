from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
import re
from collections import defaultdict
import time

pdfsep = ""

## Regex Patterns
re_subjects = "(?P<subjects>(?:\d+\(\d+\.?\d*\)\n)+)"
re_cred = "(?P<cred>\d+)"
re_scores = "(?P<scoreList>(?:\s*(?:\d+|[ACD]|\-)\s+(?:\d+|[ACD]|\-)\s*\n)+)"
re_enroll = "(?P<enroll>\d+\n)"
re_name = "(?P<name>.+\n)"
re_sid = "(?P<sid>SID:\s*\d+\n)"
re_schemeid = "(?P<schemeId>schemeID:\s*\d+\n)"
re_aggregates = "(?P<aggregates>(?:\s*(?:\d+\([ABCDEOFP]\+?\)|[ACD]))+)"
re_semester = "(?P<semester>\d+\s+(?:semester|annual))"
re_exam_type = "(?P<exam_type>(?:REGULAR|REAPPEAR)\s+\w+,\s*\w{2,4})"

re_result_row_pattern = f"{re_subjects}\s*{re_cred}\s*{re_scores}{re_enroll}{re_name}{re_sid}{re_schemeid}{re_aggregates}"


def separate_pages(doc_text, separator):
    return ['\n'.join(list(filter(None, page_text.split("\n")))) for page_text in doc_text.split(separator)]

def parse(pdf_file, pagenumbers=None):
    init_time = time.time()

    # Extract all Text from pdf file
    raw_text = extract_text(pdf_file, page_numbers=pagenumbers , laparams=LAParams(line_overlap=0, char_margin=1000, word_margin=0.1, line_margin=0.5, boxes_flow=None))
    # Divide file into pages using separator 
    pages = separate_pages(raw_text, pdfsep)[:-1]

    # Init data dictionary for later use
    data = {
        "time": None,
        "page_count": len(pages),
        "results_count": 0,
        "semesters": defaultdict(lambda: defaultdict(list))
    }

    res_count = 0
    # Iterate over pages list and perform regex on each page
    for page in pages:
        if "RESULT TABULATION SHEET" in page:
            semester = re.findall(re_semester, page, re.IGNORECASE)[0]
            exam_type = re.findall(re_exam_type, page, re.IGNORECASE)[0]
            results = re.findall(re_result_row_pattern, page, re.IGNORECASE)
            res_count += len(results)

            # Append list of results matched inside the text
            data["semesters"][semester][exam_type].append(results)
    
    data["results_count"] = res_count
    data["time"] = time.time()-init_time
    return data


