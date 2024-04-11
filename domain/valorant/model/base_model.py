# -*- coding: utf-8 -*-

import datetime
import hashlib
import os

import pytz


class BaseModel:
    """
    description:
        Class to keep out some methods and variables. The domain valorant has some releative
        and each path need to be classifier
    """

    def __init__(self, data: str) -> None:
        self.created_at = datetime.datetime.now(pytz.timezone(os.environ.get("TZ"))).strftime('%Y-%m-%dT%H:%M:%S')
        self.hash_validator = hashlib.sha256(data.encode('utf-8')).hexdigest()
