import requests
from lxml import etree

sectionURLList = [
    'http://opinion.people.com.cn/GB/8213/353915/353917/index.html',  # 本报评论部
    'http://opinion.people.com.cn/GB/8213/353915/353916/index.html',  # 人民时评
    'http://opinion.people.com.cn/GB/8213/353915/353918/index.html',  # 钟声
    'http://opinion.people.com.cn/GB/8213/353915/354347/index.html',  # 评论员观察
    'http://opinion.people.com.cn/GB/8213/353915/355231/index.html',  # 来论
]
section_titleList = [
    'ben_bao_ping_lun_bu',  # '本报评论部',
    'ren_min_shi_ping',  # '人民时评',
    'zhong_sheng',  # '钟声',
    'ping_lun_yuan_guan_cha',  # '评论员观察',
    'ping_lun', # '来论'
]

# 老版本的页面
sectionURLList2 = [
    'http://opinion.people.com.cn/GB/8213/49160/49205/index.html',    # 任仲平
    'http://opinion.people.com.cn/GB/8213/49160/49220/index.html',    # 人民论坛
]
section_titleList2 = [
    '任仲平',
    '人民论坛',
]

# 基础链接
baseurl = 'http://opinion.people.com.cn/'


# 循环读取链接与标题  
def travers_url():
    for i in range(0, len(sectionURLList)):
        url = sectionURLList[i]
        title = section_titleList[i]
        travers_page(url, title)


def travers_page(url, title):
    main_html_res = requests.get(url)
    main_html_etr = etree.HTML(main_html_res.content)
    main_a_ele_list = main_html_etr.xpath('//td[@class="t11"]/a')
    done_url_file_io = open('done_urls.txt', 'a+')
    article_url_list = []
    for aEle in main_a_ele_list:
        href = aEle.attrib.get('href')
        article_title = aEle.text
        article_url_list.append(href)
        if href not in article_url_list:
            continue
        article_url_list.append(href)
        # 完整的url
        complete_url = baseurl + href
        read_article(title, complete_url, article_title)

    for articleURL in article_url_list:
        done_url_file_io.write('\n')
        done_url_file_io.write(articleURL)


def read_article(section_title, url, article_title):
    section_file_io = open(section_title + '.txt', 'a', encoding='utf-8')

    section_file_io.write('\n')
    section_file_io.write('<h2>' + article_title + '</h2>')

    article_html_res = requests.get(url)
    article_html_etr = etree.HTML(article_html_res.content)
    article_p_ele_list = article_html_etr.xpath('//div[@id="rwb_zw"]/p')

    for articlePEle in article_p_ele_list:
        section_file_io.write('\n')
        section_file_io.write('<p>' + articlePEle.text + '</p>')


travers_url()
