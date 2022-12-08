# coding=utf-8
import time
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import tldextract


#通过ip138反查域名
def ip138(ip):

    url = f"https://site.ip138.com/{ip}/"
    headers = {
        'Host': 'site.ip138.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',    
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://site.ip138.com/'
    }
    response = requests.get(url=url, headers=headers)
    response.encoding = "utf-8"
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    #以上直接套用
    
    # print("ip138查询结果")
    domain_ls = []  #定义一个空列表，为了装select查到的内容
    for item in soup.select('#list'):
        domain_all = item.select('a')
        for domain in domain_all:
            domain_ls.append(domain.text)
    # print(domain_ls)
    domain_ls =domain_ls[0:3]   #取前三个域名，多了后面的就不准了
    return domain_ls



#保存ip138反查结果
def catch_ip138_result(ip):
    i = ip.strip()

    try:
        ip138_result = ip138(ip)

        # with open("IP反查全部结果（空+有效）.txt",'a',encoding='utf-8') as f1:
        #     f1.write(str(ip138_result) + "\n")

        if ip138_result !=[]:
            with open("ip反查结果.txt",'a',encoding='utf-8') as f:

                for domain in ip138_result:
                    with open("domain_list.txt",'a',encoding='utf-8') as fopen:
                        fopen.write(domain+"\n")

                result = i +"\t- -\t"+ "#" + str(ip138_result)
                print(result)
                f.write(result + "\n")
        else:
            # with open("ip反查失败列表.txt",'a',encoding='utf-8') as f:
            #     f.write(i + "\n")
            pass
    except:
        pass



#提取主域名
def get_main_domain(url):
    # 一级域名
    domain = tldextract.extract(url).domain
    # 二级域名
    subdomain = tldextract.extract(url).subdomain
    # 后缀
    suffix = tldextract.extract(url).suffix
    # print("获取到的一级域名:{}".format(domain))
    # print("获取到二级域名:{}".format(subdomain))
    # print("获取到的url后缀:{}".format(suffix))
    main_domain = domain+'.'+suffix
    return  main_domain
    # print(main_domain)

#导出主域名
def write_info(data):
    with open("main_domain.txt",'a+',encoding="utf-8") as f:
        for mes in data  :
            f.write(mes+'\n')
    print("[+]结果写入完毕，在当前目录下的main_domain.txt中....")




#获取域名权重
def get_domain_pr(domain):

    url = f"https://www.aizhan.com/cha/{domain}/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    response.encoding = "utf-8"
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    #以上直接套用
    try:
        #获取百度pr
        baidu = soup.find_all('a', id="baidurank_br")[0].parent
        # 1.获取标签为a，id="baidurank_br"的标签内容
        # 2.[0]表示找到所有这样的标签列表中的第一个
        # 3.parent表示找到该a标签的父标签li
        ## text = baidu.text    #获取源码中li标签下的【百度权重：】文本
        baidu_pr = baidu.img.get("alt")  #获取li标签下img标签下"alt"属性的值
        #移动pr
        yidong_pr = soup.find_all('a', id="baidurank_mbr")[0].parent.img.get("alt")
        #谷歌pr
        google_pr = soup.find_all('a', id="google_pr")[0].parent.img.get("alt")

        print(domain+"\t"+"百度"+baidu_pr+" "+"移动"+yidong_pr+" "+"谷歌"+google_pr)
        with open("查询权重结果.txt","a",encoding='utf-8') as file:
            file.write(domain+"\t"+"百度"+baidu_pr+" "+"移动"+yidong_pr+" "+"谷歌"+google_pr+"\n")

        # #实战中有很多是百度和移动pr是n的情况，未加载出来，所以这部分可以单独筛出来2次过滤，注意调大sleep
        # if baidu_pr=="n" and len(google_pr)<3:
        #     with open("需要重新查询list.txt","a",encoding='utf-8') as file:
        #         file.write(domain+"\n")

         #判断导出可用的domain
        if baidu_pr=="n":
            baidu_pr = "0"
        if yidong_pr=="n":
            yidong_pr = "0"
        if google_pr=="n":
            google_pr = "0"
        if int(baidu_pr)>=1 or int(yidong_pr)>=1 or int(google_pr)>=3:
            with open("查询权重结果可用.txt","a",encoding='utf-8') as file:
                file.write(domain+"\t"+"百度"+baidu_pr+" "+"移动"+yidong_pr+" "+"谷歌"+google_pr+"\n")
    except Exception as e:
        print(e)


if __name__ == '__main__':

    #提取IP反查域名
    print("===============IP反查域名查询开始===============")
    ip_list = open("000ip_list.txt",'r',encoding='utf-8').readlines()
    for ip in tqdm(ip_list):
        ip = ip.strip()
        time.sleep(1)
        catch_ip138_result(ip)
    print("===============IP反查域名查询完成===============")


    #处理域名为主域名
    time.sleep(1)
    print("===============开始提取主域名===============")
    time.sleep(1)
    results = set()
    with open('domain_list.txt', 'r', encoding="utf-8") as f:
        temp = f.readlines()
    print("[+]正在提取中....")
    for url in temp:
        url = url.strip()
        result = get_main_domain(url)
        results.add(result)
    print("[+]提取完毕....")
    print("[+]开始写入结果....")
    write_info(results)
    print("===============主域名提取完毕===============")


    #爱站网查权重
    time.sleep(1)
    print("===============开始查询权重===============")
    time.sleep(1)
    with open("main_domain.txt", mode="r",encoding='utf-8') as f1:
        f = f1.readlines()
        for domain in tqdm(f):
            domain = domain.strip()
            get_domain_pr(domain)
            time.sleep(1)   #每次停1s，确保查询相对正确


    #通过查找到的可用seo域名，找到对应IP
    time.sleep(1)
    print("===============处理可用seo域名对应IP===============")
    time.sleep(1)
    with open("查询权重结果可用.txt", mode="r",encoding='utf-8') as f2:
        f = f2.readlines()
        for domain_seo in tqdm(f):
            domain = domain_seo.split("\t")[0]
            # print(domain)
            with open('ip反查结果.txt', 'r', encoding='utf-8') as f3:
                f3 = f3.readlines()
                for item in f3:
                    if item.find(domain.strip()) != -1:
                        print(item.strip())
                        resul = item.strip().split("\t")[0]
                        with open('000最终可用IP.txt', 'a', encoding='utf-8') as f4:
                            f4.write(resul+"\n")

    print("===============查询完毕===============")