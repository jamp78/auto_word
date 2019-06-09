# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
import RoundUp


# 机型比选
class auto_word_wind_res(models.Model):
    # _inherit = 'auto_word.wind'
    _name = 'auto_word_wind.res'
    _description = 'turbines_res'
    _rec_name = 'tur_id'

    project_id_input = fields.Char(u'项目名')
    case_name = fields.Char(u'方案名称(结果)')

    # project_id = fields.Many2one('auto_word.project', string=u'项目名', required=True)
    # content_ids = fields.Many2one('auto_word.wind', string=u'章节分类', required=True)

    Turbine = fields.Char(u'风机')
    tur_id = fields.Char(string=u'风机ID', readonly=False)
    X = fields.Char(string=u'X', readonly=False)
    Y = fields.Char(string=u'Y', readonly=False)
    Z = fields.Char(string=u'Z', readonly=False)
    H = fields.Char(string=u'计算高度', readonly=False)
    Latitude = fields.Char(string=u'经度', readonly=False)
    Longitude = fields.Char(string=u'纬度', readonly=False)
    TrustCoefficient = fields.Char(string=u'信任系数', readonly=False)
    WeibullA = fields.Char(string=u'A', readonly=False)
    WeibullK = fields.Char(string=u'K', readonly=False)
    EnergyDensity = fields.Char(string=u'能量密度', readonly=False)
    PowerGeneration = fields.Char(string=u'理论电量', readonly=False)
    PowerGeneration_Weak = fields.Char(string=u'尾流后理论电量', readonly=False)
    CapacityCoe = fields.Char(string=u'CapacityCoe', readonly=False)
    AverageWindSpeed = fields.Char(string=u'平均风速', readonly=False)
    TurbulenceEnv_StrongWind = fields.Char(string=u'强风状态下平均环境湍流强度', readonly=False)
    Turbulence_StrongWind = fields.Char(string=u'强风状态下的平均总体湍流强度', readonly=False)
    AverageWindSpeed_Weak = fields.Char(string=u'考虑尾流效应的平均风速', readonly=False)
    Weak = fields.Char(string=u'尾流效应导致的平均折减率', readonly=False)
    AirDensity = fields.Char(string=u'该点的空气密度', readonly=False)
    WindShear_Avg = fields.Char(string=u'平均风切变指数', readonly=False)
    WindShear_Max = fields.Char(string=u'最大风切变指数', readonly=False)
    WindShear_Max_Deg = fields.Char(string=u'最大风切变指数对应方向扇区', readonly=False)
    InflowAngle_Avg = fields.Char(string=u'绝对值平均入流角', readonly=False)
    InflowAngle_Max = fields.Char(string=u'最大入流角', readonly=False)
    InflowAngle_Max_Deg = fields.Char(string=u'出现最大入流角的风向扇区', readonly=False)
    NextTur = fields.Char(string=u'最近相邻风机的标签', readonly=False)
    NextLength_M = fields.Char(string=u'相邻风机的最近距离', readonly=False)
    Diameter = fields.Char(string=u'叶轮直径', readonly=False)
    NextLength_D = fields.Char(string=u'以叶轮直径为单位的相邻风机最近距离', readonly=False)
    NextDeg = fields.Char(string=u'最近相邻风机的方位角', readonly=False)
    Sectors = fields.Char(string=u'扇区数量', readonly=False)

    turbine_capacity_each = fields.Float(string=u'风机容量', readonly=False)
    #
    # @api.depends('case_ids', 'TerrainType_turbines_compare', 'cal_id')
    # def _compute_turbine(self):
    #
    #     investment_e1_sum, investment_e2_sum = 0, 0
    #     investment_e5_sum, investment_e6_sum = 0, 0
    #     for re in self:
    #         tower_weight_word, tower_weight_words = '', ''
    #         rotor_diameter_word, rotor_diameter_words = '', ''
    #         investment_turbines_kw_word, investment_turbines_kw_words = '', ''
    #         case_hub_height_word, case_hub_height_words, capacity_words = '', '', ''
    #         name_tur_words, investment_e5 = '', 0
    #         re.case_number = str(len(re.case_ids))
    #         for i in range(0, len(re.case_ids)):
    #
    #             tower_weight_word = str(re.case_ids[i].tower_weight)
    #             rotor_diameter_word = str(re.case_ids[i].rotor_diameter)
    #             investment_turbines_kw_word = str(re.case_ids[i].investment_turbines_kw)
    #             capacity_word = str(re.case_ids[i].capacity)
    #             name_tur_word = str(re.case_ids[i].name_tur)
    #
    #             re.turbine_numbers = int(re.case_ids[i].turbine_numbers) + int(re.turbine_numbers)
    #             re.farm_capacity = int(re.case_ids[i].turbine_numbers) * int(re.case_ids[i].capacity) + int(
    #                 re.farm_capacity)
    #             investment_e1 = RoundUp.round_up(
    #                 re.case_ids[i].tower_weight * re.case_ids[i].turbine_numbers * 1.05 * int(
    #                     re.hub_height_suggestion) / 90)
    #             investment_e1_sum = investment_e1_sum + investment_e1
    #
    #             investment_e2 = int(re.case_ids[i].turbine_numbers) * int(re.case_ids[i].capacity) * int(
    #                 re.case_ids[i].investment_turbines_kw) / 10000
    #             investment_e2_sum = investment_e2_sum + investment_e2
    #
    #             if re.cal_id == 0:
    #                 if int(re.hub_height_suggestion) <= 90:
    #                     investment_e5 = re.case_ids[i].turbine_numbers * 38
    #                 elif 90 < int(re.hub_height_suggestion) <= 100:
    #                     investment_e5 = re.case_ids[i].turbine_numbers * 43
    #                 elif 100 < int(re.hub_height_suggestion) <= 120:
    #                     investment_e5 = re.case_ids[i].turbine_numbers * 55
    #                 elif 120 < int(re.hub_height_suggestion) <= 140:
    #                     investment_e5 = re.case_ids[i].turbine_numbers * 65
    #             elif re.cal_id == 1:
    #                 if int(re.hub_height_suggestion) <= 90:
    #                     investment_e5 = re.case_ids[i].turbine_numbers * 38 * 1.01 - 2.5
    #                 elif 90 < int(re.hub_height_suggestion) <= 100:
    #                     investment_e5 = re.case_ids[i].turbine_numbers * 45 * 1.01
    #                 elif 100 < int(re.hub_height_suggestion) <= 120:
    #                     investment_e5 = re.case_ids[i].turbine_numbers * 55 * 1.15
    #                 elif 120 < int(re.hub_height_suggestion) <= 140:
    #                     investment_e5 = re.case_ids[i].turbine_numbers * 65 * 1.2
    #
    #             if re.case_ids[i].capacity <= 2000:
    #                 investment_e6 = re.case_ids[i].turbine_numbers * 23
    #             elif 2000 < re.case_ids[i].capacity <= 2200:
    #                 investment_e6 = re.case_ids[i].turbine_numbers * 25
    #             elif 2200 < re.case_ids[i].capacity <= 2500:
    #                 investment_e6 = re.case_ids[i].turbine_numbers * 28
    #             elif 2500 < re.case_ids[i].capacity <= 4000:
    #                 investment_e6 = re.case_ids[i].turbine_numbers * 32
    #
    #             investment_e5_sum = investment_e5_sum + investment_e5
    #             investment_e6_sum = investment_e6_sum + investment_e6
    #             if len(re.case_ids) > 1:
    #                 if i != len(re.case_ids) - 1:
    #                     tower_weight_words = tower_weight_word + "/" + tower_weight_words
    #                     rotor_diameter_words = rotor_diameter_word + "/" + rotor_diameter_words
    #                     investment_turbines_kw_words = investment_turbines_kw_word + "/" + investment_turbines_kw_words
    #                     name_tur_words = name_tur_word + "/" + name_tur_words
    #                     capacity_words = capacity_word + "/" + capacity_words
    #
    #                 else:
    #                     tower_weight_words = tower_weight_words + tower_weight_word
    #                     rotor_diameter_words = rotor_diameter_words + rotor_diameter_word
    #                     investment_turbines_kw_words = investment_turbines_kw_words + investment_turbines_kw_word
    #                     name_tur_words = name_tur_words + name_tur_word
    #                     capacity_words = capacity_words + capacity_word
    #
    #             if len(re.case_ids) == 1:
    #                 tower_weight_words = tower_weight_word
    #                 rotor_diameter_words = rotor_diameter_word
    #                 investment_turbines_kw_words = investment_turbines_kw_word
    #                 capacity_words = capacity_word
    #                 name_tur_words = name_tur_word
    #
    #         re.name_tur = name_tur_words
    #         re.capacity = capacity_words
    #         re.tower_weight = tower_weight_words
    #         re.rotor_diameter_case = rotor_diameter_words
    #         re.investment_turbines_kws = investment_turbines_kw_words
    #
    #         re.farm_capacity = int(re.farm_capacity) / 1000
    #         re.investment_E1 = investment_e1_sum
    #         re.investment_E2 = investment_e2_sum
    #
    #         if re.investment_E4 == 0:
    #             if re.TerrainType_turbines_compare == "平原":
    #                 re.investment_E4 = float(re.project_id.total_civil_length) * 50
    #             elif re.TerrainType_turbines_compare == "丘陵":
    #                 re.investment_E4 = float(re.project_id.total_civil_length) * 80
    #             elif re.TerrainType_turbines_compare == "山地":
    #                 re.investment_E4 = float(re.project_id.total_civil_length) * 140
    #         else:
    #             pass
    #
    #         re.investment_E5 = investment_e5_sum
    #         re.investment_E6 = investment_e6_sum
    #
    #         if re.jidian_air_wind == 0 and re.jidian_cable_wind == 0:
    #             re.investment_E7 = float(re.project_id.jidian_air_wind) * 40 + float(
    #                 re.project_id.jidian_cable_wind) * 50
    #         else:
    #             re.investment_E7 = float(re.jidian_air_wind) * 40 + float(re.jidian_cable_wind) * 50
    #
    #         re.investment = RoundUp.round_up(re.investment_E1 + re.investment_E2 + re.investment_E3 + re.investment_E4 + \
    #                                          re.investment_E5 + re.investment_E6 + re.investment_E7)
    #
    #         re.investment_unit = RoundUp.round_up3((re.investment / re.power_generation * 10), 3)
    #
    # def wind_turbines_compare_form_refresh(self):
    #     for re in self:
    #         re.content_ids.rotor_diameter_case = re.rotor_diameter_case
    #         re.content_ids.case_number = re.case_number
    #
    # def take_result_refresh(self):
    #     for re in self:
    #         re.jidian_air_wind = re.project_id.jidian_air_wind
    #         re.jidian_cable_wind = re.project_id.jidian_cable_wind
    #         re.investment_E4 = re.project_id.investment_E4


class auto_word_wind_res_form(models.Model):
    _name = 'auto_word_wind_res.form'
    _description = 'auto_word_wind_res_form'
    _rec_name = 'project_id'
    _inherit = ['auto_word_wind.res']
    project_id = fields.Many2one('auto_word.project', string=u'项目名', required=False)
    content_ids = fields.Many2one('auto_word.wind', string=u'章节分类', required=False)
    auto_word_wind_res = fields.Many2many('auto_word_wind.res', string=u'机位结果', required=True)

    ongrid_power = fields.Float(string=u'上网电量', readonly=False)
    rate = fields.Float(string=u'折减率', readonly=False)


    @api.multi
    def wind_res_submit(self):
        for re in self.auto_word_wind_res:
            ongrid_power = float(re.PowerGeneration_Weak) * self.rate/re.turbine_capacity_each*1000
            print(re.tur_id)
            print(ongrid_power)
