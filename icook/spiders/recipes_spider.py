import scrapy


def create_category_paths(categories: list) -> list:
    """Construct flat category list into 2D array, remove 全部分類.
    
    Arguments:
        categories {list} -- [description]
    
    Returns:
        list -- [description]
    """
    paths = []
    path = []
    for category in categories:
        if category == '全部分類':
            if path:
                paths.append(path)
            path = []
        else:
            path.append(category)
    if path:
        paths.append(path)
    return paths


class RecipesSpider(scrapy.Spider):
    name = "icook"
    start_urls = [
        'https://icook.tw/categories/',
    ]

    def parse(self, response):
        urls = response.xpath('//a[@class="list-title"]/@href').extract()
        for url in urls:
            yield response.follow(url, callback=self.parse_category)

    def parse_category(self, response):
        urls = response.xpath((
            '//div[@class="browse-recipe-content"]'
            '/a[@class="browse-recipe-name"]/@href')
        ).extract()
        for url in urls:
            yield response.follow(url, callback=self.parse_receipes)

        next_page = response.xpath(('//a[@rel="next"]/@href')).extract_first()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_category)

    def parse_receipes(self, response):
        title = response.css('title::text').get()
        author_name = response.css('a.author-name-link::text').get()
        author_id = response.xpath('//a[@class="author-name-link"]/@href').re_first(r'/users/(.*)/recipes')
        categories = response.xpath(
            '//div[@class="findmore inner-block"]/div[@class="category-tags"]/ul/li/a/text()').getall()
        category_paths = create_category_paths(categories)
        description = ''.join(response.xpath(
            '//div[@class="header-row description"]/p/text()').getall())

        ingredients = []
        for node in response.css('div.ingredient'):
            ingredient_name = node.css('div.ingredient-name::text').extract_first()
            ingredient_unit = node.css('div.ingredient-unit::text').extract_first()
            ingredients.append((ingredient_name, ingredient_unit))

        steps = response.xpath('//li[@class="step"]/div/div/text()').getall()
        heart_num = response.xpath('//span[@class="stat"]/span[@class="stat-content"]/text()').re_first(r'收藏 (.*)')
        recommend_num = response.xpath('//span[@class="stat"]/span[@class="stat-content"]/span/a/text()').get()
        servings_num = response.xpath('//div[@class="servings"]/span[@class="num"]/text()').get()
        servings_unit = response.xpath('//div[@class="servings"]/span[@class="unit"]/text()').get()
        time_num = response.xpath('//div[@class="time-info info-block"]/div[@class="info-content"]/span[@class="num"]/text()').get()
        time_unit = response.xpath('//div[@class="time-info info-block"]/div[@class="info-content"]/span[@class="unit"]/text()').get()

        yield {
            'url': response.url,
            'tilte': title,
            'author_name': author_name,
            'author_id': author_id,
            'category_paths': category_paths,
            'description': description,
            'ingredients': ingredients,
            'steps': steps,
            'heart_num': heart_num,
            'recommend_num': recommend_num,
            'servings': (servings_num, servings_unit),
            'time': (time_num, time_unit)
        }
