import aiohttp


class Scraper:
    def __init__(self, base_url="http://your-api-endpoint.com"):
        self.base_url = base_url

    async def scrape_single(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/fetch", params={"url": url}) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"error": "Failed to fetch data"}

    async def scrape_links(self, url, max_extract=10, execution_time=30):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/fetch/extract", params={"url": url, "max_extract": max_extract,
                                                                             "execution_time": execution_time}) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"error": "Failed to fetch links"}
