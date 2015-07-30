# def test(title, location):
# 	name = 'stackoverflow'
# 	title = title.replace(" ", "+")
# 	location = location.replace(" ", "+").replace(",", "%2C")
# 	start_urls = ['http://www.indeed.com/jobs?q=' + title + '&l=' + location]
# 	return start_urls

# print test("full stack", "Seattle WA")

import scrapy

class DiceSpider(scrapy.Spider):
	name = 'dice'
	# start_urls = ['https://www.dice.com/jobs?q=full+stack&l=Seattle%2C+WA']
	start_urls = ['https://www.dice.com/jobs/q-full+stack+developer-limit-120-jobs.html']

	def parse(self, response):
		page = 1
		while response.css('.serp-result-content h3 a::attr(href)') and page < 2:
			url = 'https://www.dice.com/jobs/q-full+stack+developer-startPage-'+str(page)+'-limit-120-jobs'
			yield scrapy.Request(url, callback=self.parse_page)
			page += 1

	def parse_page(self, response):
		for href in response.css('.serp-result-content h3 a::attr(href)'):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_job)

	def parse_job(self, response):
	    yield {
			'title': response.css('.jobTitle::text').extract()[0],
			'skills': response.css('.iconsiblings::text').extract()[0],
			'salary': response.css('.mL20::text').extract()[0],
			'location': response.css('.location::text').extract()[0],
			'posted': response.css('.posted::text').extract()[0],
			# 'description': response.css('#jobdescSec').extract()[0],
			# 'travel': response.css('.iconsiblings').extract()[2],
			# 'tags': response.css('.question .post-tag::text').extract(),
			# 'link': response.url,


		}
# https://www.dice.com/jobs/q-full+stack+developer-startPage-limit-120-jobs.html
# response.css('.posiCount span::text').extract()[3]
