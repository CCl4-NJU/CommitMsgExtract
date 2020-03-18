import scrapy
from scrapy import FormRequest, Request
from scrapy.utils import log
from scrapy.utils.response import open_in_browser

commitUrl = []
index = 1 #in order to jump over zhihu project
currentUrl = ""
# prefix = r"/search?q="

with open(r'G:\DiffCommitFile\commit-pure-url.txt', 'r') as urlFile:
    commitUrl = urlFile.readlines()
    urlFile.close()

print(len(commitUrl))

class LoginSpider(scrapy.Spider):
    name = "login"
    start_urls = ['https://github.com/login']
    # def start_scrape(self):
    #     pre = r"https://github.com/search?q="
    #
    #     pnames = []
    #     i = 0
    #     for line in open("G:\\scpy\\commitproject\\commitproject\\names.txt"):
    #         i+=1
    #         pnames.append(line.replace("\n", ""))
    #
    #     urls=[]
    #     for pname in pnames:
    #         completeUrl = pre + pname
    #         urls.append(completeUrl)
    #     print(urls)
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        token = response.xpath('//*[@name="authenticity_token"]/@value').extract_first()
        return FormRequest.from_response(response,
                                        formdata={
                                            'authenticity_token':token,
                                            'login':'171250599@smail.nju.edu.cn',
                                            'password':'SlamDunk1011'},
                                        callback=self.scrape_pages)

        # target = response.css('li.repo-list-item')[0]
        # yield {
        #     'path': target.css('div.col-12 h3 a::attr(href)').get(),
        # }

    def scrape_pages(self, response):
        global currentUrl
        currentUrl = commitUrl[0]
        return Request(url=commitUrl[0],
                       callback=self.parse_tastypage)

    def parse_tastypage(self, response):
        global index
        global currentUrl
        # target = response.css('div.commit full-commit mt-0 px-2 pt-2')
        msgs = response.css('p.commit-title *::text').extract()

        # msg = response.css('p.commit-title::text').get()
        msg0 = msgs[0].replace("\n", " ")
        textRes = msg0

        rest = response.css('div.commit-desc pre::text').get()

        if len(msgs) > 1:
            for i in range(1, len(msgs)):
                msgi = msgs[i].replace("\n", " ")
                textRes = textRes + msgi


        if not rest is None:
            rest = rest.replace("\n", " ")
            textRes = textRes + rest

        head = currentUrl[18:].replace("\n", "")

        print(head + " : " + textRes)
        yield {
            head: textRes
        }

        # relative_path = commitUrl[index].substring(18)
        next_page = commitUrl[index]
        currentUrl = next_page
        index = index + 1
        if index < len(commitUrl):
            # next_page = response.urljoin(relative_path)
            yield Request(next_page, callback=self.parse_tastypage)