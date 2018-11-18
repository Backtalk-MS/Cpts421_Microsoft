from bs4 import BeautifulSoup
import os, requests, re, json, sys

#file_name = sys.argv[1]

for file_name in os.listdir(sys.argv[1]+"/"):
	filePrefix = file_name.split('.')[0]
	filePrefixTokens = filePrefix.split('_')
	f2 = open(filePrefix+'.json','w')
	with open(sys.argv[1]+"/"+file_name) as f:
		test_arr = []
		count = 0
		error_count = 0
		total_lines = sum(1 for _ in f)
		f.seek(0)
		deci_lines  = int(total_lines/10)
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
			main_category = filePrefixTokens[2]
			sub_category = "".join(filePrefixTokens[3:])
			test_arr.append({'title':title,'content':content,'subjects':subjects, 'category': main_category, 'subcategory': sub_category})
			count+=1
			if count == 2*deci_lines:
				print("{} percent done with {}".format(20,sub_category))
			if count == 4*deci_lines:
				print("{} percent done with {}".format(40,sub_category))
			if count == 6*deci_lines:
				print("{} percent done with {}".format(60,sub_category))
			if count == 8*deci_lines:
				print("{} percent done with {}".format(80,sub_category))

		json.dump(test_arr,f2, indent=4, sort_keys=True)
		f2.close()
		test_arr = []
		print("100 percent done with {} || {} Total errors".format(sub_category,error_count))