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
            'source': extract_first_with_css('tr:nth-child(5) a::text'),
            'topics': extract_all_with_css('tr:nth-child(6) a::text')
        }

'''
OLD
        for entry in response.css('[id="colTripleMiddle"] td'):
            yield {
                'date': entry.css('span.boldBlack0::text').extract_first(),
                'activity': entry.css('a::text').extract_first()
            }


>>> entry = response.css('[id="colTripleMiddle"] td')

>>> entry.css('a::text').extract()
['March 12, 2018', 'Beijing Municipality', 'Xi Jinping', '\n\t\t\t\t\t Chung Eui-yong', 'XINHUA Online (English 2010)', 'foreign relations', 'March 12, 2018', 'Beijing Municipality', 'Xi Jinping', '\n\t\t\t\t\t Chung Eui-yong', 'XINHUA Online (English 2010)', 'foreign relations']

>>> entry.css('td::text')[1].extract()
'Xi expects smooth DPRK-ROK summit, DPRK-U.S. dialogue '



>>> date = response.css('tr:nth-child(1) a::text').extract_first()
>>> date
'March 12, 2018'

>>> activity = response.css('td tr:nth-child(2) td+ td::text').extract_first()
>>> activity
'Xi expects smooth DPRK-ROK summit, DPRK-U.S. dialogue '

>>> location = response.css('#colTripleMiddle tr:nth-child(3) a::text').extract_first()
>>> location
'Beijing Municipality'

>>> attendees = response.css('#colTripleMiddle tr:nth-child(4) a::text').extract()
>>> attendees
['Xi Jinping', '\n\t\t\t\t\t Chung Eui-yong']

>>> source = response.css('tr:nth-child(5) a::text').extract_first()
>>> source
'XINHUA Online (English 2010)'

>>> topics = response.css('tr:nth-child(6) a::text').extract()
>>> topics
['foreign relations']








{'date': 'November 18, 2005', 'activity': 'Zhou Yongkang held talks with US Attorney General Alberto Gonzales. ', 'location': 'Beijing Municipality', 'attendees': ['Zhou Yongkang', '\n\t\t\t\t\tAlberto Gonzales'], 'source': 'law and the judiciary', 'topics': []}

>>> l = response.css('tr:nth-child(5) b::text, tr:nth-child(5) a::text').extract()
>>> l
['Topics: ', 'law and the judiciary']
>>>
>>> t = l.pop(0).strip(' :')
>>> t
'Topics'
>>> l
['law and the judiciary']




'''


