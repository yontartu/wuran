import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector 
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
import re
from datetime import datetime

class OfficialSpider(CrawlSpider):
	name = "official2"
	start_urls = [
		'http://chinavitae.com/vip/index.php?mode=location&id=9560.003000000000' # chongqing
	#   'http://chinavitae.com/vip/index.php?mode=location&id=9560.002000000000' # beijing
	#   'http://chinavitae.com/vip/index.php?mode=location&id=9560.004000000000' # fujian
	]
	allowed_domains = ['chinavitae.com']

	custom_settings = {
	}

	'''rules = (
		# extract links matching activity records
		Rule(LinkExtractor(allow=('mode=show&id=\d+', )), callback='parse_activity'),
		
		# extract links matching 'type=ncv' (but not matching 'type=cv') and parse them with the spider's method parse_officials
		Rule(LinkExtractor(allow=(r'type=ncv', ), deny=(r'type=cv')), callback='parse_officials'),
	)'''

	def parse(self, response):
		links = response.css('#colTripleMiddle .link12::attr(href)').extract()
		
		for ix, link in enumerate(links): # follow links to activity pages
			ix += 1
			loader = ItemLoader(item=ActivityItem(), response=response)
			loader.add_value('activity_id', ix)
			loader.add_value('url', response.urljoin(link))

			request = scrapy.Request(response.urljoin(link), callback=self.parse_activity, priority=-1)
			request.meta['loader'] = loader
			yield request


	def parse_activity(self, response):
		loader = response.meta['loader']
		sel = Selector(response)
		loader.add_value('date', datetime.strptime(sel.css('tr:nth-child(1) a::text').extract_first(), '%B %d, %Y').date())
		loader.add_value('activity', sel.css('td tr:nth-child(2) td+ td::text').extract_first())
		loader.add_value('location', sel.css('#colTripleMiddle tr:nth-child(3) a::text').extract_first())
		loader.add_value('source', sel.css('tr:nth-child(5) a::text').extract_first())
		loader.add_value('topics', sel.css('tr:nth-child(6) a::text').extract())
		loader.add_value('attendees', sel.css('#colTripleMiddle tr:nth-child(4) a::text').extract())
		loader.add_value('attendees_links', sel.css('#colTripleMiddle tr:nth-child(4) a::attr(href)').extract())
		loader.add_value('ncv_links', sel.css('#colTripleMiddle tr:nth-child(4) a::attr(href)').extract(), re='(.*type=ncv.*)')
		ncv_links = loader.get_collected_values('ncv_links')
		# len_nvc_links = len(ncv_links)

		callstack = []
		for lnk in ncv_links:
			callstack.append({'url' : 'http://chinavitae.com/vip/' + lnk, 'callback' : self.get_official_name_and_title})
		response.meta['callstack'] = callstack

		if len(ncv_links) > 0:
			if 'index.php?mode=events&type=ncv&sn=Chiang&gn=Pin-kung' in ncv_links: # duplicate test case
				print('\n duplicate test case')
				print(callstack)
				return self.callnext(response)
			

	def get_official_name_and_title(self, response):
		"""
		alsdfjasdkljfalsdfa
		"""
		loader = response.meta['loader'] 
		off_dict = {}
		off_dict['name'] = 'some_name_xxx'
		off_dict['title'] = 'some_title_xxx'

		loader.add_value('officials', off_dict)
		return self.callnext(response)


	def callnext(self, response):
		''' Call next target for the item loader, or yields it if completed. '''
		# Get the meta object from the request, as the response
		# does not contain it.
		meta = response.request.meta
		
		# Items remaining in the stack? Execute them
		if len(meta['callstack']) > 0:
			target = meta['callstack'].pop(0)
			yield scrapy.Request(target['url'], meta=meta, callback=self.get_official_name_and_title, errback=self.callnext)
		else:
			# print('***** LOADING ITEM *****')
			yield meta['loader'].load_item()


