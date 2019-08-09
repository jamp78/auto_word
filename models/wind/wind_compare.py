# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
import RoundUp


# 机型比选
class auto_word_wind_turbines_compare(models.Model):
    # _inherit = 'auto_word.wind'
    _name = 'auto_word_wind_turbines.compare'
    _description = 'turbines_compare'
    _rec_name = 'case_name'

    project_id = fields.Many2one('auto_word.project', string=u'项目名', required=True)
    content_id = fields.Many2one('auto_word.wind', string=u'章节分类', required=True)
    res_form = fields.Many2one('auto_word_wind_res.form', string=u'上传电量', required=False)

    WTG_name = fields.Char(u'风机代号', default="WTG1", required=False)
    case_name = fields.Char(u'方案名称', readonly=True, compute='_compute_ongrid_power')
    ongrid_power = fields.Char(u'上网电量(结果)', readonly=True, compute='_compute_ongrid_power')
    hours_year = fields.Char(u'年发电小时数(结果)', readonly=True, compute='_compute_ongrid_power')
    weak = fields.Char(u'尾流衰减(结果)', readonly=True, compute='_compute_ongrid_power')

    # case_name = fields.Char(u'方案名称', readonly=True)
    # ongrid_power = fields.Char(u'上网电量(结果)', readonly=True)
    # hours_year = fields.Char(u'年发电小时数(结果)', readonly=True)
    # weak = fields.Char(u'尾流衰减(结果)', readonly=True)

    TerrainType_turbines_compare = fields.Selection(
        [("平原", u"平原"), ("丘陵", u"丘陵"), ("山地", u"山地")], string=u"山地类型", required=True, default="山地")
    jidian_air_wind = fields.Float(u'架空长度', default=0, help='若不填写即采用电气集电线路')
    jidian_cable_wind = fields.Float(u'电缆长度', default=0, help='若不填写即采用电气集电线路')

    case_ids = fields.Many2many('wind_turbines.case', string=u'方案机型')
    cal_id = fields.Selection([(0, u"线性"), (1, u"非线性")], string=u"采用算法")

    turbine_numbers = fields.Char(string=u'风机数量', readonly=True, compute='_compute_turbine', default="待提交")
    name_tur = fields.Char(string=u'风机类型', readonly=True, compute='_compute_turbine', default="待提交")
    capacity = fields.Char(string=u'风机容量', readonly=True, compute='_compute_turbine', default="待提交")
    farm_capacity = fields.Char(string=u'装机容量', readonly=True, compute='_compute_turbine', default="待提交")
    tower_weight = fields.Char(compute='_compute_turbine', string=u'塔筒重量', default="待提交")
    rotor_diameter_case = fields.Char(compute='_compute_turbine', string=u'叶轮直径', default="待提交")
    case_number = fields.Char(compute='_compute_turbine', string=u'方案数')
    hub_height_suggestion = fields.Char(string=u'推荐轮毂高度', compute='_compute_ongrid_power')

    investment_E1 = fields.Float(compute='_compute_turbine', string=u'塔筒投资(万元)')
    investment_E2 = fields.Float(compute='_compute_turbine', string=u'风机设备投资(万元)')
    investment_E3 = fields.Float(string=u'基础投资(万元)', required=False, default=3240)
    investment_E4 = fields.Float(string=u'道路投资(万元)')
    investment_E5 = fields.Float(string=u'吊装费用(万元)', readonly=True, compute='_compute_turbine')
    investment_E6 = fields.Float(string=u'箱变投资(万元)', readonly=True, compute='_compute_turbine')
    investment_E7 = fields.Float(string=u'集电线路(万元)', readonly=True, compute='_compute_turbine')
    investment_turbines_kws = fields.Char(u'风机kw投资', compute='_compute_turbine')
    investment = fields.Float(string=u'发电部分投资(万元)', readonly=True, compute='_compute_turbine')
    investment_unit = fields.Float(string=u'单位度电投资', readonly=True, compute='_compute_turbine')


    @api.depends('res_form')
    def _compute_ongrid_power(self):
        for re in self:
            re.case_name = re.res_form.case_name
            re.ongrid_power = re.res_form.ongrid_power_sum
            re.hours_year = re.res_form.hours_year_average
            re.weak = re.res_form.wake_average
            re.hub_height_suggestion = re.res_form.hub_height_calcuation
    @api.depends('case_ids', 'TerrainType_turbines_compare', 'cal_id','res_form')
    def _compute_turbine(self):

        investment_e1_sum, investment_e2_sum = 0, 0
        investment_e5_sum, investment_e6_sum = 0, 0
        for re in self:
            tower_weight_word, tower_weight_words = '', ''
            rotor_diameter_word, rotor_diameter_words = '', ''
            investment_turbines_kw_word, investment_turbines_kw_words = '', ''
            case_hub_height_word, case_hub_height_words, capacity_words = '', '', ''
            name_tur_words, investment_e5 = '', 0
            re.case_number = str(len(re.case_ids))
            for i in range(0, len(re.case_ids)):

                tower_weight_word = str(re.case_ids[i].tower_weight)
                rotor_diameter_word = str(re.case_ids[i].rotor_diameter)
                investment_turbines_kw_word = str(re.case_ids[i].investment_turbines_kw)
                capacity_word = str(re.case_ids[i].capacity)
                name_tur_word = str(re.case_ids[i].name_tur)

                re.turbine_numbers = int(re.case_ids[i].turbine_numbers) + int(re.turbine_numbers)
                re.farm_capacity = int(re.case_ids[i].turbine_numbers) * int(re.case_ids[i].capacity) + int(
                    re.farm_capacity)

                print("sadasdadad000000000000000000000000")
                print(re.case_ids[i].tower_weight)
                print(re.case_ids[i].turbine_numbers)
                # print(re.hub_height_suggestion)
                # if re.hub_height_suggestion == False:
                #     re.hub_height_suggestion = re.env['auto_word_wind_res.form'].search([('case_name', '=',
                #                                                                  re.res_form.case_name)])[
                #         i].hub_height_calcuation
                # print(re.hub_height_suggestion)

                investment_e1 = RoundUp.round_up(
                    re.case_ids[i].tower_weight * re.case_ids[i].turbine_numbers * 1.05 * int(
                        re.hub_height_suggestion) / 90)
                investment_e1_sum = investment_e1_sum + investment_e1

                investment_e2 = int(re.case_ids[i].turbine_numbers) * int(re.case_ids[i].capacity) * int(
                    re.case_ids[i].investment_turbines_kw) / 10000
                investment_e2_sum = investment_e2_sum + investment_e2

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

                    else:
                        tower_weight_words = tower_weight_words + tower_weight_word
                        rotor_diameter_words = rotor_diameter_words + rotor_diameter_word
                        investment_turbines_kw_words = investment_turbines_kw_words + investment_turbines_kw_word
                        name_tur_words = name_tur_words + name_tur_word
                        capacity_words = capacity_words + capacity_word

                if len(re.case_ids) == 1:
                    tower_weight_words = tower_weight_word
                    rotor_diameter_words = rotor_diameter_word
                    investment_turbines_kw_words = investment_turbines_kw_word
                    capacity_words = capacity_word
                    name_tur_words = name_tur_word

                # if re.ongrid_power == 0:
                #     re.ongrid_power = re.env['auto_word_wind_res.form'].search([('project_id.project_name', '=',
                #                                                                  re.project_id.project_name)])[
                #         i].ongrid_power_sum

            re.name_tur = name_tur_words
            re.capacity = capacity_words
            re.tower_weight = tower_weight_words
            re.rotor_diameter_case = rotor_diameter_words
            re.investment_turbines_kws = investment_turbines_kw_words

            re.farm_capacity = int(re.farm_capacity) / 1000
            re.investment_E1 = investment_e1_sum
            re.investment_E2 = investment_e2_sum

            if re.investment_E4 == 0:
                if re.TerrainType_turbines_compare == "平原":
                    re.investment_E4 = float(re.project_id.total_civil_length) * 50
                elif re.TerrainType_turbines_compare == "丘陵":
                    re.investment_E4 = float(re.project_id.total_civil_length) * 80
                elif re.TerrainType_turbines_compare == "山地":
                    re.investment_E4 = float(re.project_id.total_civil_length) * 140
            else:
                pass

            re.investment_E5 = investment_e5_sum
            re.investment_E6 = investment_e6_sum

            if re.jidian_air_wind == 0 and re.jidian_cable_wind == 0:
                re.investment_E7 = float(re.project_id.jidian_air_wind) * 40 + float(
                    re.project_id.jidian_cable_wind) * 50
            else:
                re.investment_E7 = float(re.jidian_air_wind) * 40 + float(re.jidian_cable_wind) * 50

            re.investment = RoundUp.round_up(re.investment_E1 + re.investment_E2 + re.investment_E3 + re.investment_E4 + \
                                             re.investment_E5 + re.investment_E6 + re.investment_E7)
            # re.ongrid_power=re.res_form.ongrid_power_sum


            if re.ongrid_power!=0:
                re.investment_unit = RoundUp.round_up3(
                    (re.investment / float(re.ongrid_power) * 10), 3)




    def wind_turbines_compare_form_refresh(self):
        for re in self:
            re.content_id.rotor_diameter_case = re.rotor_diameter_case
            re.content_id.case_number = re.case_number

            re.env['auto_word.wind'].search([('project_id.project_name', '=',
                                              re.project_id.project_name)]).recommend_id = re

            re.case_name = re.res_form.case_name
            re.ongrid_power = re.res_form.ongrid_power_sum
            re.hours_year = re.res_form.hours_year_average
            re.weak = re.res_form.wake_average


    def take_result_refresh(self):
        for re in self:
            re.jidian_air_wind = re.project_id.jidian_air_wind
            re.jidian_cable_wind = re.project_id.jidian_cable_wind
            re.investment_E4 = re.project_id.investment_E4

            re.ongrid_power = re.content_id.ongrid_power
            re.weak = re.content_id.weak
            re.hours_year = re.content_id.hours_year
