# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
import RoundUp
from RoundUp import round_up


# 机型比选
class auto_word_wind_turbines_compare(models.Model):
    # _inherit = 'auto_word.wind'
    _name = 'auto_word_wind_turbines.compare'
    _description = 'turbines_compare'
    _rec_name = 'case_name'
    _inherit = ['wind_turbines.case']

    project_id = fields.Many2one('auto_word.project', string=u'项目名', required=True)
    content_id = fields.Many2one('auto_word.wind', string=u'章节分类')
    # , required=True, readonly=True)
    # domain=lambda self: [('project_id.project_name', '=', self.project_id.project_name)]

    res_form = fields.Many2one('auto_word_wind_res.form', string=u'上传电量', required=False)
    # --------方案参数---------
    WTG_name = fields.Char(u'风机代号', default="WTG1", required=False)
    case_name = fields.Char(u'方案名称')
    ongrid_power = fields.Char(u'上网电量', readonly=False)
    hours_year = fields.Char(u'满发小时', readonly=False)
    weak = fields.Char(u'尾流衰减', readonly=True)
    hub_height_suggestion = fields.Char(string=u'推荐轮毂高度')

    TerrainType = fields.Char(string=u'山地类型')

    # --------电气参数---------
    jidian_air_wind = fields.Char(u'架空长度', default="待提交", readonly=True)
    jidian_cable_wind = fields.Char(u'电缆长度', default="待提交", readonly=True)

    # --------风电参数---------
    case_ids = fields.Many2many('wind_turbines.case', string=u'方案机型')
    cal_id = fields.Selection([(0, u"线性"), (1, u"非线性")], string=u"采用算法")

    turbine_numbers = fields.Char(string=u'风机数量', readonly=True, default="0")
    farm_capacity = fields.Char(string=u'装机容量', readonly=True)

    name_tur_words = fields.Char(string=u'风机型号', readonly=True, default="待提交")
    capacity_words = fields.Char(string=u'风机容量', readonly=True, default="待提交")
    tower_weight_words = fields.Char(string=u'塔筒重量', readonly=True, default="待提交")
    rotor_diameter_words = fields.Char(string=u'叶轮直径',readonly=True, default="待提交")
    rotor_swept_area_words = fields.Char(string=u'扫风面积',readonly=True, default="待提交")
    blade_number_words = fields.Char(string=u'叶片数',readonly=True, default="待提交")

    cut_in_wind_speed_words = fields.Float(u'切入风速', readonly=False)
    cut_out_wind_speed_words = fields.Float(u'切出风速', readonly=False)
    rated_wind_speed_words = fields.Float(u'额定风速', readonly=False)
    three_second_maximum_words = fields.Char(u'生存风速', readonly=False)
    rated_power_words = fields.Float(u'额定功率', readonly=False)
    voltage_words = fields.Float(u'额定电压', readonly=False)

    # --------经评参数---------
    investment_E1 = fields.Float(string=u'塔筒投资(万元)')
    investment_E2 = fields.Float(string=u'风机设备投资(万元)')
    investment_E3 = fields.Float(string=u'基础投资(万元)', required=False, )
    investment_E4 = fields.Float(string=u'道路投资(万元)')
    investment_E5 = fields.Float(string=u'吊装费用(万元)', readonly=True, )
    investment_E6 = fields.Float(string=u'箱变投资(万元)', readonly=True, )
    investment_E7 = fields.Float(string=u'集电线路(万元)', readonly=True, )
    investment_turbines_kw_words = fields.Char(u'风机kw投资', readonly=True)
    investment = fields.Float(string=u'发电部分投资(万元)', readonly=True, )
    investment_unit = fields.Float(string=u'单位度电投资', readonly=True, )


    @api.onchange('project_id')
    def onchange_project_id(self):
        self.content_id = self.content_id.search([('project_id.project_name', '=',
                                                   self.project_id.project_name)])

    def cal_compare_result(self):
        self.case_name = self.res_form.case_name

        investment_e1_sum, investment_e2_sum, investment_e3_sum = 0, 0, 0
        investment_e5_sum, investment_e6_sum = 0, 0
        for re in self:
            tower_weight_word, tower_weight_words = '', ''
            rotor_diameter_word, rotor_diameter_words = '', ''
            investment_turbines_kw_word, investment_turbines_kw_words = '', ''
            case_hub_height_word, case_hub_height_words, capacity_words = '', '', ''
            name_tur_words, investment_e5 = '', 0
            re.turbine_numbers = 0
            re.farm_capacity = 0
            for i in range(0, len(re.case_ids)):

                rotor_swept_area_word = str(re.case_ids[i].rotor_swept_area)
                blade_number_word = str(re.case_ids[i].blade_number)
                cut_in_wind_speed_word = str(re.case_ids[i].cut_in_wind_speed)
                cut_out_wind_speed_word = str(re.case_ids[i].cut_out_wind_speed)
                rated_wind_speed_word = str(re.case_ids[i].rated_wind_speed)
                three_second_maximum_word = str(re.case_ids[i].three_second_maximum)
                rated_power_word = str(re.case_ids[i].rated_power)
                voltage_word = str(re.case_ids[i].voltage)

                tower_weight_word = str(re.case_ids[i].tower_weight)
                rotor_diameter_word = str(re.case_ids[i].rotor_diameter)
                investment_turbines_kw_word = str(re.case_ids[i].investment_turbines_kw)
                capacity_word = str(re.case_ids[i].capacity)
                name_tur_word = str(re.case_ids[i].name_tur)

                re.turbine_numbers = int(re.case_ids[i].turbine_numbers) + int(re.turbine_numbers)
                print(re.case_ids[i].capacity)
                re.farm_capacity = int(re.case_ids[i].turbine_numbers) * float(re.case_ids[i].capacity) + float(
                    re.farm_capacity)

                investment_e1 = RoundUp.round_up(
                    re.case_ids[i].tower_weight * re.case_ids[i].turbine_numbers * 1.05 * int(
                        re.hub_height_suggestion) / 90)
                investment_e1_sum = investment_e1_sum + investment_e1

                investment_e2 = int(re.case_ids[i].turbine_numbers) * int(re.case_ids[i].capacity) * int(
                    re.case_ids[i].investment_turbines_kw) / 10000
                investment_e2_sum = investment_e2_sum + investment_e2

                investment_e3 = float(re.env['auto_word.civil'].search([('project_id.project_name', '=',
                                                                         re.project_id.project_name)]).EarthExcavation_WindResource) * 9 + \
                                float(re.env['auto_word.civil'].search([('project_id.project_name', '=',
                                                                         re.project_id.project_name)]).StoneExcavation_WindResource) * 45 + \
                                float(re.env['auto_word.civil'].search([('project_id.project_name', '=',
                                                                         re.project_id.project_name)]).EarthWorkBackFill_WindResource) * 8 + \
                                float(re.env['auto_word.civil'].search([('project_id.project_name', '=',
                                                                         re.project_id.project_name)]).Cushion) * 580 + \
                                float(re.env['auto_word.civil'].search([('project_id.project_name', '=',
                                                                         re.project_id.project_name)]).Volume) * 650 + \
                                float(re.env['auto_word.civil'].search([('project_id.project_name', '=',
                                                                         re.project_id.project_name)]).Reinforcement) * 6000 + \
                                float(re.env['auto_word.civil'].search([('project_id.project_name', '=',
                                                                         re.project_id.project_name)]).stake_number) * int(
                    re.case_ids[i].turbine_numbers) * 15000
                investment_e3 = investment_e3 / 10000
                investment_e3_sum = investment_e3_sum + investment_e3
                if re.cal_id == 0:
                    if int(re.hub_height_suggestion) <= 90:
                        investment_e5 = re.case_ids[i].turbine_numbers * 38
                    elif 90 < int(re.hub_height_suggestion) <= 100:
                        investment_e5 = re.case_ids[i].turbine_numbers * 43
                    elif 100 < int(re.hub_height_suggestion) <= 120:
                        investment_e5 = re.case_ids[i].turbine_numbers * 55
                    elif 120 < int(re.hub_height_suggestion) <= 140:
                        investment_e5 = re.case_ids[i].turbine_numbers * 65
                elif re.cal_id == 1:
                    if int(re.hub_height_suggestion) <= 90:
                        investment_e5 = re.case_ids[i].turbine_numbers * 38 * 1.01 - 2.5
                    elif 90 < int(re.hub_height_suggestion) <= 100:
                        investment_e5 = re.case_ids[i].turbine_numbers * 45 * 1.01
                    elif 100 < int(re.hub_height_suggestion) <= 120:
                        investment_e5 = re.case_ids[i].turbine_numbers * 55 * 1.15
                    elif 120 < int(re.hub_height_suggestion) <= 140:
                        investment_e5 = re.case_ids[i].turbine_numbers * 65 * 1.2

                if re.case_ids[i].capacity <= 2000:
                    investment_e6 = re.case_ids[i].turbine_numbers * 23
                elif 2000 < re.case_ids[i].capacity <= 2200:
                    investment_e6 = re.case_ids[i].turbine_numbers * 25
                elif 2200 < re.case_ids[i].capacity <= 2500:
                    investment_e6 = re.case_ids[i].turbine_numbers * 28
                elif 2500 < re.case_ids[i].capacity <= 4000:
                    investment_e6 = re.case_ids[i].turbine_numbers * 32

                investment_e5_sum = investment_e5_sum + investment_e5
                investment_e6_sum = investment_e6_sum + investment_e6
                if len(re.case_ids) > 1:
                    if i != len(re.case_ids) - 1:
                        tower_weight_words = tower_weight_word + "/" + tower_weight_words
                        rotor_diameter_words = rotor_diameter_word + "/" + rotor_diameter_words
                        investment_turbines_kw_words = investment_turbines_kw_word + "/" + investment_turbines_kw_words
                        name_tur_words = name_tur_word + "/" + name_tur_words
                        capacity_words = capacity_word + "/" + capacity_words

                        rotor_swept_area_word = rotor_swept_area_word + "/" + rotor_swept_area_word
                        blade_number_word = blade_number_word + "/" + blade_number_word

                        cut_in_wind_speed_word = cut_in_wind_speed_word + "/" + cut_in_wind_speed_word
                        cut_out_wind_speed_word = cut_out_wind_speed_word + "/" + cut_out_wind_speed_word
                        rated_wind_speed_word = rated_wind_speed_word + "/" + rated_wind_speed_word
                        three_second_maximum_word = three_second_maximum_word + "/" + three_second_maximum_word
                        rated_power_word = rated_power_word + "/" + rated_power_word
                        voltage_word = voltage_word + "/" + voltage_word

                    else:
                        tower_weight_words = tower_weight_words + tower_weight_word
                        rotor_diameter_words = rotor_diameter_words + rotor_diameter_word
                        investment_turbines_kw_words = investment_turbines_kw_words + investment_turbines_kw_word
                        name_tur_words = name_tur_words + name_tur_word
                        capacity_words = capacity_words + capacity_word

                        rotor_swept_area_words = rotor_swept_area_words + rotor_swept_area_word
                        blade_number_words = blade_number_words + blade_number_word

                        cut_in_wind_speed_words = cut_in_wind_speed_word + cut_in_wind_speed_words
                        cut_out_wind_speed_words = cut_out_wind_speed_word + cut_out_wind_speed_words
                        rated_wind_speed_words = rated_wind_speed_word + rated_wind_speed_words
                        three_second_maximum_words = three_second_maximum_word + three_second_maximum_words
                        rated_power_words = rated_power_word + rated_power_words
                        voltage_words = voltage_word + voltage_words

                if len(re.case_ids) == 1:
                    tower_weight_words = tower_weight_word
                    rotor_diameter_words = rotor_diameter_word
                    investment_turbines_kw_words = investment_turbines_kw_word
                    capacity_words = capacity_word
                    name_tur_words = name_tur_word
                    rotor_swept_area_words = rotor_swept_area_word
                    blade_number_words = blade_number_word

                    cut_in_wind_speed_words = cut_in_wind_speed_word
                    cut_out_wind_speed_words = cut_out_wind_speed_word
                    rated_wind_speed_words = rated_wind_speed_word
                    three_second_maximum_words = three_second_maximum_word
                    rated_power_words = rated_power_word
                    voltage_words = voltage_word

            re.name_tur_words = name_tur_words
            re.capacity_words = capacity_words
            re.tower_weight_words = tower_weight_words
            re.rotor_diameter_words = rotor_diameter_words
            re.rotor_swept_area_words = rotor_swept_area_words
            re.blade_number_words = blade_number_words

            re.cut_in_wind_speed_words = cut_in_wind_speed_words
            re.cut_out_wind_speed_words = cut_out_wind_speed_words
            re.rated_wind_speed_words = rated_wind_speed_words
            re.three_second_maximum_words = three_second_maximum_words
            re.rated_power_words = rated_power_words
            re.voltage_words = voltage_words

            re.investment_turbines_kw_words = investment_turbines_kw_words

            re.farm_capacity = round_up(float(re.farm_capacity) / 1000, 2)
            re.investment_E1 = investment_e1_sum
            re.investment_E2 = investment_e2_sum
            re.investment_E3 = investment_e3_sum

            if re.content_id.TerrainType == "平原":
                re.TerrainType = '平原'
            elif re.content_id.TerrainType == "丘陵":
                re.TerrainType = '丘陵'
            else:
                re.TerrainType = '山地'

            if re.project_id.total_civil_length == "待提交":
                re.project_id.total_civil_length = 0

            if re.investment_E4 == 0:
                if re.TerrainType == "平原":
                    re.investment_E4 = float(re.project_id.total_civil_length) * 50
                elif re.TerrainType == "丘陵":
                    re.investment_E4 = float(re.project_id.total_civil_length) * 80
                elif re.TerrainType == "山地":
                    re.investment_E4 = float(re.project_id.total_civil_length) * 140
            else:
                pass

            re.investment_E5 = investment_e5_sum
            re.investment_E6 = investment_e6_sum

            if re.project_id.jidian_air_wind == "待提交":
                re.project_id.jidian_air_wind = 0

            if re.project_id.jidian_cable_wind == "待提交":
                re.project_id.jidian_cable_wind = 0

            if re.jidian_air_wind == "待提交" and re.jidian_cable_wind == "待提交":
                re.jidian_air_wind = re.project_id.jidian_air_wind
                re.jidian_cable_wind = re.project_id.jidian_cable_wind

                re.investment_E7 = float(re.jidian_air_wind) * 40 + float(
                    re.jidian_cable_wind) * 50
            else:
                re.investment_E7 = float(re.jidian_air_wind) * 40 + float(re.jidian_cable_wind) * 50

            re.investment = RoundUp.round_up(re.investment_E1 + re.investment_E2 + re.investment_E3 + re.investment_E4 + \
                                             re.investment_E5 + re.investment_E6 + re.investment_E7)

            if re.ongrid_power != 0:
                re.investment_unit = RoundUp.round_up3(
                    (re.investment / float(re.ongrid_power) * 10), 3)
            re.ongrid_power = re.res_form.ongrid_power_sum
            re.hours_year = re.res_form.hours_year_average
            re.weak = re.res_form.wake_average
            re.hub_height_suggestion = re.res_form.hub_height_calcuation

    def submit_turbines_compare(self):
        for re in self:
            re.content_id.rotor_diameter_case = re.rotor_diameter_words
            re.env['auto_word.wind'].search([('project_id.project_name', '=',
                                              re.project_id.project_name)]).recommend_id = re
            re.content_id.tower_weight = re.tower_weight

    def result_refresh(self):
        for re in self:
            re.jidian_air_wind = re.project_id.jidian_air_wind
            re.jidian_cable_wind = re.project_id.jidian_cable_wind
            re.investment_E4 = re.project_id.investment_E4

            re.ongrid_power = re.res_form.ongrid_power_sum
            re.hours_year = re.res_form.hours_year_average
            re.weak = re.res_form.wake_average
            re.hub_height_suggestion = re.res_form.hub_height_calcuation
