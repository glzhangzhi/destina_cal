import math

import ephem

tiangan = '甲、乙、丙、丁、戊、己、庚、辛、壬、癸'.split('、')
dizhi = '子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥'.split('、')
nlrq = '初一 初二 初三 初四 初五 初六 初七 初八 初九 初十 十一 十二 十三 十四 十五 十六 十七 十八 十九 二十 廿一 廿二 廿三 廿四 廿五 廿六 廿七 廿八 廿九 三十'.split(' ')
yuefen = '正月 二月 三月 四月 五月 六月 七月 八月 九月 十月 十一月 十二月'.split(' ')
gz = []
for i in range(60):
    gz.append(f'{tiangan[i % 10]}{dizhi[i % 12]}')

def julian_date_2_date(julian_date, ut=8):
    return ephem.Date(julian_date + ut / 24 - 2415020)

def date_differ(jd1, jd2):
    return math.floor(jd1 + 8 / 24 + 0.5) - math.floor(jd2 + 8 / 24 + 0.5)

def date_compare(jd1, jd2):
    return date_differ(jd1, jd2) >= 0

def find_dzs(year):
    if year == 1:
        year -= 1
    dz = ephem.next_solstice((year - 1, 12))
    jd = ephem.julian_date(dz)
    
    date1 = ephem.next_new_moon(julian_date_2_date(jd))
    jd1 = ephem.julian_date(date1)

    date2 = ephem.next_new_moon(julian_date_2_date(jd - 29))
    jd2 = ephem.julian_date(date2)

    date3 = ephem.next_new_moon(julian_date_2_date(jd - 31))
    jd3 = ephem.julian_date(date3)
    
    if date_compare(jd, jd1):
        return date1
    elif date_compare(jd, jd2):
        return date2
    elif date_compare(jd, jd3):
        return date3
        

def find_szy(jd, shuojd):
    szy = -1
    for i in range(len(shuojd)):
        if date_compare(jd, shuojd[i]):
            szy += 1
    return szy

def EquinoxSolsticeJD(year, angle):
    if 0 <= angle < 90:
        date = ephem.next_vernal_equinox(year)
    elif 90 <= angle < 180:
        date = ephem.next_summer_solstice(year)
    elif 180 <= angle < 270:
        date = ephem.next_autumn_equinox(year)
    else:
        date = ephem.next_winter_solstice(year)
    
    jd = ephem.julian_date(date)

    return jd

def lunar_calendar(nian, type=1):   # type=1时截止到次年冬至朔,=0时截止到次年冬至朔次月
	dzs = find_dzs(nian)
	shuo = dzs  # 计算用朔,date格式
	shuoJD = [ephem.julian_date(dzs)]  # 存储ut+8 JD,起冬至朔
	next_dzsJD = ephem.julian_date(find_dzs(nian + 1))  # 次年冬至朔
	i = -1  # 中气序,从0起计
	j = -1  # 计算连续两个冬至月中的合朔次数,从0起计
	zry = 0
	flag = False
	# 查找所在月及判断置闰
	while not date_compare(shuoJD[j+type], next_dzsJD):  # 从冬至月起查找,截止到次年冬至朔
		i += 1
		j += 1
		shuo = ephem.next_new_moon(shuo)  # 次月朔
		shuoJD.append(ephem.julian_date(shuo))
		# 查找本月中气,若无则置闰
		if j == 0: continue  # 冬至月一定含中气,从次月开始查找
		angle = (-90 + 30 * i) % 360  # 本月应含中气,起冬至
		qJD = solar_terms(nian, angle)
		# 不判断气在上月而后气在后月的情况,该月起的合朔次数不超过气数,可省去
		if date_compare(qJD, shuoJD[j+1]) and flag == False:  # 中气在次月,则本月无中气
				zry = j + 1  # 置闰月
				i -= 1
				flag = True  # 仅第一个无中气月置闰
	# 生成农历月序表
	ymb = []
	for k in range(len(shuoJD)):
		ymb.append(yuefen[(k - 2) % 12])  # 默认月序
		if j + type == 13:  # 仅12次合朔不闰,有闰时修改月名
			if k + 1 == zry:
				ymb[k] = '闰' + yuefen[(k-1 - 2) % 12]
			elif k + 1 > zry:
				ymb[k] = yuefen[(k-1 - 2) % 12]
	return ymb, shuoJD   # 月名表,合朔JD日期表


