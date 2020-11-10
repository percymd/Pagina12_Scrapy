import scrapy
from scrapy.crawler import CrawlerProcess

class Spider12(scrapy.Spider):
    name = 'spider12'
    allowed_domains = ['pagina12.com.ar']
    custom_settings = {'FEED_FORMAT': 'json',
                       'FEED_URI': 'resultados.json',
                       'FEED_EXPORT_ENCODING': 'utf-8',
                       'DEPTH_LIMIT': 2}
    
    start_urls = ['https://www.pagina12.com.ar/secciones/el-pais',
                  'https://www.pagina12.com.ar/secciones/economia',
                  'https://www.pagina12.com.ar/secciones/sociedad',
                  'https://www.pagina12.com.ar/suplementos/cultura-y-espectaculos',
                  'https://www.pagina12.com.ar/secciones/deportes',
                  'https://www.pagina12.com.ar/secciones/el-mundo',
                  'https://www.pagina12.com.ar/secciones/contratapa']
    
    def parse(self, response):
        # Artículo promocionado
        nota_promocionada = response.xpath('//section[@class="top-content"]//h2/a/@href').get()
        if nota_promocionada is not None:
            yield response.follow (nota_promocionada, callback=self.parse_nota)
        
        # notas secundarias
        notas_secundarias = response.xpath('//div[@class="articles-list is-grid-col2 grid-mobile-row"]//h3/a/@href').getall()
        for nota_sec in notas_secundarias:
            yield response.follow(nota_sec, callback=self.parse_nota)
        
        # Listado notas
        notas = response.xpath('//div[@class="article-list"]//h4/a/@href').getall()
        for nota in notas:
            yield response.follow(nota, callback=self.parse_nota)
            
        # Link a la siguiente página
        next_page = response.xpath('//a[@class"next"]/@href')
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        
    def parse_nota(self, response):
        titulo = response.xpath('//div[@class="article-titles"]/h1/text()').get()
        volanta = response.xpath('//div[@class="article-titles"]/h2/text()').get()
        fecha = response.xpath('//div[@class="time"]/span/@datetime').get()
        copete = response.xpath('//div[@class="article-sumary"]/text()').get()
        autor = response.xpath('//div[@class="article-author"]/text()').get()
        cuerpo = response.xpath('//div[@class="article-text"]/p/text()').get()
        yield {'url': response.url,
               'titulo': titulo,
               'volanta': volanta,
               'fecha': fecha,
               'copete': copete,
               'autor': autor,
               'cuerpo': cuerpo}

process = CrawlerProcess()
process.crawl(Spider12)
process.start()