class ActivityItem(scrapy.Item):
	activity_id = scrapy.Field()
	url = scrapy.Field()
	date = scrapy.Field()
	activity = scrapy.Field()
	location = scrapy.Field()
	source = scrapy.Field()
	topics = scrapy.Field()
	attendees = scrapy.Field()
	attendees_links = scrapy.Field()
	ncv_links = scrapy.Field()
	officials = scrapy.Field()










	# def parse_officials2(self, response):
	# 	#item = response.meta['item']
	# 	loader = response.meta['loader']
	# 	i = response.meta['i'] # official counter?
	# 	#officials_list_all = response.meta['officials_list_all']
	# 	loader.add_value('officials', 'inside ncv_links loop')

	# 	'''off_num = 'official_' + str(i+1)
	# 	off_dict = {}
	# 	off_dict['name'] = 'some_name_xxx'
	# 	off_dict['title'] = 'some_title_xxx'
	# 	new_el = {off_num:off_dict}
	# 	#officials_list_all.append(new_el)	
	# 	#item['officials'] = officials_list_all
	# 	loader.add_value('officials', new_el)'''
		
	# 	return loader	



# 	def parse_officials(self, response):
# 		print('\t*** Called parse_officials on %s', response.url)
# 		item = response.meta['item']
# 		i = response.meta['i'] # official counter?
# 		officials_list_all = response.meta['officials_list_all']

# 		for row_ix in range(0, len(response.css('td td:nth-child(1) .link12').extract())): # loop through all "rows" on this official's page
# 			regex_date = re.compile(r'\d{2}\/\d{2}\/\d{2}')
# 			regex_cq = re.compile(r'Chongqing')
# 			raw_text = response.css('tr:nth-child('+str(row_ix+1)+') .link12::text , tr:nth-child('+str(row_ix+1)+') strong::text').extract()
			
# 			start_ix = [x for x, item in enumerate(raw_text) if re.search('\(', item)][0] - 1 # 7
# 			#end_ix = [i for i, item in enumerate(ex) if re.search('Others Attending', item)][0] # 12

# 			if regex_date.search(raw_text[0]): # first element is a date
# 				if regex_cq.search(raw_text[3]): # fourth element is chongqing
# 					print('Date: ', datetime.strptime(raw_text[0], '%m/%d/%y'))
# 					print('Location: ', raw_text[3])
# 					#print(s[start_ix : end_ix])
# 					off_counter = 0
# 					for j in range(start_ix, len(raw_text)): # loop through elements in relavent portion of raw text [end_ix]
# 						if '(' in raw_text[j]: # element with official title/parentheses
# 							off_counter += 1 # found an official
# 							print('Name ' + str(off_counter) + ': ', raw_text.__getitem__(j-1))
# 							print('Title ' + str(off_counter) + ': ', re.sub('[()]', '', raw_text[j]).strip())

# 							off_num = 'official_' + str(off_counter)
# 							off_dict = {}
# 							off_dict['name'] = raw_text.__getitem__(j-1)
# 							off_dict['title'] = re.sub('[()]', '', raw_text[j]).strip()
# 							new_el = {off_num:off_dict}
# 							officials_list_all.append(new_el)
# 				else: # fourth element NOT chongqing
# 					continue
# 					#print('No city match. This is row number ', row_ix+1)
# 			else: # first element NOT a date
# 				continue


# 		'''raw_text = response.css('tr:nth-child(1) .link12::text').extract()
# 		for ix, off_title in enumerate(raw_text): # loop thru list of raw text elements
# 			if '(' in off_title: # found list element containing official title/parentheses
# 				off_num = 'official_' + str(i+1)
# 				off_dict = {}
# 				off_dict['name'] = raw_text.__getitem__(ix-1)
# 				off_dict['title'] = re.sub('[()]', '', off_title).strip()
# 				new_el = {off_num:off_dict}
# 				officials_list_all.append(new_el)
# 				#item['officials'] = officials_list_all
# 				#return item

# 				officials_dict = {}
# 				#od_key_name = 'official_name'
# 				#od_key_name = 'official_' + str(i) + '_name'
# 				officials_dict['official_name'] = raw_text.__getitem__(ix-1)
# 				#od_key_title = 'official_title'
# 				#od_key_title = 'official_' + str(i) + '_title'
# 				officials_dict['official_title'] = re.sub('[()]', '', off_title).strip()
# 				officials_list.append(officials_dict)
# 				item['officials'] = officials_list
# 				return item

# 			else: # list element doesn't contain title/parentheses
# 				continue'''
# 		item['officials'] = officials_list_all
# 		return item

# 				#if (ix + 1) == len(raw_text): # reached last element of list
# 					#officials_list_all = list()
# 					#item['officials'] = officials_list_all
# 					#return item
# 				#else: # not last element of list, and list element doesn't contain title
# 					#continue


