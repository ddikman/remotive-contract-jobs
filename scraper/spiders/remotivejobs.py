import scrapy


class RemotivejobsSpider(scrapy.Spider):
    name = 'remotivejobs'
    allowed_domains = ['remotive.com']
    start_urls = ['https://remotive.com/?live_jobs%5Bmenu%5D%5Bcategory%5D=Software%20Development']

    custom_settings = {
        'FEEDS': {
            'output/jobs.csv': {
                'format': 'csv',
                'overwrite': True
            }
        }
    }

    def parse(self, response):
        links = response.css('.job-tile a::attr(href)').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_job)

    def parse_job(self, response):
        job_type = response.css("#job-meta-panel span.remotive-text-xsmaller:contains('Job Type') + span::text").get()
        
        if job_type == 'Contract':
            title = response.css('section h1::text').get().strip()
            salary = response.css("#job-meta-panel span.remotive-text-xsmaller:contains('Salary') + span::text").get(default='').strip()
            salary = salary.replace('💸\n', '')
            location = response.css("#job-meta-panel span.remotive-text-xsmaller:contains('Location') + span span::text").get(default='').strip()
            yield {
                'title': title,
                'salary': salary,
                'location': location,
                'link': response.url
            }