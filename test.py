from skyfield import almanac
from skyfield import almanac_east_asia as almanac_ea
from skyfield import api

from date_utils import gz

jushu = {
    '冬至':{
        '上元':1,
        '中元':7,
        '下元':4
    },
    '小寒':{
        '上元':2,
        '中元':8,
        '下元':5
    },
    '大寒':{
        '上元':3,
        '中元':9,
        '下元':6
    },
    '立春':{
        '上元':8,
        '中元':5,
        '下元':2
    },
    '雨水':{
        '上元':9,
        '中元':6,
        '下元':3
    },
    '惊蛰':{
        '上元':1,
        '中元':7,
        '下元':4
    },
    '春分':{
        '上元':3,
        '中元':9,
        '下元':6
    },
    '清明':{
        '上元':4,
        '中元':1,
        '下元':7
    },
    '谷雨':{
        '上元':5,
        '中元':2,
        '下元':8
    },
    '立夏':{
        '上元':4,
        '中元':1,
        '下元':7
    },
    '小满':{
        '上元':5,
        '中元':2,
        '下元':8
    },
    '芒种':{
        '上元':6,
        '中元':3,
        '下元':9
    },
    '夏至':{
        '上元':9,
        '中元':3,
        '下元':6
    },
    '小暑':{
        '上元':8,
        '中元':2,
        '下元':5
    },
    '大暑':{
        '上元':7,
        '中元':1,
        '下元':4
    },
    '立秋':{
        '上元':2,
        '中元':5,
        '下元':8
    },
    '处暑':{
        '上元':1,
        '中元':4,
        '下元':7
    },
    '白露':{
        '上元':9,
        '中元':3,
        '下元':6
    },
    '秋分':{
        '上元':7,
        '中元':1,
        '下元':4
    },
    '寒霜':{
        '上元':6,
        '中元':9,
        '下元':3
    },
    '霜降':{
        '上元':5,
        '中元':8,
        '下元':2
    },
    '立冬':{
        '上元':6,
        '中元':9,
        '下元':3
    },
    '小雪':{
        '上元':5,
        '中元':8,
        '下元':2
    },
    '大雪':{
        '上元':4,
        '中元':7,
        '下元':1
    },
}

def sanyuan(rgz):
    gz_index = gz.index(rgz) + 1
    i = gz_index % 15
    if int(i / 5) == 0:
        return '上元'
    elif int(i / 5) == 1:
        return '中元'
    elif int(i / 5) == 2:
        return '下元'

def get_last_jieqi(date):
    
    nian, yue, ri = date.split('-')
    nian, yue, ri = int(nian), int(yue), int(ri)


    eph = api.load('de421.bsp')
    ts = api.load.timescale()
    t0 = ts.utc(nian, 1, 1)
    t1 = ts.utc(nian, yue, ri)
    t, tm = almanac.find_discrete(t0, t1, almanac_ea.solar_terms(eph))

    jieqis = []
    for tmi, _ in zip(tm, t):
        jieqis.append(almanac_ea.SOLAR_TERMS_ZHS[tmi])
    
    return jieqis[-1]

dipan_tiangan = '戊 己 庚 辛 壬 癸 丁 丙 乙'.split(' ')

tiangan2wuxing = {'甲':'木',
                  '乙':'木',
                  '丙':'火',
                  '丁':'火',
                  '戊':'土',
                  '己':'土',
                  '庚':'金',
                  '辛':'金',
                  '壬':'水',
                  '癸':'水',
                  }

yuefen2wuxing = {
    '正月':'木',
    '二月':'木',
    '三月':'土',
    '四月':'火',
    '五月':'火',
    '六月':'土',
    '七月':'金',
    '八月':'金',
    '九月':'土',
    '十月':'水',
    '十一月':'水',
    '十二月':'土'
}

def get_jiugong_wuxing(i):
    if i in [1, 4, 7]:
        return '土'
    elif i in [8]:
        return '火'
    elif i in [0]:
        return '水'
    elif i in [5, 6]:
        return '金'
    elif i in [2, 3]:
        return '木'

def wuxing_sheng_ke(zhu, ke):
    wuxing = '金 水 木 火 土'.split(' ')
    index_zhu = wuxing.index(zhu)
    index_ke = wuxing.index(ke)
    shengke = index_zhu - index_ke
    if shengke == 0:
        return '旺'
    elif shengke == -1 or shengke == 4:
        return '相'
    elif shengke == -2 or shengke == 3:
        return '休'
    elif shengke == -3 or shengke == 2:
        return '囚'
    elif shengke == -4 or shengke == 1:
        return '死'