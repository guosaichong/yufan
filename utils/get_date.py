import requests
from lxml import etree

def get_date():
    date_list=[]
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 '
        }
    try:
        riqi_url = 'http://tools.2345.com/rili.htm'
        response = requests.get(riqi_url, headers=headers)
        html = etree.HTML(response.text)
        data1 = html.xpath('//*[@id="info_all"]/h3/text()')
        data2 = html.xpath('//*[@id="info_nong"]/text()')
        print(data1[0].split(" ")[1],data1[0].split(" ")[2],data1[0].split(" ")[3],data2[0])
        date_list.append
        # riqi_str = data1[0] + '\n' + data2[0]
        # print(riqi_str)
    except:
        riqi_str = '***没有获取到数据***'
if __name__ == "__main__":
    get_date()