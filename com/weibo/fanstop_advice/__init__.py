# -*- coding: utf-8 -*-
__author__ = 'Zealot'

import logging as logger

logger.basicConfig(level=logger.DEBUG,
                    format='%(asctime)s %(levelname)s %(filename)s[line:%(lineno)d] %(message)s'
                    )
# logger.info("123")

#
# handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # 实例化handler
# fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
#
# formatter = logging.Formatter(fmt)   # 实例化formatter
# handler.setFormatter(formatter)      # 为handler添加formatter
#
# logger = logging.getLogger()    # 获取名为tst的logger
# logger.addHandler(handler)           # 为logger添加handler
# logger.setLevel(logging.DEBUG)
#
# logger.info('first info message')
# logger.debug('first debug message')
# logger.error("234")
# logger.