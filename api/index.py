# -*- coding: utf-8 -*-
# Author : xy_cloud
import base64
from flask import Flask, request
import ziafont
import requests
import json
import re
from IPython.display import SVG
from xml.etree import ElementTree as ET
from PIL import Image
from io import BytesIO


def get_ddnet_with_username(username: str) -> dict:
    return json.loads(requests.get(f'https://ddnet.org/players/?json2={username}').text)


class DATA_READER(object):
    def __init__(self, data):
        self.data = data

    def get_total_hours(self):
        activitys = self.data['activity']
        hoursum = 0
        for i in activitys:
            hoursum += i['hours_played']
        day = str(hoursum // 24) + ' d ' + str(hoursum % 24) + ' h'
        return day

    def get_country(self):
        return self.data['last_finishes'][0]['country']

    def get_global_rank(self):
        return str(self.data['points']['rank'])

    def get_total365(self):
        hours = self.data['hours_played_past_365_days']
        day = str(hours // 24) + ' d ' + str(hours % 24) + ' h'
        return day

    def get_total_map(self):
        map_total = 0
        types = self.data['types']
        map_played = 0
        for i in types:
            for j in types[i]['maps']:
                if types[i]['maps'][j]['finishes'] > 0:
                    map_played += 1
                map_total += 1
        return str(map_played) + ' / ' + str(map_total)

    def get_points(self):
        return (str(self.data['points']['points']) + ' / ' + str(self.data['points']['total'])), (
                    int(self.data['points']['points']) / int(self.data['points']['total'])),

    def get_ranks(self):
        types = self.data['types']
        rank1 = 0
        top10 = 0
        top100 = 0
        for i in types:
            for j in types[i]['maps']:
                if types[i]['maps'][j]['finishes'] > 0:
                    if types[i]['maps'][j]['rank'] == 1:
                        rank1 += 1
                    if types[i]['maps'][j]['rank'] <= 10:
                        top10 += 1
                    if types[i]['maps'][j]['rank'] <= 100:
                        top100 += 1
        return str(rank1), str(top10), str(top100)


def replace_file_content(file_path, mapping):
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

    pattern = re.compile(r'{{(.*?)}}')
    file_content = pattern.sub(lambda match: mapping.get(match.group(1)), file_content)

    with open('../output.svg', 'w', encoding='utf-8') as f:
        f.write(file_content)


def get_map_value(key):
    global mapping
    return mapping[key]


def render_tee(img_src):
    response = requests.get(img_src)
    image = Image.open(BytesIO(response.content))
    back_feet_shadow = image.crop((192, 64, 192 + 64, 64 + 32)).resize((64, 30))
    body_shadow = image.crop((96, 0, 96 + 96, 0 + 96)).resize((64, 64))
    front_feet_shadow = image.crop((192, 64, 192 + 64, 64 + 32)).resize((64, 30))
    back_feet = image.crop((192, 32, 192 + 64, 32 + 32)).resize((64, 30))
    body = image.crop((0, 0, 96, 96)).resize((64, 64))
    front_feet = image.crop((192, 32, 192 + 64, 32 + 32)).resize((64, 30))
    left_eye = image.crop((64, 96, 64 + 32, 96 + 32)).resize((26, 26))
    tee = Image.new(mode="RGBA", size=(96, 64), color=(0, 0, 0, 0))
    tee.paste(back_feet_shadow, (8, 32), mask=back_feet_shadow)
    tee.paste(body_shadow, (16, 0), mask=body_shadow)
    tee.paste(front_feet_shadow, (24, 32), mask=front_feet_shadow)
    tee.paste(back_feet, (8, 32), mask=back_feet)
    tee.paste(body, (16, 0), mask=body)
    tee.paste(front_feet, (24, 32), mask=front_feet)
    tee.paste(left_eye, (39, 18), mask=left_eye)
    tee = tee.transpose(Image.FLIP_LEFT_RIGHT)
    tee.paste(left_eye, (96 - 73, 18), mask=left_eye)
    tee = tee.transpose(Image.FLIP_LEFT_RIGHT)
    image_data = BytesIO()
    tee.save(image_data, format='PNG')
    image_data_bytes = image_data.getvalue()
    encoded_image = base64.b64encode(image_data_bytes).decode()
    return encoded_image


def get_reg_flag(country):
    flag = requests.get(f'https://ddnet.org/countryflags/{country}.png')
    return base64.b64encode(flag.content).decode()


def draw_pic(mode):

    if mode == 'jpg':
        return
    _ = get_map_value
    font = ziafont.Font('../fonts/Comfortaa/Comfortaa-Bold-2.ttf')
    svg = ET.Element('svg')
    svg.set('width', '570')
    svg.set('height', '285')
    svg.set('xmlns', 'http://www.w3.org/2000/svg')
    svg.set('viewBox', '0 0 570 285')
    svg.set('xmlns:xlink', 'http://www.w3.org/1999/xlink')

    style = ET.SubElement(svg, 'style')
    style.text = '''svg{
        user-select: none; !important
        }
        .profile {
        font: 'Segoe UI', Ubuntu, Sans-Serif;
        fill: #F7F7F7;
        font-weight:800;
        white-space: pre;
        }

        .status {
        font: 'Segoe UI', Ubuntu, Sans-Serif;
        fill: #F7F7F7;
        font-weight:800;
        white-space: pre;
        animation: fadeInAnimation 0.5s ease-in-out forwards;
        }

        .rank-circle-rim {
        stroke: #8C8BBA;
        fill: none;
        stroke-width: 10;
        opacity: 0.3;
        }

        .rank-circle {
        stroke: #8C8BBA;
        stroke-dasharray: 406.25;
        fill: none;
        stroke-width: 10;
        stroke-linecap: round;
        opacity: 1;
        transform-origin: -10px 8px;
        transform: rotate(-90deg);
        animation: rankAnimation 1s forwards ease-in-out;
        }

        .rank-text {
        font: 800 50px 'Segoe UI', Ubuntu, Sans-Serif; fill: #8C8BBA;
        animation: scaleInAnimation 0.3s ease-in-out forwards;
        }
        #points_line_bg{
        stroke: #8C8BBA;
        stroke-opacity: 0.34;
        stroke-width: 8;
        stroke-linecap: round;
        }

        #points_line{
        stroke: #8C8BBA;
        stroke-opacity: 1;
        stroke-width: 8;
        stroke-linecap: round;
        stroke-dasharray: 360;
        animation: barAnimation 1s forwards ease-in-out;
        }

        @keyframes barAnimation {
        from {
        stroke-dashoffset: 360;
        }
        to {
        stroke-dashoffset: ''' + str(360 - 360 * _('percent_points')) + ''';
        }
        }
        @keyframes rankAnimation {
        from {
        stroke-dashoffset: 408.4070449979;
        }
        to {
        stroke-dashoffset: ''' + str(408.4070449979 - 408.4070449979 * _('percent_rank')) + ''';
        }
        }

        @keyframes scaleInAnimation {
        from {
        transform: translate(-5px, 5px) scale(0);
        }
        to {
        transform: translate(-5px, 5px) scale(1);
        }
        }

        @keyframes fadeInAnimation {
        from {
        transform: translateY(5px);
        opacity: 0;
        }
        to {
        transform: translateY(0px);
        opacity: 1;
        }
        }'''

    defs = ET.SubElement(svg, 'defs')

    pattern0 = ET.SubElement(defs, 'pattern')
    pattern0.set('id', 'pattern0')
    pattern0.set('patternContentUnits', 'objectBoundingBox')
    pattern0.set('width', '1')
    pattern0.set('height', '1')

    pattern0_use = ET.SubElement(pattern0, 'use')
    pattern0_use.set('xlink:href', '#image0')
    pattern0_use.set('transform', 'translate(-0.25) scale(0.015625)')

    pattern0_img = ET.SubElement(defs, 'image')
    pattern0_img.set('id', 'image0')
    pattern0_img.set('data-name', 'image.png')
    pattern0_img.set('width', '96')
    pattern0_img.set('height', '64')
    pattern0_img.set('xlink:href', f'data:image/png;base64,{render_tee(_("skin_url"))}')

    pattern1 = ET.SubElement(defs, 'pattern')
    pattern1.set('id', 'pattern1')
    pattern1.set('patternContentUnits', 'objectBoundingBox')
    pattern1.set('width', '1')
    pattern1.set('height', '1')

    pattern1_use = ET.SubElement(pattern1, 'use')
    pattern1_use.set('xlink:href', '#image1')
    pattern1_use.set('transform', 'matrix(0.0078125 0 0 0.0158617 0 -0.00757576)')

    pattern1_img = ET.SubElement(defs, 'image')
    pattern1_img.set('id', 'image1')
    pattern1_img.set('data-name', 'image.png')
    pattern1_img.set('width', '128')
    pattern1_img.set('height', '64')
    pattern1_img.set('xlink:href', f'data:image/png;base64,{get_reg_flag(_("country"))}')

    bg_rect = ET.SubElement(svg, 'rect')
    bg_rect.set('id', 'bg_rect')
    bg_rect.set('width', '570')
    bg_rect.set('height', "285")
    bg_rect.set('rx', '11')
    bg_rect.set('fill', '#434343')

    tee = ET.SubElement(svg, 'rect')
    tee.set('id', 'tee')
    tee.set('x', '18')
    tee.set('y', '50')
    tee.set('width', '83')
    tee.set('height', '83')
    tee.set('fill', 'url(#pattern0)')

    username = ET.SubElement(svg, 'text')
    username.set('id', 'username')
    username.set('class', 'profile')
    username.set('xml:space', 'preserve')
    username.set('font-size', '22')
    username_tspan = ET.SubElement(username, 'tspan')
    username_tspan.set('x', '123')
    username_tspan.set('y', '73.2273')
    username_tspan.text = _("username")

    team = ET.SubElement(svg, 'text')
    team.set('id', 'team')
    team.set('class', 'profile')
    team.set('xml:space', 'preserve')
    team.set('font-size', '24')
    team_tspan = ET.SubElement(team, 'tspan')
    team_tspan.set('x', '123')
    team_tspan.set('y', '114.227')
    team_tspan.text = _("team")

    flag = ET.SubElement(svg, 'rect')
    flag.set('id', 'flag')
    flag.set('x', '268')
    flag.set('y', '48')
    flag.set('width', '67')
    flag.set('height', '33')
    flag.set('fill', 'url(#pattern1)')

    country = ET.SubElement(svg, 'text')
    country.set('id', 'country')
    country.set('class', 'profile')
    country.set('xml:space', 'preserve')
    country.set('font-size', '24')
    country_tspan = ET.SubElement(country, 'tspan')
    country_tspan.set('x', '335')
    country_tspan.set('y', '73.2273')
    country_tspan.text = _("country")

    global_rank = ET.SubElement(svg, 'text')
    global_rank.set('id', 'global_rank')
    global_rank.set('class', 'status')
    global_rank.set('xml:space', 'preserve')
    global_rank.set('style', 'white-space: pre')
    global_rank.set('font-size', '16')
    global_rank_tspan = ET.SubElement(global_rank, 'tspan')
    global_rank_tspan.set('x', '18')
    global_rank_tspan.set('y', '201.318')
    global_rank_tspan.text = "Global Rank"

    global_rank_num = ET.SubElement(svg, 'text')
    global_rank_num.set('id', 'global_rank_num')
    global_rank_num.set('class', 'status')
    global_rank_num.set('xml:space', 'preserve')
    global_rank_num.set('style', 'white-space: pre')
    global_rank_num.set('font-size', '40')
    global_rank_num_tspan = ET.SubElement(global_rank_num, 'tspan')
    global_rank_num_tspan.set('x', '18')
    global_rank_num_tspan.set('y', '244.545')
    global_rank_num_tspan.text = '#' + _("Global Rank")

    total_play_time = ET.SubElement(svg, 'text')
    total_play_time.set('id', 'total_play_time')
    total_play_time.set('class', 'status')
    total_play_time.set('xml:space', 'preserve')
    total_play_time.set('style', 'white-space: pre')
    total_play_time.set('font-size', '8')
    total_play_time_tspan = ET.SubElement(total_play_time, 'tspan')
    total_play_time_tspan.set('x', '192')
    total_play_time_tspan.set('y', '195.636')
    total_play_time_tspan.text = "Total Play Time (past 365 days)"

    total_play_time_num = ET.SubElement(svg, 'text')
    total_play_time_num.set('id', 'total_play_time_num')
    total_play_time_num.set('class', 'status')
    total_play_time_num.set('xml:space', 'preserve')
    total_play_time_num.set('style', 'white-space: pre')
    total_play_time_num.set('font-size', '20')
    total_play_time_num_tspan = ET.SubElement(total_play_time_num, 'tspan')
    total_play_time_num_tspan.set('x', '192')
    total_play_time_num_tspan.set('y', '220.273')
    total_play_time_num_tspan.text = _("Total365")

    total_play_map = ET.SubElement(svg, 'text')
    total_play_map.set('id', 'total_play_map')
    total_play_map.set('class', 'status')
    total_play_map.set('xml:space', 'preserve')
    total_play_map.set('style', 'white-space: pre')
    total_play_map.set('font-size', '12')
    total_play_map_tspan = ET.SubElement(total_play_map, 'tspan')
    total_play_map_tspan.set('x', '192')
    total_play_map_tspan.set('y', '243.636')
    total_play_map_tspan.text = "Total Play Map"

    total_play_map_num = ET.SubElement(svg, 'text')
    total_play_map_num.set('id', 'total_play_map_num')
    total_play_map_num.set('class', 'status')
    total_play_map_num.set('xml:space', 'preserve')
    total_play_map_num.set('style', 'white-space: pre')
    total_play_map_num.set('font-size', '20')
    total_play_map_num_tspan = ET.SubElement(total_play_map_num, 'tspan')
    total_play_map_num_tspan.set('x', '192')
    total_play_map_num_tspan.set('y', '268.273')
    total_play_map_num_tspan.text = _("Total Map")

    rank_circle_group = ET.SubElement(svg, 'g')
    rank_circle_group.set('data-testid', 'rank-circle')
    rank_circle_group.set('transform', 'translate(490.5, 87.5)')

    rank_circle_rim = ET.SubElement(rank_circle_group, 'circle')
    rank_circle_rim.set('class', 'rank-circle-rim')
    rank_circle_rim.set('cx', '-10')
    rank_circle_rim.set('cy', '8')
    rank_circle_rim.set('r', '65')

    rank_circle = ET.SubElement(rank_circle_group, 'circle')
    rank_circle.set('class', 'rank-circle')
    rank_circle.set('cx', '-10')
    rank_circle.set('cy', '8')
    rank_circle.set('r', '65')

    rank_text_group = ET.SubElement(rank_circle_group, 'g')
    rank_text_group.set('class', 'rank-text')

    rank_text = ET.SubElement(rank_text_group, 'text')
    rank_text.set('x', '-5')
    rank_text.set('y', '-2')
    rank_text.set('alignment-baseline', 'central')
    rank_text.set('dominant-baseline', 'central')
    rank_text.set('text-anchor', 'middle')
    rank_text.set('data-testid', 'level-rank-text')
    rank_text.text = str(_('rank(circle)'))

    title = ET.SubElement(svg, 'text')
    title.set('id', 'title')
    title.set('fill', '#6D86DD')
    title.set('xml:space', 'preserve')
    title.set('style', 'white-space: pre')
    title.set('font-size', '20')
    title.set('font-weight', '900')
    title_span = ET.SubElement(title, 'tspan')
    title_span.set('x', '23')
    title_span.set('y', '25.2727')
    title_span.text = f'{_("username")}\'s DDNet Stats'

    points_line_bg = ET.SubElement(svg, 'line')
    points_line_bg.set('id', 'points_line_bg')
    points_line_bg.set('x1', '21')
    points_line_bg.set('y1', '166')
    points_line_bg.set('x2', '381')
    points_line_bg.set('y2', '166')

    points_line = ET.SubElement(svg, 'line')
    points_line.set('id', 'points_line')
    points_line.set('x1', '21')
    points_line.set('y1', '166')
    points_line.set('x2', '381')
    points_line.set('y2', '166')

    points = ET.SubElement(svg, 'text')
    points.set('id', 'points')
    points.set('fill', '#8C8BBA')
    points.set('xml:space', 'preserve')
    points.set('style', 'white-space: pre')
    points.set('font-size', '16')

    points_span = ET.SubElement(points, 'tspan')
    points_span.set('x', '18')
    points_span.set('y', '154.318')
    points_span.text = "points"

    points_num = ET.SubElement(svg, 'text')
    points_num.set('id', 'points_num')
    points_num.set('fill', '#8C8BBA')
    points_num.set('xml:space', 'preserve')
    points_num.set('style', 'white-space: pre')
    points_num.set('font-size', '16')
    points_num.set('text-anchor', "end")

    points_num_span = ET.SubElement(points_num, 'tspan')
    points_num_span.set('x', '383.578')
    points_num_span.set('y', '158.318')
    points_num_span.text = _("points")

    little_card = ET.SubElement(svg, 'g')
    little_card.set('id', 'little_card')
    little_card.set('class', 'status')

    mask1 = ET.SubElement(little_card, 'mask')
    mask1.set('id', 'path-21-inside-1_22_2')
    mask1.set('fill', 'white')
    path11 = ET.SubElement(mask1, 'path')
    path11.set('d',
               "M359 185C359 182.239 361.239 180 364 180H448.662C451.424 180 453.662 182.239 453.662 185V219C453.662 221.761 451.424 224 448.662 224H364C361.239 224 359 221.761 359 219V185Z")

    path12 = ET.SubElement(little_card, 'path')
    path12.set('d',
               "M359 185C359 182.239 361.239 180 364 180H448.662C451.424 180 453.662 182.239 453.662 185V219C453.662 221.761 451.424 224 448.662 224H364C361.239 224 359 221.761 359 219V185Z")
    path12.set('fill', '#F7F7F7')
    path12.set('fill-opacity', '0.1')

    path13 = ET.SubElement(little_card, 'path')
    path13.set('d',
               "M359 185C359 180.029 363.029 176 368 176H444.662C449.633 176 453.662 180.029 453.662 185C453.662 184.448 451.424 184 448.662 184H364C361.239 184 359 184.448 359 185ZM453.662 224H359H453.662ZM359 224V180V224ZM453.662 180V224V180Z")
    path13.set('fill', '#8C8BBA')
    path13.set('mask', 'url(#path-21-inside-1_22_2)')

    rank1 = ET.SubElement(little_card, 'text')
    rank1.set('id', 'rank1')
    rank1.set('fill', '#F7F7F7')
    rank1.set('xml:space', 'preserve')
    rank1.set('style', 'white-space: pre')
    rank1.set('font-size', '14')

    rank1_tspan = ET.SubElement(rank1, 'tspan')
    rank1_tspan.set('x', '366.675')
    rank1_tspan.set('y', '198.591')
    rank1_tspan.text = '#1 Ranks'

    rank1_num = ET.SubElement(little_card, 'text')
    rank1_num.set('id', 'rank1_num')
    rank1_num.set('fill', '#F7F7F7')
    rank1_num.set('xml:space', 'preserve')
    rank1_num.set('style', 'white-space: pre')
    rank1_num.set('font-size', '14')

    rank1_num_tspan = ET.SubElement(rank1_num, 'tspan')
    rank1_num_tspan.set('x', '366.675')
    rank1_num_tspan.set('y', '218.591')
    rank1_num_tspan.text = _('rank1')

    mask2 = ET.SubElement(little_card, 'mask')
    mask2.set('id', 'path-25-inside-2_22_2')
    mask2.set('fill', 'white')
    path21 = ET.SubElement(mask2, 'path')
    path21.set('d',
               "M461.338 234C461.338 231.239 463.576 229 466.338 229H551C553.761 229 556 231.239 556 234V268C556 270.761 553.761 273 551 273H466.338C463.576 273 461.338 270.761 461.338 268V234Z")

    path22 = ET.SubElement(little_card, 'path')
    path22.set('d',
               "M461.338 234C461.338 231.239 463.576 229 466.338 229H551C553.761 229 556 231.239 556 234V268C556 270.761 553.761 273 551 273H466.338C463.576 273 461.338 270.761 461.338 268V234Z")
    path22.set('fill', '#F7F7F7')
    path22.set('fill-opacity', '0.1')

    path23 = ET.SubElement(little_card, 'path')
    path23.set('d',
               "M461.338 234C461.338 229.029 465.367 225 470.338 225H547C551.971 225 556 229.029 556 234C556 233.448 553.761 233 551 233H466.338C463.576 233 461.338 233.448 461.338 234ZM556 273H461.338H556ZM461.338 273V229V273ZM556 229V273V229Z")
    path23.set('fill', '#8C8BBA')
    path23.set('mask', 'url(#path-25-inside-2_22_2)')

    top100 = ET.SubElement(little_card, 'text')
    top100.set('id', 'top100')
    top100.set('fill', '#F7F7F7')
    top100.set('xml:space', 'preserve')
    top100.set('style', 'white-space: pre')
    top100.set('font-size', '14')

    top100_tspan = ET.SubElement(top100, 'tspan')
    top100_tspan.set('x', '469.013')
    top100_tspan.set('y', '247.591')
    top100_tspan.text = 'Top 100'

    top100_num = ET.SubElement(little_card, 'text')
    top100_num.set('id', 'top100_num')
    top100_num.set('fill', '#F7F7F7')
    top100_num.set('xml:space', 'preserve')
    top100_num.set('style', 'white-space: pre')
    top100_num.set('font-size', '14')

    top100_num_tspan = ET.SubElement(top100_num, 'tspan')
    top100_num_tspan.set('x', '469')
    top100_num_tspan.set('y', '267.591')
    top100_num_tspan.text = _('top100')

    mask3 = ET.SubElement(little_card, 'mask')
    mask3.set('id', 'path-29-inside-3_22_2')
    mask3.set('fill', 'white')
    path31 = ET.SubElement(mask3, 'path')
    path31.set('d',
               "M359 234C359 231.239 361.239 229 364 229H448.662C451.424 229 453.662 231.239 453.662 234V268C453.662 270.761 451.424 273 448.662 273H364C361.239 273 359 270.761 359 268V234Z")

    path32 = ET.SubElement(little_card, 'path')
    path32.set('d',
               "M359 234C359 231.239 361.239 229 364 229H448.662C451.424 229 453.662 231.239 453.662 234V268C453.662 270.761 451.424 273 448.662 273H364C361.239 273 359 270.761 359 268V234Z")
    path32.set('fill', '#F7F7F7')
    path32.set('fill-opacity', '0.1')

    path33 = ET.SubElement(little_card, 'path')
    path33.set('d',
               "M359 234C359 229.029 363.029 225 368 225H444.662C449.633 225 453.662 229.029 453.662 234C453.662 233.448 451.424 233 448.662 233H364C361.239 233 359 233.448 359 234ZM453.662 273H359H453.662ZM359 273V229V273ZM453.662 229V273V229Z")
    path33.set('fill', '#8C8BBA')
    path33.set('mask', 'url(#path-29-inside-3_22_2)')

    top10 = ET.SubElement(little_card, 'text')
    top10.set('id', 'top10')
    top10.set('fill', '#F7F7F7')
    top10.set('xml:space', 'preserve')
    top10.set('style', 'white-space: pre')
    top10.set('font-size', '14')

    top10_tspan = ET.SubElement(top10, 'tspan')
    top10_tspan.set('x', '366.675')
    top10_tspan.set('y', '247.591')
    top10_tspan.text = 'Top 10'

    top10_num = ET.SubElement(little_card, 'text')
    top10_num.set('id', 'top10_num')
    top10_num.set('fill', '#F7F7F7')
    top10_num.set('xml:space', 'preserve')
    top10_num.set('style', 'white-space: pre')
    top10_num.set('font-size', '14')

    top10_num_tspan = ET.SubElement(top10_num, 'tspan')
    top10_num_tspan.set('x', '367')
    top10_num_tspan.set('y', '267.591')
    top10_num_tspan.text = _('top10')

    mask4 = ET.SubElement(little_card, 'mask')
    mask4.set('id', 'path-33-inside-4_22_2')
    mask4.set('fill', 'white')
    path41 = ET.SubElement(mask4, 'path')
    path41.set('d',
               "M461.338 185C461.338 182.239 463.576 180 466.338 180H551C553.761 180 556 182.239 556 185V219C556 221.761 553.761 224 551 224H466.338C463.576 224 461.338 221.761 461.338 219V185Z")

    path42 = ET.SubElement(little_card, 'path')
    path42.set('d',
               "M461.338 185C461.338 182.239 463.576 180 466.338 180H551C553.761 180 556 182.239 556 185V219C556 221.761 553.761 224 551 224H466.338C463.576 224 461.338 221.761 461.338 219V185Z")
    path42.set('fill', '#F7F7F7')
    path42.set('fill-opacity', '0.1')

    path43 = ET.SubElement(little_card, 'path')
    path43.set('d',
               "M461.338 185C461.338 180.029 465.367 176 470.338 176H547C551.971 176 556 180.029 556 185C556 184.448 553.761 184 551 184H466.338C463.576 184 461.338 184.448 461.338 185ZM556 224H461.338H556ZM461.338 224V180V224ZM556 180V224V180Z")
    path43.set('fill', '#8C8BBA')
    path43.set('mask', 'url(#path-33-inside-4_22_2)')

    total_time = ET.SubElement(little_card, 'text')
    total_time.set('id', 'total_time')
    total_time.set('fill', '#F7F7F7')
    total_time.set('xml:space', 'preserve')
    total_time.set('style', 'white-space: pre')
    total_time.set('font-size', '10')

    total_time_tspan = ET.SubElement(total_time, 'tspan')
    total_time_tspan.set('x', '469.013')
    total_time_tspan.set('y', '196.636')
    total_time_tspan.text = 'Total Play Time'

    total_time_num = ET.SubElement(little_card, 'text')
    total_time_num.set('id', 'total_time_num')
    total_time_num.set('fill', '#F7F7F7')
    total_time_num.set('xml:space', 'preserve')
    total_time_num.set('style', 'white-space: pre')
    total_time_num.set('font-size', '14')

    total_time_num_tspan = ET.SubElement(total_time_num, 'tspan')
    total_time_num_tspan.set('x', '469')
    total_time_num_tspan.set('y', '218.591')
    total_time_num_tspan.text = _('total_time')
    if mode == 'svg text to path(only english username)':
        font.text(f'{_("username")}\'s DDNet Stats', size=20, color='#6D86DD').drawon(svg, 23, 25.2727)

        # with open('../output.svg', 'w', encoding='utf-8') as f:
        #     f.write(SVG(ET.tostring(svg)).data)
    elif mode == 'svg':
        # with open('../output.svg', 'wb') as f:
        #     f.write(ET.tostring(svg, encoding='utf-8'))
        return ET.tostring(svg, encoding='utf-8')


app = Flask(__name__)


@app.route("/svg", methods=["GET"])
def getsvg():
    global mapping
    username = request.args.get("username")
    team = request.args.get("team")
    if username == None:
        username = 'nameless tee'
    if team == None:
        team = ''
    print(username, team)
    dr = DATA_READER(get_ddnet_with_username(username))
    # 映射表
    pt = dr.get_points()
    rk = dr.get_ranks()
    mapping = {
        'username': username,
        'team': team,
        'skin_url': 'https://ddnet.org/skins/skin/community/AmethystCat.png',
        'country': dr.get_country(),
        'Global Rank': dr.get_global_rank(),
        'Total365': dr.get_total365(),
        'Total Map': dr.get_total_map(),
        'rank(circle)': 'A+',
        'points': pt[0],
        'rank1': rk[0],
        'top10': rk[1],
        'top100': rk[2],
        'total_time': dr.get_total_hours(),
        'percent_points': pt[1],
        'percent_rank': 0.5
    }
    return draw_pic('svg')


app.run(host='0.0.0.0', port=8080)
