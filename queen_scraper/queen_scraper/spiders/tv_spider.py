import scrapy

class TvSpider(scrapy.Spider):
    name = 'tv'

    start_urls = ['http://tvepisodes.queentorrent.net/',]

    def parse(self, response):
        # follow links to author pages
        if response.css('span a[title]') != None:
            for href in response.css('span a[title]'):
                href = href.css('::attr(href)').extract_first()
                print(1)
                print(href)
                if href is not None:
                    href = response.urljoin(href)            
                    yield scrapy.Request(href, callback=self.parse_tv)

        # follow pagination links
        
##        for href in response.css('span a::attr(href)'):
##            yield response.follow(href, self.parse)
##                next_page = response.css('li.next a::attr(href)').extract_first()
        if response.css('span a::attr(href)') != None:

            href = response.css('span a::attr(href)').extract_first()
            print(2)
            print(href)
            if href is not None:
                href = response.urljoin(href)
                yield scrapy.Request(href, callback=self.parse)    

    #story = response.css('div.container span').extract_first()
    #a = story[story.index('</h2>')+5:story.index("<p>")]
    #head title
    def parse_tv(self, response):
        story = response.css('div.container span').extract_first()
        a = story[story.index('</h2>')+5:story.index("<p>")]
        a = a.replace('\t','').replace('\n','').replace('\r','')
        title = response.css('head title').extract_first()
        yield {
            'story': a,
            'title': title,
        }