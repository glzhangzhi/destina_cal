# 由上一个节气以及上中下元得到局数
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

# 阴历月份对应五行
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

# 地盘天干顺序
dipan_tiangan = '戊 己 庚 辛 壬 癸 丁 丙 乙'.split(' ')

# 由天干得到对应五行
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

# 天干
tiangan = '甲 乙 丙 丁 戊 己 庚 辛 壬 癸'.split(' ')

# 地支
dizhi = '子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥'.split(' ')

# 农历日期
nlrq = '初一 初二 初三 初四 初五 初六 初七 初八 初九 初十 十一 十二 十三 十四 十五 十六 十七 十八 十九 二十 廿一 廿二 廿三 廿四 廿五 廿六 廿七 廿八 廿九 三十'.split(' ')

# 农历月份
yuefen = '正月 二月 三月 四月 五月 六月 七月 八月 九月 十月 十一月 十二月'.split(' ')

# 六十甲子干支
gz = []
for i in range(60):
    gz.append(f'{tiangan[i % 10]}{dizhi[i % 12]}')

# 阴阳节气
yangjieqi = '冬至 小寒 大寒 立春 雨水 惊蛰 春分 清明 谷雨 立夏 小满 芒种'.split(' ')
yinjieqi = '夏至 小暑 大暑 立秋 处暑 白露 秋分 寒霜 霜降 李东 小雪 大雪'.split(' ')

# 九星
jiuxing = '蓬 任 冲 辅 英 芮 柱 心 禽'.split(' ')

# 九星驻地
jiuxingzhudi = {
    0:'蓬',
    1:'芮',
    2:'冲',
    3:'辅',
    4:'禽',
    5:'心',
    6:'柱',
    7:'任',
    8:'英'
}