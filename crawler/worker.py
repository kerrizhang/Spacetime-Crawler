from threading import Thread

from utils.download import download
from utils import get_logger
from scraper import scraper, print_everything
import time


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            scraped_urls = scraper(tbd_url, resp)

            print("Frontier to be downloaded: ", len(self.frontier.to_be_downloaded))
            print("Frontier saved: ", len(self.frontier.save))

            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            #
            if len(self.frontier.save)) == 1000:
                print_everything(1000)
            elif len(self.frontier.save)) == 5000:
                print_everything(5000)
            elif len(self.frontier.save)) == 7000:
                print_everything(7000)
            elif len(self.frontier.save)) == 11000:
                print_everything(11000)
            #
            time.sleep(self.config.time_delay)
        
        print_everything(69)
