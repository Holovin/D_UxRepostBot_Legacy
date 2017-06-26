import requests
from config import Config


class Network:
    def __init__(self, logger):
        self.last_answer = None
        self.session = requests.Session()
        self.logger = logger

    def get_data(self):
        return self.last_answer.text

    def get_data_json(self):
        return self.last_answer.json()

    def do_get(self, url):
        self.logger.debug("Get url: " + url)

        try:
            self.last_answer = self.session.get(url, headers=Config.HEADERS)
            self.logger.debug("Result url (" + str(self.last_answer.status_code) + " : " + self.last_answer.url + ")")

            if self.last_answer.url.lower() != url.lower():
                self.logger.warning("Redirect to: " + self.last_answer.url)

        except requests.exceptions.RequestException as e:
            self.logger.warning("Fatal error [get url]: " + str(e))
            return False

        self.logger.debug("Getting url... ok")
        return True

    def do_post(self, url, data):
        self.logger.debug("Post url: " + url)

        try:
            self.last_answer = self.session.post(url, headers=Config.HEADERS, data=data)
            self.logger.debug("Result url (" + str(self.last_answer.status_code) + " : " + self.last_answer.url + ")")

        except requests.exceptions.RequestException as e:
            self.logger.warning("Fatal error [post url]: " + str(e))
            return False

        self.logger.debug("Posting url... ok")
        return True
