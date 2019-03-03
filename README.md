# icook crawler
This is a Scrapy project to scrape recipes from [icook](https://icook.tw/).

## Extracted data format

The extracted data looks like this sample:

    {
        "url": "https://icook.tw/recipes/226422",
        "tilte": "柿子烤布丁 by 飄香筆記 - 愛料理",
        "author_name": "飄香筆記",
        "author_id": "Note-a-licious",
        "category paths": [["烘焙點心", "布丁"]],
        "description": "這是一個很簡單的法式烤水果布丁...",
        "ingredients": [
            ["脆柿子", "3 個"],
            ["楓糖", "1 大匙"],
            ["鹽", "一點點"]],
        "steps": [
            "先製作布丁液: 將蛋打至起泡", 
            "加入楓糖和鹽打勻, 然後一點一點地加入麵粉, 攪拌至無顆粒."], 
        "heart_num": "75",
        "recommend_num": null,
        "servings": ["6", "人份"],
        "time": ["90", "分鐘"]
    }


## Running the spiders
Install scrapy if you haven't:

    $ pip install scrapy
You can run a spider using the `scrapy crawl` command, such as:

    $ scrapy crawl icook
If you want to save the scraped data to a file, you can pass the `-o` option:
    
    $ scrapy crawl icook -o recipes.json

These formats are supported out of the box:
* JSON
* JSON lines
* CSV
* XML