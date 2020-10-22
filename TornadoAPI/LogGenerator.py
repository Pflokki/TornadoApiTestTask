from pathlib import Path
import string
import random
import json

LOG_LEVEL = ["DEBUG", "INFO", "WARN", "ERROR"]


def create_message(length=10):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def get_log_record():
    return json.dumps(
        {
            "level": random.choice(LOG_LEVEL),
            "message": create_message()
        }
    )


def create_log(path, message_count=10000):
    with open(path, 'w') as log_file:
        for _ in range(message_count):
            log_file.write(f"{get_log_record()}\n")


if __name__ == '__main__':
    file_path = Path().absolute().joinpath("log_file.log")
    create_log(file_path)
