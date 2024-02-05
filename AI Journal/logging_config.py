import logging


def configure_logging(log_file_path='error_log.txt', level=logging.INFO,
                      format_str='%(asctime)s - %(levelname)s - %(message)s', filemode='a'):
    logging.basicConfig(filename=log_file_path, level=level, format=format_str, filemode=filemode)
