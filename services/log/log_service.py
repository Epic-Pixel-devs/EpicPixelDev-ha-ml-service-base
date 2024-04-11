# -*- coding: utf-8 -*-

import logging


class LogService:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s')

    @staticmethod
    def log():
        return logging
