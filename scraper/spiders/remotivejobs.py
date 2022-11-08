import scrapy


class RemotivejobsSpider(scrapy.Spider):
    name = 'remotivejobs'
    allowed_domains = ['remotive.com']
    start_urls = ['https://remotive.com/?live_jobs%5Bmenu%5D%5Bcategory%5D=Software%20Development']

    def parse(self, response):
        links = response.css('.job-tile a::attr(href)').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_job)

    def parse_job(self, response):
        job_type = response.css("#job-meta-panel span.remotive-text-xsmaller:contains('Job Type') + span::text").get()
        
        if job_type == 'Contract':
            title = response.css('section h1::text').get()
            salary = response.css("#job-meta-panel span.remotive-text-xsmaller:contains('Salary') + span::text").get()
            location = response.css("#job-meta-panel span.remotive-text-xsmaller:contains('Remote Location') + span::text").get()
            yield {
                'title': response.css('h1::text').get(),
                'salary': salary,
                'location': location,
                'link': response.url
            }