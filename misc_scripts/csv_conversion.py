import csv, os, json, string
from urllib.parse import urlparse

translation = str.maketrans('','', string.punctuation)

with open("./csv_2000_all/AllCats_2000.csv","w",encoding="utf-8") as csv_file:
    comment_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')
    comment_writer.writerow(['Category','Subcategory','Title','Content'])
    for file_name in os.listdir('../Test_Mongoose/json/'):
        count = 0
        json_file = open('../Test_Mongoose/json/{}'.format(file_name),'r',encoding='utf-8')
        json_data = json.load(json_file)
        file_name_tokens = file_name.split('.')[0].split('_')
        print("Converting {} {}".format(file_name_tokens[2],"_".join(file_name_tokens[3:])))
        for elem in json_data:
            token_title = elem['title'].lower().split()
            token_content = elem['content'].lower().split()
            try:
                token_title_clean = [ele for ele in token_title if not urlparse(ele).scheme]
                token_content_clean = [ele for ele in token_content if not urlparse(ele).scheme]
            except:
                continue
            comment_writer.writerow([
                elem['category'],
                elem['subcategory'],
                (' '.join(token_title_clean).translate(translation)),
                (' '.join(token_content_clean).translate(translation))
                ])
            count+=1
            if count == 2000:
                break
        json_file.close()