from skyfield import almanac
from skyfield import almanac_east_asia as almanac_ea
from skyfield import api

from konstant import bashen, dipan_tiangan, jiuxingzhudi, yangjieqi, yinjieqi


def sanyuan(gz):
    '''由干支计算上中下元'''
    gz_index = gz.index(gz) + 1
    i = gz_index % 15
    if int(i / 5) == 0:
        return '上元'
    elif int(i / 5) == 1:
        return '中元'
    elif int(i / 5) == 2:
        return '下元'

def get_last_jieqi(date):
    '''由日期得上一个节气'''
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

def wuxing_sheng_ke(zhu, ke):
    '''计算五行生克关系'''
    wuxing = '金 水 木 火 土'.split(' ')
    index_zhu = wuxing.index(zhu)
    index_ke = wuxing.index(ke)
    shengke = index_zhu - index_ke
    if shengke == 0:
        return '旺(大吉)'
    elif shengke == -1 or shengke == 4:
        return '相(小吉)'
    elif shengke == -2 or shengke == 3:
        return '休(小凶)'
    elif shengke == -3 or shengke == 2:
        return '囚(小凶)'
    elif shengke == -4 or shengke == 1:
        return '死(大凶)'

def yinyangju(last_jieqi):
    '''根据上一个节气判断是阳局还是阴局'''
    if last_jieqi in yangjieqi:
        return '阳'
    elif last_jieqi in yinjieqi:
        return '阴'
    else:
        raise ValueError

class Dipan:
    
    def __init__(self, ju, shu):
        self.ju = ju
        self.shu = shu
        self._make()
    
    def _make(self):
        '''根据阴阳局和局数创建地盘九宫'''
        # 初始化地盘九宫矩阵
        self.dipan = [1] * 9

        next = self.shu
        for i in range(9):
            
            # 按顺序排盘
            self.dipan[next - 1] = dipan_tiangan[i]
            
            # 阳顺阴逆
            if self.ju == '阳':
                next += 1
            else:
                next -= 1
            
            # 收尾相接
            if next > 9:
                next = 1
            elif next < 1:
                next = 9

    def __str__(self):
        '''显示地盘九宫'''
        return f'''     
        地盘九宫
        {self.dipan[3]} {self.dipan[8]} {self.dipan[1]}
        {self.dipan[2]} {self.dipan[4]} {self.dipan[6]}
        {self.dipan[7]} {self.dipan[0]} {self.dipan[5]}
        '''
    
    def index2tiangan(self, index):
        '''用位置编号查询地盘九宫中对应位置天干'''
        return self.dipan[index]
    
    def tiangan2index(self, tiangan):
        '''用天干查询在地盘九宫中的位置编号'''
        return self.dipan.index(tiangan)
    
    def get_jiugong_wuxing(self, tiangan):
        '''由九宫所在位置得到九宫五行'''
        index = self.tiangan2index(tiangan)
        if index in [1, 4, 7]:
            return '土'
        elif index in [8]:
            return '火'
        elif index in [0]:
            return '水'
        elif index in [5, 6]:
            return '金'
        elif index in [2, 3]:
            return '木'
    
    def get_jiuxing_zhudi(self, tiangan):
        '''查询天干对应位置的九星驻地'''
        index = self.tiangan2index(tiangan)
        jgzd = jiuxingzhudi[index]
        return jgzd

class Jiuxing:
    
    def __init__(self, zhifujiuxing, shiganzhi, dipan):
        self.zhifujiuxing = zhifujiuxing
        self.shiganzhi = shiganzhi
        self.dipan = dipan
        self._make()
        
    def _make(self):
        self.jiuxing = [1] * 9
        self.jiuxing[4] = '禽'
        jiuxingshunxu = '蓬 任 冲 辅 英 芮 柱 心'.split(' ')
        jiugongshunxu = [0, 7, 2, 3, 8, 1, 6, 5]
        shiganjiugong = self.dipan.tiangan2index(self.shiganzhi[0])
        a = jiugongshunxu.index(shiganjiugong)
        new_jiugongshunxu = jiugongshunxu[a:] + jiugongshunxu[:a]
        b = jiuxingshunxu.index(self.zhifujiuxing)
        new_jiuxingshunxu = jiuxingshunxu[b:] + jiuxingshunxu[:b]
        for i in range(8):
            self.jiuxing[new_jiugongshunxu[i]] = new_jiuxingshunxu[i]
    
    def __str__(self):
        '''显示九星九宫'''
        return f'''     
        九星九宫
        {self.jiuxing[3]} {self.jiuxing[8]} {self.jiuxing[1]}
        {self.jiuxing[2]} {self.jiuxing[4]} {self.jiuxing[6]}
        {self.jiuxing[7]} {self.jiuxing[0]} {self.jiuxing[5]}
        '''
    
    def index2jiuxing(self, index):
        return self.jiuxing[index]
    
    def jiuxing2index(self, jx):
        return self.jiuxing.index(jx)
    

class Bashen:
    
    def __init__(self, zhifujiugong, ju):
        self.zhifujiugong = zhifujiugong
        self.ju = ju
        self._make()
    
    def _make(self):
        if self.ju == '阳':
            bashen_shunxu = bashen
        else:
            bashen_shunxu = bashen[::-1]
        jiugongshunxu = [0, 7, 2, 3, 8, 1, 6, 5]
        a = jiugongshunxu.index(self.zhifujiugong)
        new_jiugongshunxu = jiugongshunxu[a:] + jiugongshunxu[:a]
        self.bashen = [1] * 9
        self.bashen[4] = '  '
        for i in range(8):
            self.bashen[new_jiugongshunxu[i]] = bashen_shunxu[i]
    
    def __str__(self):
        '''显示八神九宫'''
        return f'''     
        八神九宫
        {self.bashen[3]} {self.bashen[8]} {self.bashen[1]}
        {self.bashen[2]} {self.bashen[4]} {self.bashen[6]}
        {self.bashen[7]} {self.bashen[0]} {self.bashen[5]}
        '''