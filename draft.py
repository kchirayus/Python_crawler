# pip install scrapy
# --------------To Use---------------
# import draft
# print draft.customCrawler()
# -----------------------------------

import scrapy
from scrapy.crawler import CrawlerProcess

results = []

def customCrawler():
	process.crawl(diceSpider)
	process.start()
	return results

class diceSpider(scrapy.Spider):
	name = 'back'
	# start_urls = ['https://www.dice.com/jobs?q=full+stack&l=Seattle%2C+WA']
	start_urls = ['https://www.dice.com/jobs/q-"back+end"+"full+stack"+"front+end"-limit-30-jobs.html']
	
	def parse(self, response):
		page = 1
		while response.css('.serp-result-content h3 a::attr(href)') and page < 8:
			url = 'https://www.dice.com/jobs/q-"back+end"+"full+stack"+"front+end"-startPage-'+str(page)+'-limit-30-jobs.html'
			yield scrapy.Request(url, callback=self.parse_page)
			page += 1

	def parse_page(self, response):
		for href in response.css('.serp-result-content h3 a::attr(href)'):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_job)

	def parse_job(self, response):
		results.append({
			'title': response.css('.jobTitle::text').extract()[0],
			'skills': response.css('.iconsiblings::text').extract()[0],
			'salary': response.css('.mL20::text').extract()[0],
			'location': response.css('.location::text').extract()[0],
			'posted': response.css('.posted::text').extract()[0],
		})

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})