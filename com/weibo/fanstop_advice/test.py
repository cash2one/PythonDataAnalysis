__author__ = 'Zealot'
import utils as util
import cPickle as ce
import sys
reload(sys)
sys.setdefaultencoding('utf8')
util.logger.info("123")
def main():
    util.logger.info("123")
    a=1
    b=True
    util.logger.info(["123",a,b])

if __name__ == '__main__':
    main()