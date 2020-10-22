from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from pathlib import Path
import json


class LogSender(RequestHandler):
    log_path = Path('log_file.log')
    offset_step = 50

    def _get_log_total_size(self):
        count = 0
        with open(self.log_path, 'r') as log_file:
            for _ in log_file.readlines():
                count += 1
        return count

    def _get_log_string(self, from_pos, to_pos):
        with open(self.log_path, 'r') as log_file:
            return [
                json.loads(line)
                for index, line in enumerate(log_file)
                if from_pos <= index < to_pos
            ]

    @staticmethod
    def _get_success_message(next_offset, total_size, messages):
        return {
            'ok': True,
            'next_offset': next_offset,
            'total_size': total_size,
            'messages': messages,
        }

    @staticmethod
    def _get_failed_messages(reason):
        return {
            'ok': False,
            'reason': reason,
        }

    def post(self):
        ret_msg = self._get_failed_messages("Internal error")
        try:
            body = json.loads(self.request.body)
            from_pos = int(body['offset'])
            total_size = self._get_log_total_size()
            messages = self._get_log_string(from_pos, from_pos + self.offset_step)
            next_offset = from_pos + self.offset_step \
                if total_size > from_pos + self.offset_step else 0

            ret_msg = self._get_success_message(next_offset, total_size, messages)
        except (ValueError, IndexError):
            ret_msg = self._get_failed_messages("Wrong request")
        except FileNotFoundError:
            ret_msg = self._get_failed_messages("File not found")
        finally:
            self.write(ret_msg)


def make_app():
    urls = [("/read_log", LogSender)]
    return Application(urls)


def api_start():
    app = make_app()
    app.listen(3000)
    IOLoop.instance().start()
