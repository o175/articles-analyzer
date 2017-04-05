import scrapy
import html2text

class QuotesSpider(scrapy.Spider):
    
    name = "articles"

    def start_requests(self):
        # for id in range(17000..76094): \\ все id статей, которые нас могут интересовать
        for id in range(17000, 17003):
            url = "http://old.novayagazeta.ru/politics/%s.html" %id
            yield scrapy.Request(url=url, callback=self.parse)

            
    def parse(self, response):
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        converter.body_width = 0
        converter.ignore_links = True
        
        page = response.url.split("/")[-1][0:-5]
        filename = '../downloads/NG-%s.txt' % page
        text = converter.handle(response.css('.b-article').extract()[0]) #
        text = text.replace('*', '')
        with open(filename, 'w') as f:
            f.write(text)
        self.log('Saved file %s' % filename)
