import logging

import requests

from config import Config


class Network:
    def __init__(self):
        self.last_answer = None
        self.session = requests.Session()

    def get_data(self):
        return self.last_answer.text

    def get_data_json(self):
        return self.last_answer.json()

    def do_get(self, url):
        logging.debug("Get url: " + url)

        try:
            self.last_answer = self.session.get(url, headers=Config.HEADERS)
            logging.debug("Result url (" + str(self.last_answer.status_code) + " : " + self.last_answer.url + ")")

            if self.last_answer.url.lower() != url.lower():
                logging.warning("Redirect to: " + self.last_answer.url)

        except requests.exceptions.RequestException as e:
            logging.warning("Fatal error [get url]: " + str(e))
            return False

        logging.debug("Getting url... ok")
        return True

    def do_post(self, url, data):
        logging.debug("Post url: " + url)

        try:
            self.last_answer = self.session.post(url, headers=Config.HEADERS, data=data)
            logging.debug("Result url (" + str(self.last_answer.status_code) + " : " + self.last_answer.url + ")")

        except requests.exceptions.RequestException as e:
            logging.warning("Fatal error [post url]: " + str(e))
            return False

        logging.debug("Posting url... ok")
        return True
