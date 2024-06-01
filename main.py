import time

from module1.jobs.specialized_jobs.amazon_job import AmazonJob
from module1.scrapers.portal_scrapers.amazon import AmazonScraper 


if __name__ == "__main__":
    start_time = time.time()

    # Example usage
    amazon = AmazonScraper(
        baseUrl="https://hvr-amazon.my.site.com",
        jobSearchKeyword='',
        location={'country': 'CA', 'state': 'ON'},
        timeType='Part Time'
    )

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Script executed in {elapsed_time:.2f} seconds.")
