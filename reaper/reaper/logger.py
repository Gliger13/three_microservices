import logging


logger = logging.getLogger('reaper')
console_handler = logging.StreamHandler()
console_format = logging.Formatter('%(levelname)-8s | %(asctime)s | %(name)-6s | - %(message)s', "%H:%M:%S")
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

parser_logger = logging.getLogger('jobs_parser')
parser_logger.setLevel(logging.ERROR)

if __name__ == '__main__':
    logger.debug('Some useless information')
    logger.info('Some information')
    logger.warning('Some warning')
    logger.error('Some error')
    logger.critical('Some critical error')
