#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2020/12/12 23:11
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2020 yuangezhizao <root@yuangezhizao.cn>
"""
import datetime
import re
import time

import requests
from lxml import etree

from maimai_DX_CN_probe.models.maimai import HOME, PlayerData, album, Record, playlogDetail


def save_home(raw_html):
    selector = etree.HTML(raw_html)

    basic_img = selector.xpath('/html/body/div[2]/div[2]/div[1]/img/@src')[0]
    trophy = selector.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[1]/div/span/text()')[0]
    name = selector.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/text()')[0]
    rating = selector.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div/text()')[0]
    rating_max = selector.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/text()')[0][4:]
    rating_img = selector.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/img/@src')[0]
    grade_img = selector.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/img[2]/@src')[0]
    star = selector.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[4]/text()')[0][1:]
    chara = selector.xpath('/html/body/div[2]/div[2]/img/@src')[0]
    comment = selector.xpath('/html/body/div[2]/div[2]/div[2]/text()')[0]
    cache_dt = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    new_maimai_HOME = HOME(basic_img, trophy, name, rating, rating_max, rating_img, grade_img, star, chara, comment,
                           cache_dt)
    r = new_maimai_HOME.save()
    return r


def save_playerData(raw_html):
    selector = etree.HTML(raw_html)

    music_count = selector.xpath('/html/body/div[2]/div[2]/div[3]/text()')[0].split('：')[1]
    total_count = selector.xpath('/html/body/div[2]/div[2]/div[4]/div[2]/text()')[0].split('/')[1].replace(',', '')

    sssp = selector.xpath('/html/body/div[2]/div[2]/div[4]/div[2]/text()')[0].split('/')[0]
    sss = selector.xpath('/html/body/div[2]/div[2]/div[7]/div[2]/text()')[0].split('/')[0]
    ssp = selector.xpath('/html/body/div[2]/div[2]/div[10]/div[2]/text()')[0].split('/')[0]
    ss = selector.xpath('/html/body/div[2]/div[2]/div[13]/div[2]/text()')[0].split('/')[0]
    sp = selector.xpath('/html/body/div[2]/div[2]/div[16]/div[2]/text()')[0].split('/')[0]
    s = selector.xpath('/html/body/div[2]/div[2]/div[19]/div[2]/text()')[0].split('/')[0]
    clear = selector.xpath('/html/body/div[2]/div[2]/div[22]/div[2]/text()')[0].split('/')[0]

    app = selector.xpath('/html/body/div[2]/div[2]/div[5]/div[2]/text()')[0].split('/')[0]
    ap = selector.xpath('/html/body/div[2]/div[2]/div[8]/div[2]/text()')[0].split('/')[0]
    fcp = selector.xpath('/html/body/div[2]/div[2]/div[11]/div[2]/text()')[0].split('/')[0]
    fc = selector.xpath('/html/body/div[2]/div[2]/div[14]/div[2]/text()')[0].split('/')[0]
    fsdp = selector.xpath('/html/body/div[2]/div[2]/div[17]/div[2]/text()')[0].split('/')[0]
    fsd = selector.xpath('/html/body/div[2]/div[2]/div[20]/div[2]/text()')[0].split('/')[0]
    fsp = selector.xpath('/html/body/div[2]/div[2]/div[23]/div[2]/text()')[0].split('/')[0]
    fs = selector.xpath('/html/body/div[2]/div[2]/div[25]/div[2]/text()')[0].split('/')[0]

    cache_dt = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    new_maimai_PlayerData = PlayerData(music_count, total_count, sssp, sss, ssp, ss, sp, s, clear, app, ap, fcp, fc,
                                       fsdp, fsd, fsp, fs,
                                       cache_dt)
    r = new_maimai_PlayerData.save()
    return r


def save_playerData_album(raw_html):
    selector = etree.HTML(raw_html)

    new_count = 0
    album_count = len(selector.xpath('.//div[@class=" m_10 p_5 f_0"]'))

    for i in range(album_count + 1, 1, -1):
        dx_img_s = selector.xpath(f'/html/body/div[2]/div[{i}]/div/img[1]/@src')[0].split('/')[-1].split('.')[0]
        play_dt = selector.xpath(f'/html/body/div[2]/div[{i}]/div/div[1]/text()')[0]
        play_dt_utc = datetime.datetime.strptime(play_dt, '%Y/%m/%d %H:%M') - datetime.timedelta(hours=8)
        level_img_s = selector.xpath(f'/html/body/div[2]/div[{i}]/div/img[2]/@src')[0].split('/')[-1].split('.')[0]
        name = selector.xpath(f'/html/body/div[2]/div[{i}]/div/div[3]/text()')[0]
        img = selector.xpath(f'/html/body/div[2]/div[{i}]/div/img[3]/@src')[0].split('/')[-1]
        cache_dt = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        if not album.query.filter(album.play_dt == play_dt).first():
            new_maimai_album = album(dx_img_s, play_dt, play_dt_utc, level_img_s, name, img, cache_dt)
            new_maimai_album.save()
            new_count += 1

    return [new_count, album_count]


def save_record(raw_html):
    selector = etree.HTML(raw_html)

    new_count = 0
    record_count = len(selector.xpath('//div[@class="p_10 t_l f_0 v_b"]'))

    for i in range(record_count + 1, 1, -1):
        level_img_s = selector.xpath(f'/html/body/div[2]/div[{i}]/div[1]/img/@src')[0].split('/')[-1].split('.')[0]
        try:
            vs_img_s = selector.xpath(f'/html/body/div[2]/div[{i}]/div[1]/img[3]/@src')[0] \
                .split('/')[-1].split('.')[0]
        except Exception as e:
            vs_img_s = None

        track = selector.xpath(f'/html/body/div[2]/div[{i}]/div[1]/div[1]/span[1]/text()')[0].split(' ')[1]
        play_dt = selector.xpath(f'/html/body/div[2]/div[{i}]/div[1]/div[1]/span[2]/text()')[0]

        play_dt_utc = datetime.datetime.strptime(play_dt, '%Y/%m/%d %H:%M') - datetime.timedelta(hours=8)
        # play_ts_utc = int(time.mktime(play_dt_utc.timetuple()))

        try:
            selector.xpath(f'/html/body/div[2]/div[{i}]/div[2]/div[1]/img/@src')[0].split('/')[-1].split('.')[0]
            clear = True
        except Exception as e:
            clear = False
        name = selector.xpath(f'/html/body/div[2]/div[{i}]/div[2]/div[1]/text()')[0]
        img_s = selector.xpath(f'/html/body/div[2]/div[{i}]/div[2]/div[2]/img[1]/@src')[0]
        dx_img_s = selector.xpath(f'/html/body/div[2]/div[{i}]/div[2]/div[2]/img[2]/@src')[0] \
            .split('/')[-1].split('.')[0]
        achievement_0 = selector.xpath(f'/html/body/div[2]/div[{i}]/div[2]/div[2]/div/div[2]/text()')[0]
        achievement_1 = selector.xpath(f'/html/body/div[2]/div[{i}]/div[2]/div[2]/div/div[2]/span/text()')[0]
        achievement = int(achievement_0) + float(f'0{achievement_1}'[:-1])
        try:
            selector.xpath(f'/html/body/div[2]/div[{i}]/div[2]/div[2]/div/img[3]/@src')[0]
            score_rank_new = True
            score_rank_img_s = selector.xpath(f'/html/body/div[2]/div[{i}]/div[2]/div[2]/div/img[2]/@src')[0] \
                .split('/')[-1].split('.')[0]
        except Exception as e:
            score_rank_new = False
            score_rank_img_s = selector.xpath(f'/html/body/div[2]/div[{i}]/div[2]/div[2]/div/img[1]/@src')[0] \
                .split('/')[-1].split('.')[0]
        delux_score = selector.xpath(f'/html/body/div[2]/div[{i}]/div[2]/div[2]/div/div[3]/div[1]/div/text()')[0] \
            .split('/')[-1].split('.')[0].replace(',', '')
        try:
            selector.xpath(f'/html/body/div[2]/div[{i}]/div[2]/div[2]/div/div[3]/div[1]/img[2]/@src')[0]
            delux_new = True
        except Exception as e:
            delux_new = False
        fc_img_s = selector.xpath(f'/html/body/div[2]/div[{i}]/div[2]/div[2]/div/div[3]/img[1]/@src')[0] \
            .split('/')[-1].split('.')[0]
        fs_img_s = selector.xpath(f'/html/body/div[2]/div[{i}]/div[2]/div[2]/div/div[3]/img[2]/@src')[0] \
            .split('/')[-1].split('.')[0]
        try:
            rate_img_s = selector.xpath(f'/html/body/div[2]/div[{i}]/div[2]/div[2]/div/div[3]/img[3]/@src')[0] \
                .split('/')[-1].split('.')[0]
        except Exception as e:
            rate_img_s = None
        cache_dt = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        if not Record.query.filter(Record.play_dt == play_dt).first():
            new_maimai_Record = Record(level_img_s, vs_img_s, track, play_dt, play_dt_utc, clear, name, img_s, dx_img_s,
                                       achievement,
                                       score_rank_new, score_rank_img_s, delux_score, delux_new, fc_img_s, fs_img_s,
                                       rate_img_s, cache_dt)
            new_maimai_Record.save()
            new_count += 1

    return [new_count, record_count]


def save_record_playlogDetail(userId, _t, start_posi, end_posi):
    session = requests.Session()
    # 下方手动指定并不会更新 cookies，因此不可多次使用
    # cookies = requests.utils.cookiejar_from_dict(cookies)
    # session.cookies = cookies

    if end_posi <= start_posi:
        idx = list(range(start_posi, 50))
        idx.extend(list(range(0, end_posi)))
    else:
        idx = range(start_posi, end_posi)

    for i in idx:
        url = f'https://maimai.wahlap.com/maimai-mobile/record/playlogDetail/?idx={i}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        }
        cookies = {
            'userId': userId,
            '_t': _t
        }

        if i == idx[0]:
            r = session.get(url, headers=headers, cookies=cookies, verify=False)
        else:
            # 之后 session 库自行处理 cookies
            r = session.get(url, headers=headers, verify=False)
        r_text = r.text
        status_code = r.status_code
        if status_code != 200:
            return f'ERROR [{i}]：status_code != 200'
        if '错误码' in r_text:
            error_code = re.findall('错误码：(.*?)</div>', r_text, re.S)[0]
            return f'ERROR [{i}]：error_code {error_code}'
        parse_record_playlogDetail(r_text)
        time.sleep(1)
    print(session.cookies.get_dict())
    return idx


def parse_record_playlogDetail(raw_html):
    selector = etree.HTML(raw_html)

    vsUser = len(selector.xpath('//div[@class="see_through_block m_10 m_t_0  p_l_10 t_l f_0 break"]'))
    if vsUser:
        vs_rank = selector.xpath('/html/body/div[2]/div[3]/span/div[1]/text()')[0]
        vs_achievement = selector.xpath('/html/body/div[2]/div[3]/span/div[1]/span/text()')[0][:-1]
        vs_rating = selector.xpath('/html/body/div[2]/div[3]/span/div[2]/span/text()')[0]
        vs_grade = selector.xpath('/html/body/div[2]/div[3]/span/img[2]/@src')[0].split('/')[-1].split('.')[0]

        # [【爬虫】使用xpath与lxml移除特定标签](https://blog.csdn.net/aqua75836/article/details/101355869)
        for bad in selector.xpath("/html/body/div[2]/div[3]"):
            bad.getparent().remove(bad)
    else:
        vs_rank = None
        vs_achievement = None
        vs_rating = None
        vs_grade = None
    try:
        chara_0_img_s = selector.xpath('/html/body/div[2]/div[3]/div[2]/div[1]/div/img/@src')[0] \
            .split('/')[-1].split('.')[0]
        chara_0_star = selector.xpath('/html/body/div[2]/div[3]/div[2]/div[2]/text()')[0][1:]
        chara_0_lv = selector.xpath('/html/body/div[2]/div[3]/div[2]/div[3]/text()')[0][2:]
    except Exception as e:
        chara_0_img_s = ''
        chara_0_star = 0
        chara_0_lv = 0
    try:
        chara_1_img_s = selector.xpath('/html/body/div[2]/div[3]/div[3]/div[1]/div/img/@src')[0] \
            .split('/')[-1].split('.')[0]
        chara_1_star = selector.xpath('/html/body/div[2]/div[3]/div[3]/div[2]/text()')[0][1:]
        chara_1_lv = selector.xpath('/html/body/div[2]/div[3]/div[3]/div[3]/text()')[0][2:]
    except Exception as e:
        chara_1_img_s = ''
        chara_1_star = 0
        chara_1_lv = 0
    try:
        chara_2_img_s = selector.xpath('/html/body/div[2]/div[3]/div[4]/div[1]/div/img/@src')[0] \
            .split('/')[-1].split('.')[0]
        chara_2_star = selector.xpath('/html/body/div[2]/div[3]/div[4]/div[2]/text()')[0][1:]
        chara_2_lv = selector.xpath('/html/body/div[2]/div[3]/div[4]/div[3]/text()')[0][2:]
    except Exception as e:
        chara_2_img_s = ''
        chara_2_star = 0
        chara_2_lv = 0
    try:
        chara_3_img_s = selector.xpath('/html/body/div[2]/div[3]/div[5]/div[1]/div/img/@src')[0] \
            .split('/')[-1].split('.')[0]
        chara_3_star = selector.xpath('/html/body/div[2]/div[3]/div[5]/div[2]/text()')[0][1:]
        chara_3_lv = selector.xpath('/html/body/div[2]/div[3]/div[5]/div[3]/text()')[0][2:]
    except Exception as e:
        chara_3_img_s = ''
        chara_3_star = 0
        chara_3_lv = 0
    try:
        chara_4_img_s = selector.xpath('/html/body/div[2]/div[3]/div[6]/div[1]/div/img/@src')[0] \
            .split('/')[-1].split('.')[0]
        chara_4_star = selector.xpath('/html/body/div[2]/div[3]/div[6]/div[2]/text()')[0][1:]
        chara_4_lv = selector.xpath('/html/body/div[2]/div[3]/div[6]/div[3]/text()')[0][2:]
    except Exception as e:
        chara_4_img_s = ''
        chara_4_star = 0
        chara_4_lv = 0

    try:
        fast = selector.xpath('/html/body/div[2]/div[3]/div[7]/div[1]/div/text()')[0]
    except Exception as e:
        print('【ERROR】fast')
        fast = 0
        print(e)

    try:
        late = selector.xpath('/html/body/div[2]/div[3]/div[7]/div[2]/div/text()')[0]
    except Exception as e:
        print('【ERROR】late')
        late = 0
        print(e)

    # grade = selector.xpath('/html/body/div[2]/div[3]/div[9]/div[1]/table/tbody/tr[1]/td[2]/div/text()')[0]
    # [xpath解析网页中tbody问题](https://web.archive.org/web/20200621034512/https://blog.csdn.net/qq_32590631/article/details/76064127)，移除 tbody

    grade = selector.xpath('/html/body/div[2]/div[3]/div[9]/div[1]/table/tr[1]/td[2]/div/text()')[0]
    # grade = selector.xpath('//div[@class="playlog_rating_val_block"]/text()')[0]

    grade_diff = selector.xpath('/html/body/div[2]/div[3]/div[9]/div[1]/table/tr[1]/td[2]/span/text()')[0]
    # grade_diff = selector.xpath('//span[@class="f_11"]/text()')[0]

    rating = selector.xpath('/html/body/div[2]/div[3]/div[9]/div[1]/table/tr[2]/td[2]/div/text()')[0]
    # rating = selector.xpath('//div[@class="playlog_rating_val_block"]/text()')[1]

    try:
        delux_rating = selector.xpath('/html/body/div[2]/div[3]/div[9]/div[1]/div[1]/span/text()')[0]
    except Exception as e:
        print('【ERROR】delux_rating')
        delux_rating = 0
        print(e)
    try:
        delux_rating_diff = selector.xpath('/html/body/div[2]/div[3]/div[9]/div[1]/div[1]/img[2]/@src')[0] \
            .split('/')[-1].split('.')[0]
    except Exception as e:
        print('【ERROR】delux_rating_diff')
        delux_rating_diff = ''
        print(e)
    try:
        grade_pic_s = selector.xpath('/html/body/div[2]/div[3]/div[9]/div[1]/div[2]/img/@src')[0] \
            .split('/')[-1].split('.')[0]
    except Exception as e:
        print('【ERROR】grade_pic_s')
        grade_pic_s = ''
        print(e)

    empty_calu = lambda count: count[0] if count else None

    notes_tap_cp = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[2]/td[1]/text()')
    notes_tap_cp = empty_calu(notes_tap_cp)

    notes_tap_p = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[2]/td[2]/text()')
    notes_tap_p = empty_calu(notes_tap_p)

    notes_tap_great = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[2]/td[3]/text()')
    notes_tap_great = empty_calu(notes_tap_great)

    notes_tap_good = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[2]/td[4]/text()')
    notes_tap_good = empty_calu(notes_tap_good)

    notes_tap_miss = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[2]/td[5]/text()')
    notes_tap_miss = empty_calu(notes_tap_miss)

    notes_hold_cp = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[3]/td[1]/text()')
    notes_hold_cp = empty_calu(notes_hold_cp)
    if notes_hold_cp == '\u3000':
        notes_hold_cp = None

    notes_hold_p = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[3]/td[2]/text()')
    notes_hold_p = empty_calu(notes_hold_p)

    notes_hold_great = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[3]/td[3]/text()')
    notes_hold_great = empty_calu(notes_hold_great)

    notes_hold_good = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[3]/td[4]/text()')
    notes_hold_good = empty_calu(notes_hold_good)

    notes_hold_miss = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[3]/td[5]/text()')
    notes_hold_miss = empty_calu(notes_hold_miss)

    notes_slide_cp = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[4]/td[1]/text()')
    notes_slide_cp = empty_calu(notes_slide_cp)

    notes_slide_p = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[4]/td[2]/text()')
    notes_slide_p = empty_calu(notes_slide_p)

    notes_slide_great = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[4]/td[3]/text()')
    notes_slide_great = empty_calu(notes_slide_great)

    notes_slide_good = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[4]/td[4]/text()')
    notes_slide_good = empty_calu(notes_slide_good)

    notes_slide_miss = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[4]/td[5]/text()')
    notes_slide_miss = empty_calu(notes_slide_miss)

    notes_touch_cp = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[5]/td[1]/text()')
    notes_touch_cp = empty_calu(notes_touch_cp)
    if notes_touch_cp == '\u3000':
        notes_touch_cp = None

    notes_touch_p = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[5]/td[2]/text()')
    notes_touch_p = empty_calu(notes_touch_p)

    notes_touch_great = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[5]/td[3]/text()')
    notes_touch_great = empty_calu(notes_touch_great)

    notes_touch_good = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[5]/td[4]/text()')
    notes_touch_good = empty_calu(notes_touch_good)

    notes_touch_miss = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[5]/td[5]/text()')
    notes_touch_miss = empty_calu(notes_touch_miss)

    notes_break_cp = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[6]/td[1]/text()')
    notes_break_cp = empty_calu(notes_break_cp)

    notes_break_p = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[6]/td[2]/text()')
    notes_break_p = empty_calu(notes_break_p)

    notes_break_great = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[6]/td[3]/text()')
    notes_break_great = empty_calu(notes_break_great)

    notes_break_good = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[6]/td[4]/text()')
    notes_break_good = empty_calu(notes_break_good)

    notes_break_miss = selector.xpath('/html/body/div[2]/div[3]/div[9]/table/tr[6]/td[5]/text()')
    notes_break_miss = empty_calu(notes_break_miss)

    try:
        maxcombo = selector.xpath('/html/body/div[2]/div[3]/div[9]/div[3]/div/div/text()')[0]
    except Exception as e:
        print('【ERROR】maxcombo')
        maxcombo = 0
        print(e)
    try:
        maxsync = selector.xpath('/html/body/div[2]/div[3]/div[9]/div[4]/div/div/text()')[0]
    except Exception as e:
        print('【ERROR】maxsync')
        maxsync = 0
        print(e)
    try:
        level_img_s = selector.xpath('//*[@id="matching"]/span[1]/img[1]/@src')[0].split('/')[-1].split('.')[0]
        name = selector.xpath('//*[@id="matching"]/span[1]/div/text()')[0]
    except Exception as e:
        # 单人模式
        level_img_s = None
        name = None
    cache_dt = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    new_maimai_playlogDetail = playlogDetail(vs_rank, vs_achievement, vs_rating, vs_grade, chara_0_img_s, chara_0_star,
                                             chara_0_lv,
                                             chara_1_img_s, chara_1_star, chara_1_lv, chara_2_img_s,
                                             chara_2_star, chara_2_lv, chara_3_img_s, chara_3_star, chara_3_lv,
                                             chara_4_img_s, chara_4_star,
                                             chara_4_lv, fast, late, grade, grade_diff, rating, delux_rating,
                                             delux_rating_diff, grade_pic_s,
                                             notes_tap_cp, notes_tap_p, notes_tap_great, notes_tap_good, notes_tap_miss,
                                             notes_hold_cp,
                                             notes_hold_p, notes_hold_great, notes_hold_good, notes_hold_miss,
                                             notes_slide_cp,
                                             notes_slide_p, notes_slide_great, notes_slide_good, notes_slide_miss,
                                             notes_touch_cp, notes_touch_p,
                                             notes_touch_great, notes_touch_good, notes_touch_miss, notes_break_cp,
                                             notes_break_p,
                                             notes_break_great, notes_break_good, notes_break_miss, maxcombo, maxsync,
                                             level_img_s, name, cache_dt)
    new_maimai_playlogDetail.save()
