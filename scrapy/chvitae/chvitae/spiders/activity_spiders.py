import scrapy


class ActivitySpider(scrapy.Spider):
	name = "activity"

	start_urls = [
	   'http://chinavitae.com/vip/index.php?mode=location&id=9560.002000000000' # beijing
	#   'http://chinavitae.com/vip/index.php?mode=location&id=9560.004000000000' # fujian
	]

	def parse(self, response):
		# follow links to activity pages
		for href in response.css('#colTripleMiddle .link12::attr(href)'):
			yield response.follow(href, self.parse_activity)

	def parse_activity(self, response):
		def extract_first_with_css(query):
			return response.css(query).extract_first()#.strip()

		def extract_all_with_css(query):
			return response.css(query).extract()#.strip()

		yield {
			'date': extract_first_with_css('tr:nth-child(1) a::text'),
			'activity': extract_first_with_css('td tr:nth-child(2) td+ td::text'),
			'location': extract_first_with_css('#colTripleMiddle tr:nth-child(3) a::text'),   
			'attendees': extract_all_with_css('#colTripleMiddle tr:nth-child(4) a::text'),
			'attendees_links': extract_all_with_css('#colTripleMiddle tr:nth-child(4) a::attr(href)'), 
			'source': extract_first_with_css('tr:nth-child(5) a::text'),
			'topics': extract_all_with_css('tr:nth-child(6) a::text')
		}