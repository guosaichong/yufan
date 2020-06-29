import requests
from lxml import etree
import json

def get_date():
    data={}
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 '
        }
    try:
        riqi_url = 'http://tools.2345.com/rili.htm'
        response = requests.get(riqi_url, headers=headers)
        html = etree.HTML(response.text)
        riqi_url1 = 'https://www.2345.com/?kgsc21'
        response1 = requests.get(riqi_url1, headers=headers)
        html1 = etree.HTML(response1.text)
        # print(html1)
        data1 = html.xpath('//*[@id="info_all"]/h3/text()')
        data2 = html.xpath('//*[@id="info_nong"]/text()')
        data3 = html.xpath('//*[@id="info_nong"]/b/text()')
        # data=(data1[0].split(" ")[1],data1[0].split(" ")[2],data1[0].split(" ")[3],data2[0],data3[0])
        data["1"]=data1[0].split(" ")[1]
        data["2"]=data1[0].split(" ")[2]
        data["3"]=data1[0].split(" ")[3]
        data["4"]=data2[0]
        data["5"]=data3[0]
        print(data)
        # print(type(data))
        with open("date.json","w") as f:
            json.dump(data,f)
    except:
        data={}
        # riqi_str = '***没有获取到数据***'
    return data
if __name__ == "__main__":
    get_date()