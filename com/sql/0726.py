__author__ = 'Zealot'
#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()

def main(id):
    #get person
    sql = """
        select  id,
                email,
                mobile,
                enabled,
                emailVerified,
                mailNotifierSetting,
                groupName,
                ipAddress,
                lastLogondate,
                updateDate,
                regdate,
                address,
                birthday,
                sex,
                star
         from userinfo.person where id = %s
          """
    readcur.execute(sql % (id,))
    personrows = readcur.fetchone()


    if personrows:
        #get person field
        sql = """
            select  totalViews,
                    totalTopics,
                    grade,
                    totalMarks,
                    totalArticles,
                    level,
                    updateDate,
                    EXP,
                    totalPlayLists
                    from userinfo.personfield
            where id = %s
        """
        readcur.execute(sql % (id,))
        personfieldrows = readcur.fetchone()

        if personfieldrows:
            personlist = [ str(a).replace(',','') for a in personrows ]
            for k in personfieldrows:
                personlist.append(str(k).replace(',',''))
            print ','.join(personlist)

if __name__ == '__main__':
    pool = Pool(4)
    print(1)
    readconn = MySQLdb.connect(host='userinfoslave1.mysql.yyt', user='readonly', passwd='readonly', charset='utf8')
    readcur = readconn.cursor()
    sid = 0
    offset = 200

    while sid <= 50969266:
    #while sid <= 202:
        endid = sid + offset
        idlist = [ n for n in range(sid,endid) ]
        pool.map(main,idlist)
        sid = endid

    sys.exit()
