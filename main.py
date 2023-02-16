
from test import (
    Bashen,
    Dipan,
    Jiuxing,
    get_last_jieqi,
    sanyuan,
    wuxing_sheng_ke,
    yinyangju,
)

from date_utils import calculate_gan_zhi
from konstant import gz, jiaxun, jiuxing2wuxing, jiuxingzhudi, jushu, tiangan2wuxing, yuefen2wuxing

# 输入日期和时间
date = '2023-2-13 20:59'

# 计算年月日时干支和阴历月份
ngz, ygz, rgz, sgz, yly = calculate_gan_zhi(date)
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

# 计算日干五行和阴历月份五行的生克关系
print(f'日月凶吉: {wuxing_sheng_ke(rgwuxing, ywuxing)}')

# 计算日干五行和日干所在地盘九宫位置五行的生克关系
print(f'地盘凶吉: {wuxing_sheng_ke(rgwuxing, jiugongwuxing)}')

print('#########################')

# 查询日干对应的九星驻地
riganjiuxingzhudi = dipan.get_jiuxing_zhudi(rg)
print('日干对应的九星驻地', riganjiuxingzhudi)

# 计算时干支对应的甲旬
jx = jiaxun[int(gz.index(sgz) / 10)]
print('时干支对应的甲旬为', jx)

# 确定值符
zhifu = jx[2]
print('值符为', zhifu)
# 确定值符所在的九宫位置编号
zhifujiugong = dipan.tiangan2index(zhifu)
# 如果值符位于中宫，则看坤二宫
if zhifujiugong == 4:
    zhifujiugong = 1
# 由值符九宫位置确定值符九星
zhifujiuxing = jiuxingzhudi[zhifujiugong]
print('值符所在九宫对应的九星', zhifujiuxing)

# 排九星盘
jiuxing = Jiuxing(zhifujiuxing, sgz, dipan)
print(jiuxing)
riganjiugong = dipan.tiangan2index(rgz[0])
riganjiuxing = jiuxing.index2jiuxing(riganjiugong)
riganjiuxingwuxing = jiuxing2wuxing[riganjiuxing]
print('日干九星五行为', riganjiuxingwuxing)
print('日干九星与日干的凶吉', wuxing_sheng_ke(riganjiuxingwuxing, rgwuxing))
print('#########################')

# 开始排八神盘
bs = Bashen(zhifujiugong, ju)
print(bs)
riganbashen = bs.index2bashen(riganjiugong)

print('#########################')

