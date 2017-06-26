from helpers.network import Network


class API:
    API_TELEGRAM_URL = 'https://api.telegram.org'

    def __init__(self, bot_id, secret_token):
        self.bot_id = bot_id
        self.secret_token = secret_token
        self.network = Network()

    def _build_url(self, method_name):
        return API.API_TELEGRAM_URL + '/bot' + self.bot_id + ':' + self.secret_token + '/' + method_name

    def api_forward_message(self, chat_id, from_chat_id, disable_notification, message_id):
        url = self._build_url('forwardMessage')

        params = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'disable_notification': disable_notification,
            'message_id': message_id
        }

        if self.network.do_post(url, params):
            return self.network.get_data_json()

        else:
            return None

    @staticmethod
    def api_check_success(json):
        if not json.get('ok', False):
            return False

        return True
