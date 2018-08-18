import logging
import os


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


def get_log_dir():
    current_path = os.path.dirname(os.path.realpath(__file__))
    log_dir = os.path.join(current_path, 'log')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    return log_dir


def get_file_logger(name=None, file_name='main.log'):
    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(os.path.join(get_log_dir(), file_name))
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


main_logger = get_file_logger('main', 'main.log')
thread_info_logger = get_file_logger('thread_info', 'thread_info.log')
record_logger = get_file_logger('record', 'record.csv')


if __name__ == '__main__':
    record_logger.critical('Test')

