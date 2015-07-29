# def test(title, location):
#     name = 'stackoverflow'
#     title = title.replace(" ", "+")
#     location = location.replace(" ", "+").replace(",", "%2C")
#     start_urls = ['http://www.indeed.com/jobs?q=' + title + '&l=' + location]
#     return start_urls

# print test("full stack", "Seattle WA")

import scrapy

class DiceSpider(scrapy.Spider):
    name = 'dice'
    # start_urls = ['https://www.dice.com/jobs?q=full+stack&l=Seattle%2C+WA']
    start_urls = ['https://www.dice.com/jobs/q-full+stack+developer-l-Seattle%2C+WA-radius-30-startPage-1-limit-100-jobs.html']

    def parse(self, response):
        for href in response.css('.serp-result-content h3 a::attr(href)'):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_question)

    def parse_question(self, response):
        yield {
            'title': response.css('.jobTitle::text').extract()[0],
            'description': response.css('#jobdescSec').extract()[0],
            'skills': response.css('.iconsiblings').extract()[0],
            'salary': response.css('.iconsiblings').extract()[1],
            'travel': response.css('.iconsiblings').extract()[2],
            # 'tags': response.css('.question .post-tag::text').extract(),
            # 'link': response.url,
        }