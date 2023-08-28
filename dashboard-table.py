# dashboard url
url = "https://chartink.com/dashboard/123"



import os
import csv
import sys

try:
    import requests_html
except (ModuleNotFoundError, ImportError):
    print("requests module not found")
    os.system(f"{sys.executable} -m pip install -U requests-html")
finally:
    import requests_html



session = requests_html.HTMLSession()
r = session.get(url)
r.html.render(sleep=3)
id_name = 'vgt-table'
class_name = 'vue-grid-item'


tables = r.html.find(f'.{class_name}')
for table in tables:
    final_data = []
    title = table.find('.truncate',first = True)
    tbl = table.find(f'#{id_name}',first = True)
    if tbl != None:
        for item in tbl.find('tr'):
                headerdata = [head.text.split("Sort table")[0] for head in item.find("th")]
                if headerdata:
                    final_data.append(headerdata)
                data = [head.text for head in item.find("td")]
                if 'No data for table' in data:
                    continue
                elif data:
                    final_data.append(data)
        if final_data:
            file_name = f'{title.text}.csv'
            if os.path.exists(file_name):
                os.remove(file_name)
            
            with open(file_name, mode='w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                for data in final_data:
                    csv_writer.writerow(data)  # Write header
