import re
import scrapy
from scrapy import Request
from urllib import parse
import requests
import json

from cnblog.items import CnblogItem

from cnblog.utils.common import getMd5


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['https://news.cnblogs.com/']

    def parse(self, response):
        urlContent = response.css("div.news_block div.content")
        for content in urlContent:
            uri = content.css('h2.news_entry a::attr(href)').extract_first('')
            image = content.css('div.entry_summary img.topic_img::attr(src)').extract_first('')
            if image.startswith('//'):
                image = image.replace("//", "https://")
            if uri:
                yield Request(url=parse.urljoin(response.url, uri), meta={"image": image}, callback=self.parse_detail)
        # 提取下一页给parse处理
        # pageContent = response.css("div.pager a:last_child::text").extract_first("")
        # if pageContent == 'Next >':
        #     nextUrl = response.css("div.pager a:last_child::attr(href)").extract_first("")
        #     yield Request(url=parse.urljoin(response.url,nextUrl),callback=self.parse)

        pass

    def parse_detail(self, response):
        r = re.match(".*?(\d+)", response.url)
        if r:
            item = CnblogItem()
            title = response.css('div#news_title a::text').extract_first("")

            create = response.css('div#news_info span.time::text').extract_first("")
            createRe = re.match(".*?(\d+.*)", create)
            createTime = ''
            if createRe:
                createTime = createRe.group(1)

            content = response.css('div#news_content div#news_body').extract_first("")

            otherInfouri = "/NewsAjax/GetAjaxNewsInfo?contentId={}"
            postId = r.group(1)
            jsonHtml = requests.get(parse.urljoin(response.url, otherInfouri.format(postId)))
            jsonData = json.loads(jsonHtml.text)
            totalView = jsonData['TotalView']
            zan = jsonData['DiggCount']
            comments = jsonData['CommentCount']

            tagList = response.css('div#news_more_info a.catalink::text').extract()
            tags = ",".join(tagList)
            item['title'] = title
            item['createTime'] = createTime

            image = response.meta.get("image", "")
            if image:
                item['imageUrl'] = [image]
            else:
                item['imageUrl'] = []
            item['url'] = response.url
            item['urlId'] = getMd5(response.url)
            item['zan'] = zan
            item['comments'] = comments
            item['reads'] = totalView
            item['content'] = content
            item['tags'] = tags
            yield item
