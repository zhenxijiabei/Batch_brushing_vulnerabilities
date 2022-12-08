# coding=utf-8
import requests
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time

url = "https://www.butian.net/Reward/pub"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0'}

#定义函数获取page页
def get_response(page):
	post_dict = {
		"s":1,
		"p":page
	}
	print(f'正在打印第{page}页')

	new_request = urllib.request.Request(url=url, headers=headers, method='POST')
	from_data = urllib.parse.urlencode(post_dict).encode()

	response = urllib.request.urlopen(new_request, data=from_data)
	result = response.read()
	# print(result)
	
	with open("id_list.txt", mode="a",encoding='utf-8') as f:
		f.write(result)


#利用page页获取资产名称&url
def get_url(company_id):

    url = f'https://www.butian.net/Loo/submit?cid={company_id}'

    print(f'正在打印第{company_id}页')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        "Cookie": "UM_distinctid=1831d199cb3531-0ea3030fbf0df2-26021d51-100200-1831d199cb69a; __btu__=352d3a283326532069de8aa715bc47b0c03c0a4e; __btc__=2a491be21ff5b7544dd0765f09e0d266f65aa870; notice=0; PHPSESSID=ckfe2q12lbl8tk95j12do7pkk6; __btuc__=ea34ab71e595d07be46c91ae73794d125d42f48e"
	}
    response = requests.get(url=url, headers=headers)
    response.encoding = "utf-8"
    content = response.text

    soup = BeautifulSoup(content, "html.parser")

    company = soup.find_all('input', placeholder="请选择")[0].get("value")
    domain = soup.find_all('input', placeholder="输入所属域名或ip，若存在多个以,分隔")[0].get("value")

    print(company+"#"+domain)

    with open("result.txt","a",encoding='utf-8') as file:
    	file.write(company+"#"+domain+"\n")


if __name__ == '__main__':
    for page in range(12, 192):
    	get_response(page)
    	time.sleep(1)

    with open("id_list.txt", mode="r",encoding='utf-8') as f1:
    	for company_id in f1:
            company_id = company_id.strip()
            get_url(company_id)
            time.sleep(1)