def solar_longitube(jd):
    date = julian_date_2_date(jd)
    s = ephem.Sun(date)
    sa = ephem.Equatorial(s.ra, s.dec, epoch=date)
    se = ephem.Ecliptic(sa)
    l = se.lon / ephem.degree / 180 * math.pi
    return l
    
def solar_terms(year, angle):
    if angle > 270:
        year -= 1
    if year == 0:
        year -= 1
    
    jd = EquinoxSolsticeJD(str(year), angle)
    
    if angle >= 270:
        jd0 = EquinoxSolsticeJD(str(year), (angle - 90) % 360)
        if jd < jd0:
            jd = EquinoxSolsticeJD(str(year + 1), angle)
    jd1 = jd
    
    while True:
        jd2 = jd1
        l = solar_longitube(jd2)
        jd1 += math.sin(angle * math.pi / 180 - l) / math.pi * 180
        if abs(jd1 - jd2) < 0.00001:
            break
    
    return jd1
    
def solar_2_lunar_calendar(date):
    
    if date[0] == '0':
        raise ValueError
    
    julian_date = ephem.julian_date(date) - 8 / 24
    year, month, day = julian_date_2_date(julian_date, 8).triple()
    
    dzs = find_dzs(year)
    next_dzs = find_dzs(year + 1)
    
    this_dzs_jd = ephem.julian_date(dzs)
    next_dzs_jd = ephem.julian_date(next_dzs)
    
    nian = year
    if date_compare(julian_date, next_dzs_jd):
        nian += 1
    if not date_compare(julian_date, this_dzs_jd):
        nian -= 1
    
    ymb, shuojd = lunar_calendar(nian)
    szy = find_szy(julian_date, shuojd)
    
    if year < 0:
        year += 1
    
    jqy, jqr = julian_date_2_date(solar_terms(year, month * 30 + 255), 8).triple()[1:]
    
    if int(jqy) != month:
        month -= (int(jqy) - month)

    if day >= int(jqr):
        ygz = gz[(year * 12 + 12 + month) % 60]
    else:
        ygz = gz[(year * 12 + 11 + month) % 60]
    
    # if szy < 3:
    #     nian -= 1
    
    if nian < 0:
        nian += 1
    
    ngz = gz[(nian - 4) % 60]
    
    rgz = gz[math.floor(julian_date + 8 / 24 + 0.5 + 49) % 60]
    
    rq = date_differ(julian_date, shuojd[szy])
    
    # print(f'{date} 为农历 {ngz}年{ygz}月{rgz}日 {ymb[szy]}{nlrq[rq]}')
    
    return ngz, ygz, rgz, ymb[szy]


def shi_gan_zhi(t, rigan):
    shi, fen = t.split(':')
    shi = int(shi)
    shi = int(shi / 2 + 0.5) % 12
    
    if rigan in ['甲', '己']:
        multipler = 0
    elif rigan in ['乙', '庚']:
        multipler = 1
    elif rigan in ['丙', '辛']:
        multipler = 2
    elif rigan in ['丁', '壬']:
        multipler = 3
    elif rigan in ['戊', '癸']:
        multipler = 4
    
    ganzhi_index = 12 * multipler + shi
    
    shiganzhi = gz[ganzhi_index]
    
    return shiganzhi

def gan_zhi(t):
    t1, t2 = t.split(' ')
    ngz, ygz, rgz, yly = solar_2_lunar_calendar(t1)
    sgz = shi_gan_zhi(t2, rgz[0])

    # print(f'{ngz}年{ygz}月{rgz}日{sgz}时 阴历{yly}')
    
    return ngz, ygz, rgz, sgz, yly