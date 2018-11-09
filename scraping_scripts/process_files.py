from bs4 import BeautifulSoup
import os, requests, re, json, sys

for file_name in os.listdir(sys.argv[1]+"/"):
    filePrefix = file_name.split('.')[0]
    filePrefixTokens = filePrefix.split('_')
    f2 = open(filePrefix+'.json','w')
    with open(sys.argv[1]+"/"+file_name) as f:
        test_arr = []
        # count = 0
        error_count = 0
        for line in f:
            # if count >= 500:
            #     break
            resp = requests.get(line[:-1])
            if resp.status_code != requests.codes.ok:
                error_count+=1
                print(resp.status_code)
                continue
            soup = BeautifulSoup(resp.content,'lxml')
            subjects = re.sub(r"[\n]*","",soup.find(id='threadQuestionInfoAppliesToItems').get_text().encode('ascii','ignore').decode('utf-8')).split('/')
            title = soup.find(id='threadQuestionTitleStatusIcons').get_text().strip()
            content = re.sub(r'\r\n|\n|\s+',' ',soup.find("div",class_="thread-message-content-body-text thread-full-message").get_text().strip().encode('ascii','ignore').decode('utf-8'))
            main_category = filePrefixTokens[1]
            sub_category = filePrefixTokens[2]
            test_arr.append({'title':title,'content':content,'subjects':subjects, 'category': main_category, 'subcategory': sub_category})
            # count+=1
        json.dump(test_arr,f2, indent=4, sort_keys=True)
        f2.close()
        test_arr = []
        print("Total errors for {} {} errors".format(file_name,error_count))