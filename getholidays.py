import scrapy
from scrapy.crawler import CrawlerProcess

# Running Scrapy from a script - this method uses an API to run Scrapy via a script.


class HolidaySpider(scrapy.Spider):

    name = "my_holidays"

    # link: https://www.officeholidays.com/countries/malaysia/{year}

    allowed_domains = ["officeholidays.com"]

    start_urls = [
        "https://www.officeholidays.com/countries/malaysia/2020",
        "https://www.officeholidays.com/countries/malaysia/2021",
        "https://www.officeholidays.com/countries/malaysia/2022",
        "https://www.officeholidays.com/countries/malaysia/2023"
    ]

    def parse(self, response):

        data = response.xpath("//tr[@class='region ']|//tr[@class='country ']")

        # get all data points
        for d in data:
            date = d.xpath(".//*[@itemprop='startDate']").attrib["datetime"]
            holiday = d.css("a.country-listing::text").get()
            type = d.css("td.comments::text").get()
            comment = d.css("td.hide-ipadmobile::text").get()

            yield {
                "date": date,
                "holiday_name": holiday,
                "type": type,
                "comment": comment
            }


# process
if __name__ == "__main__":

    process = CrawlerProcess(settings={
        "FEED_URI": "my_holidays.csv",
        "FEED_FORMAT": "csv"
    })

    process.crawl(HolidaySpider)
    process.start()
