
from test import Dipan, get_last_jieqi, sanyuan, wuxing_sheng_ke, yinyangju

from date_utils import gan_zhi
from konstant import dipan_tiangan, jushu, tiangan2wuxing, yuefen2wuxing, jiuxingzhudi

# 输入日期和时间
date = '2023-2-13 20:59'

# 计算年月日时干支和阴历月份
ngz, ygz, rgz, sgz, yly = gan_zhi(date)
print(f'{ngz}年{ygz}月{rgz}日{sgz} 阴历{yly}')

# 判断上中下元
yuan = sanyuan(rgz)
print(yuan)

# 计算上一个节气
nian = date.split(' ')[0]
last_jieqi = get_last_jieqi(nian)
print(f'上一个节气为{last_jieqi}')

ju = yinyangju(last_jieqi)
shu = jushu[last_jieqi][yuan]
print(f'此局为{ju}{shu}局')

# 排地盘九宫
dipan = Dipan(ju, shu)
print(dipan)

# 日干
rg = rgz[0]

# 获取日干五行
rgwuxing = tiangan2wuxing[rg]
print('日干五行', rgwuxing)

# 获取阴历月份五行
ywuxing = yuefen2wuxing[yly]
print('月份五行', ywuxing)

# 获取地盘九宫五行
jiugongwuxing = dipan.get_jiugong_wuxing(rg)
print('地盘五行', jiugongwuxing)

print(f'日月凶吉: {wuxing_sheng_ke(rgwuxing, ywuxing)}')

print(f'地盘凶吉: {wuxing_sheng_ke(rgwuxing, jiugongwuxing)}')

riganjiuxing = jiuxingzhudi[dipan.index(rg)]
riganjiuxing





