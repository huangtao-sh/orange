# 项目：标准库函数
# 模块：时间模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2015-09-17 13:24
# 修改：2016-03-12 18:53

import datetime as dt

ZERO = dt.timedelta(0)

# A class building tzinfo objects for fixed-offset time zones.
# Note that FixedOffset(0, "UTC") is a different way to build a
# UTC tzinfo object.

class FixedOffset(dt.tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, offset, name):
        self.__offset = dt.timedelta(minutes = offset)
        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return ZERO

utc=FixedOffset(0,'UTC')

# A class capturing the platform's idea of local time.

import time as _time

STDOFFSET = dt.timedelta(seconds = -_time.timezone)
if _time.daylight:
    DSTOFFSET = dt.timedelta(seconds = -_time.altzone)
else:
    DSTOFFSET = STDOFFSET

DSTDIFF = DSTOFFSET - STDOFFSET

class LocalTimezone(dt.tzinfo):

    def utcoffset(self, dt):
        if self._isdst(dt):
            return DSTOFFSET
        else:
            return STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return DSTDIFF
        else:
            return ZERO

    def tzname(self, dt):
        return _time.tzname[self._isdst(dt)]

    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, 0)
        stamp = _time.mktime(tt)
        tt = _time.localtime(stamp)
        return tt.tm_isdst > 0

Local = LocalTimezone()

def now(tz=Local):
    return datetime.now(tz)

class datetime(dt.datetime):
    def __new__(cls, year, month=None, day=None, hour=0,
                    minute=0, second=0,microsecond=0, tzinfo=Local):
        if isinstance(month,int)and isinstance(day,int):
            return super().__new__(cls,year,month,day,hour,minute,
                                   second,microsecond,tzinfo)
        elif isinstance(year,(float,int)):
            return cls.fromtimestamp(year,tzinfo)
        elif isinstance(year,str):
            args=re.findall(r'\d{1,}',year)
            if len(args)>=5:
                args=[int(x) for x in args]
                return super().__new__(cls,*args,tzinfo=tzinfo)
        elif isinstance(year,(dt.datetime,dt.time)):
            tzinfo=year.tzinfo if year.tzinfo else tzinfo
            return cls.fromtimestamp(year.timestamp(),tzinfo)

    @property
    def utctime(self):
        return self.astimezone(utc)

    @property
    def localtime(self):
        return self.astimezone(Local)
