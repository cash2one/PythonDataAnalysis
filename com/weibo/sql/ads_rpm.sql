#查找一段时间内的，订单，广告主的曝光数、订阅数、以及点击率（保留5位）
#如果曝光为0，就忽略这个广告主
#加一个总的平均的RPM,uid为1

SELECT 1,
       round(a.all_attend/a.all_pv,5)
FROM
  (SELECT nvl(sum(CAST(pv AS float)),0) AS all_pv,
          nvl(sum(CAST(attend AS float)),0) AS all_attend
   FROM ads_algo_oid_uid_pv_attend_interaction
   WHERE cast(substring(dt,1,8) AS int) >=20160404) a
UNION ALL
SELECT a.uid,
       round(a.attend_float/a.pv_float,5)
FROM
  (SELECT uid,
          nvl(sum(CAST(pv AS float)),0) AS pv_float,
          nvl(sum(CAST(attend AS float)),0) AS attend_float
   FROM ads_algo_oid_uid_pv_attend_interaction
   WHERE cast(substring(dt,1,8) AS int) >=20160404
   GROUP BY uid) a
WHERE a.pv_float!=0