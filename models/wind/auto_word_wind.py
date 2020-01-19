# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import exceptions
import base64, os
import numpy as np
import global_dict as gl
from array import array
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../GOdoo12_community/myaddons/auto_word/models/source")))
# print(os.path.abspath(os.path.join(os.getcwd(), "../GOdoo12_community/myaddons/auto_word/models/source")))

import doc_5
from RoundUp import round_up, Get_Average, Get_Sum


def cal_wind_result(self):
    self.dict_1_submit_word = self.project_id.dict_1_submit_word
    print("check dict_1_submit_word")
    if self.dict_1_submit_word == False:
        s = "项目"
        raise exceptions.Warning('请点选 %s，并点击 --> 分发信息（%s 位于软件上方，自动编制报告系统右侧）。' % (s, s))
    print(self.dict_1_submit_word)
    print("dict_1_submit_word 已读取")
    # 检查填写内容
    if self.max_wind_txt == "待提交" or self.max_wind_txt == "0":
        s = "五十年一遇最大风速"
        raise exceptions.Warning('请提交 --> %s 信息。' % s)

    if self.Temperature_txt == "待提交" or self.Temperature_txt == "0":
        s = "温度"
        raise exceptions.Warning('请提交 --> %s 信息。' % s)

    if self.area_words == "待提交" or self.area_words == "0":
        s = "风场面积"
        raise exceptions.Warning('请提交 --> %s 信息。' % s)

    if self.cft_name_words == "待提交":
        s = "风能部分"
        raise exceptions.Warning('请点选 %s，并点击 --> 机组选型（%s 位于软件上方，自动编制报告系统右侧）。' % (s, s))

    self.Lat_words = self.project_id.Lat_words
    self.Lon_words = self.project_id.Lon_words
    extreme_wind = round_up(float(self.max_wind_txt) * 1.4)

    if self.recommend_id.case_name == False:
        s = "风能部分"
        raise exceptions.Warning('请点选推荐方案，具体方案详情请点选 %s，并点击 --> 发电量估算（%s 位于软件上方，自动编制报告系统右侧）。' % (s, s))

    # 进行计算
    tur_name = []

    for i in range(0, len(self.select_turbine_ids)):
        tur_name.append(self.select_turbine_ids[i].name_tur)

    self.path_images = self.env['auto_word.project'].path_chapter_5

    case_name_dict, name_tur_dict, turbine_numbers_dict, capacity_dict = [], [], [], []
    farm_capacity_dict, rotor_diameter_dict, tower_weight_dict = [], [], []
    case_hub_height_dict, power_generation_dict, weak_dict = [], [], []
    power_hours_dict, investment_dict, investment_unit_dict = [], [], []
    investment_E1_dict, investment_E2_dict, investment_E3_dict = [], [], []
    investment_E4_dict, investment_E5_dict, investment_E6_dict, investment_E7_dict = [], [], [], []
    investment_turbines_kws_dict = []

    # 机型结果
    project_id_input_dict, case_name_dict, Turbine_dict, tur_id_dict = [], [], [], []
    X_dict, Y_dict, Z_dict, H_dict, Latitude_dict, Longitude_dict, TrustCoefficient_dict = [], [], [], [], [], [], []
    WeibullA_dict, WeibullK_dict, EnergyDensity_dict, PowerGeneration_dict = [], [], [], []
    PowerGeneration_Weak_dict, CapacityCoe_dict, AverageWindSpeed_dict = [], [], []
    TurbulenceEnv_StrongWind_dict, Turbulence_StrongWind_dict, AverageWindSpeed_Weak_dict = [], [], []
    Weak_res_dict, AirDensity_dict, WindShear_Avg_dict, WindShear_Max_dict, WindShear_Max_Deg_dict = [], [], [], [], []
    InflowAngle_Avg_dict, InflowAngle_Max_dict, InflowAngle_Max_Deg_dict, NextTur_dict = [], [], [], []
    NextLength_M_dict, Diameter_dict, NextLength_D_dict, NextDeg_dict, Sectors_dict = [], [], [], [], []
    rate_dict, hours_year_dict, ongrid_power_dict, Elevation_dict = [], [], [], []
    rotor_diameter_dict_words = ""
    ave_elevation, ave_powerGeneration, ave_weak_res, ave_hours_year, ave_ongrid_power = 0, 0, 0, 0, 0
    ave_AverageWindSpeed_Weak, total_powerGeneration, total_ongrid_power, total_powerGeneration_weak = 0, 0, 0, 0

    # 结果 Dict

    for re in self.recommend_id.res_form.auto_word_wind_res:
        project_id_input_dict.append(re.project_id_input)
        Turbine_dict.append(re.Turbine)
        tur_id_dict.append(re.tur_id)
        X_dict.append(re.X)
        Y_dict.append(re.Y)
        Z_dict.append(round_up(float(re.Z)))
        H_dict.append(round_up(float(re.H)))
        Elevation_dict.append(round_up(float(re.Z)) - round_up(float(re.H)))
        Latitude_dict.append(re.Latitude)
        Longitude_dict.append(re.Longitude)
        TrustCoefficient_dict.append(re.TrustCoefficient)
        WeibullA_dict.append(re.WeibullA)
        WeibullK_dict.append(re.WeibullK)
        EnergyDensity_dict.append(re.EnergyDensity)
        PowerGeneration_dict.append(round_up(float(re.PowerGeneration), 1))
        PowerGeneration_Weak_dict.append(round_up(float(re.PowerGeneration_Weak), 1))
        CapacityCoe_dict.append(re.CapacityCoe)
        AverageWindSpeed_dict.append(round_up(float(re.AverageWindSpeed), 2))
        TurbulenceEnv_StrongWind_dict.append(re.TurbulenceEnv_StrongWind)
        Turbulence_StrongWind_dict.append(re.Turbulence_StrongWind)
        AverageWindSpeed_Weak_dict.append(round_up(float(re.AverageWindSpeed_Weak), 2))
        Weak_res_dict.append(round_up(float(re.Weak)))
        AirDensity_dict.append(re.AirDensity)
        WindShear_Avg_dict.append(re.WindShear_Avg)
        WindShear_Max_dict.append(re.WindShear_Max)
        WindShear_Max_Deg_dict.append(re.WindShear_Max_Deg)
        InflowAngle_Avg_dict.append(re.InflowAngle_Avg)
        InflowAngle_Max_dict.append(re.InflowAngle_Max)
        InflowAngle_Max_Deg_dict.append(re.InflowAngle_Max_Deg)
        NextTur_dict.append(re.NextTur)
        NextLength_M_dict.append(re.NextLength_M)
        Diameter_dict.append(re.Diameter)
        NextLength_D_dict.append(re.NextLength_D)
        NextDeg_dict.append(re.NextDeg)
        Sectors_dict.append(re.Sectors)
        rate_dict.append(re.rate)

        ongrid_power_dict.append(round_up(float(re.ongrid_power), 1))
        hours_year_dict.append(round_up(float(re.hours_year), 1))

    ave_elevation = round_up(Get_Average(Elevation_dict), 1)
    ave_AverageWindSpeed_Weak = round_up(Get_Average(AverageWindSpeed_Weak_dict), 2)
    ave_powerGeneration = round_up(Get_Average(PowerGeneration_dict), 1)
    ave_weak_res = round_up(Get_Average(Weak_res_dict))
    ave_weak_res_xz = 100 + ave_weak_res
    ave_hours_year = round_up(Get_Average(hours_year_dict), 1)
    capacity_coefficient = round_up(ave_hours_year / 8760 * 100, 2)
    ave_ongrid_power = round_up(Get_Average(ongrid_power_dict), 1)
    total_powerGeneration_weak = round_up(Get_Sum(PowerGeneration_Weak_dict), 1)
    total_powerGeneration = round_up(Get_Sum(PowerGeneration_dict), 1)
    self.ongrid_power = round_up(Get_Sum(ongrid_power_dict), 1)

    # 方案比选 Dict
    for i in range(0, len(self.case_names)):
        case_name_dict.append(self.case_names[i].case_name)
        name_tur_dict.append('WTG' + str(int(i + 1)))
        turbine_numbers_dict.append(self.case_names[i].turbine_numbers)
        capacity_dict.append(self.case_names[i].capacity)
        farm_capacity_dict.append(self.case_names[i].farm_capacity)
        rotor_diameter_dict.append(self.case_names[i].rotor_diameter_words)
        case_hub_height_dict.append(self.case_names[i].hub_height_suggestion)
        power_generation_dict.append(self.case_names[i].ongrid_power)
        weak_dict.append(self.case_names[i].weak)
        power_hours_dict.append(self.case_names[i].hours_year)
        tower_weight_dict.append(str(self.case_names[i].tower_weight))
        investment_E1_dict.append(str(self.case_names[i].investment_E1))
        investment_E2_dict.append(str(self.case_names[i].investment_E2))
        investment_E3_dict.append(str(self.case_names[i].investment_E3))
        investment_E4_dict.append(str(self.case_names[i].investment_E4))
        investment_E5_dict.append(str(self.case_names[i].investment_E5))
        investment_E6_dict.append(str(self.case_names[i].investment_E6))
        investment_E7_dict.append(str(self.case_names[i].investment_E7))
        investment_dict.append(str(self.case_names[i].investment))
        investment_unit_dict.append(str(self.case_names[i].investment_unit))
        investment_turbines_kws_dict.append(str(self.case_names[i].investment_turbines_kw_words))

    rotor_diameter_dict_words_only = list(set(rotor_diameter_dict))
    print(rotor_diameter_dict_words)
    for j in range(0, len(rotor_diameter_dict_words_only)):
        if j != len(rotor_diameter_dict_words_only) - 1:
            rotor_diameter_dict_words = str(rotor_diameter_dict_words_only[j]) + '/' + rotor_diameter_dict_words
        else:
            rotor_diameter_dict_words = rotor_diameter_dict_words + str(rotor_diameter_dict_words_only[j])

    result = np.vstack((np.array(X_dict), np.array(Y_dict), np.array(Z_dict),
                        np.array(AverageWindSpeed_Weak_dict),
                        np.array(InflowAngle_Max_dict), np.array(PowerGeneration_dict),
                        np.array(Weak_res_dict), np.array(hours_year_dict),
                        np.array(ongrid_power_dict)
                        ))
    result = result.T

    context = {}
    result_list = []
    result_lables_chapter5 = ['X', 'Y', 'Z', '尾流后风速', '最大入流角', '理论发电量',
                              '尾流损失', '满发小时', '上网电量']

    context['result_labels'] = result_lables_chapter5
    for i in range(0, len(result)):
        result_dict = {'number': tur_id_dict[i], 'cols': result[i].tolist()}
        result_list.append(result_dict)
    context['result_list'] = result_list

    dict5 = doc_5.generate_wind_dict(tur_name, self.path_images)
    dict_5_word_part = {
        "叶轮直径words": rotor_diameter_dict_words,
        "方案数": len(rotor_diameter_dict),
        "最终方案": self.recommend_id.case_name,
        "方案e": case_name_dict,
        "风机类型e": name_tur_dict,
        "风机台数e": turbine_numbers_dict,
        "单机容量e": capacity_dict,
        "装机容量e": farm_capacity_dict,
        "叶轮直径e": rotor_diameter_dict,
        "轮毂高度e": case_hub_height_dict,
        "上网电量e": power_generation_dict,
        "尾流衰减e": weak_dict,
        "满发小时e": power_hours_dict,
        "塔筒重量e": tower_weight_dict,
        "风机投资e": investment_turbines_kws_dict,
        "塔筒投资e": investment_E1_dict,
        "风机设备投资e": investment_E2_dict,
        "基础投资e": investment_E3_dict,
        "道路投资e": investment_E4_dict,
        "吊装费用e": investment_E5_dict,
        "箱变投资e": investment_E6_dict,
        "集电线路e": investment_E7_dict,
        "发电部分投资e": investment_dict,
        "单位度电投资e": investment_unit_dict,
    }
    # 提交的生成chapter5的dict
    dict_5_suggestion_word = {
        "山地类型": self.TerrainType,
        "海拔高程": self.Elevation_words,
        "风场面积": self.area_words,

        '推荐机型': self.name_tur_suggestion,
        '推荐机组数量': self.turbine_numbers_suggestion,
        '推荐单机容量': self.TurbineCapacity_suggestion,
        "推荐叶轮直径": self.rotor_diameter_suggestion,
        '推荐轮毂高度': self.hub_height_suggestion,
        '推荐叶片数': self.blade_number_suggestion,
        '推荐扫风面积': self.rotor_swept_area_suggestion,

        '推荐切入风速': self.cut_in_wind_speed_suggestion,
        '推荐切出风速': self.cut_out_wind_speed_suggestion,
        '推荐额定风速': self.rated_wind_speed_suggestion,
        '推荐生存风速': self.three_second_maximum_suggestion,
        '推荐额定功率': self.rated_power_suggestion,
        '推荐额定电压': self.voltage_suggestion,

        '装机容量': self.project_capacity,
        "上网电量": self.ongrid_power,
        "满发小时": ave_hours_year,
        "容量系数": capacity_coefficient,
        "风功率密度等级": self.PWDLevel,

        "风速信息": self.string_speed_words,
        "选取时段": self.cft_time_words,
        "湍流信息": self.cft_TI_words,
        "风向信息": self.string_deg_words,
        "测风塔数目": self.cft_number_words,
        '测风塔名字': self.cft_name_words,

        "五十年一遇最大风速": self.max_wind_txt,
        "五十年一遇极大风速": extreme_wind,
        "折减率": self.rate,
        "折减率备注": self.project_id.note,
        'IEC等级': self.IECLevel,
        "风速区间": self.farm_speed_range_words,

        "平均温度": self.Temperature_txt,
        "平均海拔": ave_elevation,
        "尾流后平均风速": ave_AverageWindSpeed_Weak,
        "平均发电量": ave_powerGeneration,
        "总发电量": total_powerGeneration,
        "平均尾流损失": ave_weak_res,
        "平均上网电量": ave_ongrid_power,
        "尾流损失修正系数": ave_weak_res_xz,
        "尾流修正后的总理论发电量": total_powerGeneration_weak,
        "空气密度": self.air_density_words,

        'WTG数量': str(len(self.select_turbine_ids)),
        '推荐风机型号_WTG': self.project_id.turbine_model_suggestion,
        '限制性因素': self.project_id.limited_words,
    }

    dict_5_submit_word = dict(dict_5_word_part, **dict5, **context, **dict_5_suggestion_word)

    # 生成chapter5 所需要的总的dict
    dict_5_words = dict(dict_5_submit_word, **eval(self.dict_1_submit_word))

    # for key, value in dict_5_word.items():
    #     gl.set_value(key, value)

    return dict_5_words, dict_5_submit_word


class auto_word_wind(models.Model):
    _name = 'auto_word.wind'
    _description = 'Wind energy input'
    _rec_name = 'content_id'

    # 提交
    dict_5_submit_word = fields.Char(u'字典5_提交')
    # 提取
    dict_1_submit_word = fields.Char(u'字典1_提交')
    # 项目参数
    project_id = fields.Many2one('auto_word.project', string=u'项目名', required=True)
    version_id = fields.Char(u'版本', default="1.0", required=True)
    content_id = fields.Selection([("风能", u"风能"), ("电气", u"电气"), ("土建", u"土建"),
                                   ("其他", u"其他")], string=u"章节分类", required=True)

    # --------风场信息---------
    # 风能
    Lon_words = fields.Char(string=u'东经', default="待提交", readonly=True)
    Lat_words = fields.Char(string=u'北纬', default="待提交", readonly=True)
    Elevation_words = fields.Char(string=u'海拔高程', default='588m～852m', required=True)
    Relative_height_difference_words = fields.Char(string=u'相对高差', default='100m-218m', required=True)
    area_words = fields.Char(string=u'风场面积', default="待提交", required=True)
    farm_speed_range_words = fields.Char(string=u'风速区间', default="5.2~6.4", required=True)
    air_density_words = fields.Char(string=u'空气密度', default="1.096", required=True)
    # 限制性因素
    limited_1 = fields.Boolean(u'是否占用基本农田')
    limited_2 = fields.Boolean(u'是否占用生态红线')
    limited_3 = fields.Boolean(u'是否存在压覆矿')
    limited_words = fields.Char(u'限制性因素')

    IECLevel = fields.Selection([("IA", u"IA"), ("IIA", u"IIA"), ("IIIA", u"IIIA"),
                                 ("IB", u"IB"), ("IIB", u"IIB"), ("IIIB", u"IIIB"),
                                 ("IC", u"IC"), ("IIC", u"IIC"), ("IIIC", u"IIIC"),
                                 ], string=u"IEC等级", default="IIIB", required=True)
    PWDLevel = fields.Selection([("I", u"I"), ("II", u"II"), ("III", u"III"),
                                 ("IV", u"IV"), ("V", u"V"), ("VI", u"VI"),
                                 ("VII", u"VII")], string=u"风功率密度等级", default="I", required=True)

    TerrainType = fields.Selection(
        [("平原", u"平原"), ("丘陵", u"丘陵"), ("缓坡低山", u"缓坡低山"), ("陡坡低山", u"陡坡低山"), ("缓坡中山", u"缓坡中山"),
         ("陡坡中山", u"陡坡中山"), ("缓坡高山", u"缓坡高山"), ("陡坡高山", u"陡坡高山")], string=u"山地类型", required=True)

    Temperature_txt = fields.Char(u'平均温度', default="待提交", required=True)
    max_wind_txt = fields.Char(u'50年一遇最大风速', default="待提交", required=True)

    # --------测风信息---------
    cft_name_words = fields.Char(string=u'测风塔名字', default="待提交", readonly=True)
    cft_number_words = fields.Char(string=u'测风塔数目', default="待提交", readonly=True)
    string_speed_words = fields.Char(string=u'风速信息', default="待提交", readonly=True)
    string_deg_words = fields.Char(string=u'风向信息', default="待提交", readonly=True)
    cft_TI_words = fields.Char(string=u'湍流信息', default="待提交", readonly=True)
    cft_time_words = fields.Char(string=u'选取时间段', default="待提交", readonly=True)
    note = fields.Char(string=u'备注', readonly=False)

    # ####################################功能模块########################
    # --------机型推荐---------
    select_turbine_ids = fields.Many2many('auto_word_wind.turbines', string=u'机组选型', required=False)
    # --------方案比选---------
    recommend_id = fields.Many2one('auto_word_wind_turbines.compare', string=u'推荐方案', required=False)
    case_names = fields.Many2many('auto_word_wind_turbines.compare', string=u'方案名称', required=False)
    case_number = fields.Char(string=u'方案数', default="待提交", readonly=True)
    name_tur_suggestion = fields.Char(u'推荐机型', compute='_compute_compare_case', readonly=True)
    turbine_numbers_suggestion = fields.Char(u'机组数量', compute='_compute_compare_case', readonly=True)
    hub_height_suggestion = fields.Char(u'轮毂高度', compute='_compute_compare_case', readonly=True)
    rotor_diameter_suggestion = fields.Char(string=u'叶轮直径', readonly=True, default="待提交",
                                            compute='_compute_compare_case')
    TurbineCapacity_suggestion = fields.Char(string=u'推荐单机容量', readonly=True, default="待提交",
                                             compute='_compute_compare_case')
    rotor_swept_area_suggestion = fields.Char(string=u'推荐扫风面积', readonly=True, default="待提交",
                                              compute='_compute_compare_case')
    blade_number_suggestion = fields.Char(string=u'推荐叶片数', readonly=True, default="待提交",
                                          compute='_compute_compare_case')
    cut_in_wind_speed_suggestion = fields.Char(string=u'推荐切入风速', readonly=True, default="待提交",
                                               compute='_compute_compare_case')
    cut_out_wind_speed_suggestion = fields.Char(string=u'推荐切出风速', readonly=True, default="待提交",
                                                compute='_compute_compare_case')
    rated_wind_speed_suggestion = fields.Char(string=u'推荐额定风速', readonly=True, default="待提交",
                                              compute='_compute_compare_case')
    three_second_maximum_suggestion = fields.Char(string=u'推荐生存风速', readonly=True, default="待提交",
                                                  compute='_compute_compare_case')
    rated_power_suggestion = fields.Char(string=u'推荐额定功率', readonly=True, default="待提交",
                                         compute='_compute_compare_case')
    voltage_suggestion = fields.Char(string=u'推荐额定电压', readonly=True, default="待提交",
                                     compute='_compute_compare_case')
    investment_turbines_kws = fields.Char(u'风机投资（KW）', compute='_compute_compare_case')
    project_capacity = fields.Char(string=u'装机容量', readonly=True, compute='_compute_compare_case', default="待提交")

    ongrid_power = fields.Char(u'上网电量', readonly=True, compute='_compute_compare_case')
    weak = fields.Char(u'尾流衰减', default="待提交", readonly=True, compute='_compute_compare_case')
    hours_year = fields.Char(u'满发小时', default="待提交", readonly=True, compute='_compute_compare_case')
    capacity_coefficient = fields.Char(u'容量系数', default="待提交", readonly=True, compute='_compute_compare_case')
    rate = fields.Char(string=u'风场折减', default="待提交", readonly=True, compute='_compute_compare_case')
    tower_weight = fields.Char(string=u'塔筒重量', default="待提交", readonly=True, compute='_compute_compare_case')

    # --------结果文件---------
    # auto_word_wind_res = fields.Many2many('auto_word_wind.res', string=u'机位结果', required=False)
    path_images = fields.Char(u'图片路径')
    file_excel_path = fields.Char(u'文件路径')
    report_attachment_id = fields.Many2one('ir.attachment', string=u'可研报告风能章节')
    report_attachment_id2 = fields.Many2many('ir.attachment', string=u'图片')
    attachment_number = fields.Integer(compute='_compute_attachment_number', string='Number of Attachments')


    # ############################################################
    png_list = []
    project_id_input_dict, case_name_dict, Turbine_dict, tur_id_dict = [], [], [], []
    X_dict, Y_dict, Z_dict, H_dict, Latitude_dict, Longitude_dict, TrustCoefficient_dict = [], [], [], [], [], [], []
    WeibullA_dict, WeibullK_dict, EnergyDensity_dict, PowerGeneration_dict = [], [], [], []
    PowerGeneration_Weak_dict, CapacityCoe_dict, AverageWindSpeed_dict = [], [], []
    TurbulenceEnv_StrongWind_dict, Turbulence_StrongWind_dict, AverageWindSpeed_Weak_dict = [], [], []
    Weak_res_dict, AirDensity_dict, WindShear_Avg_dict, WindShear_Max_dict, WindShear_Max_Deg_dict = [], [], [], [], []
    InflowAngle_Avg_dict, InflowAngle_Max_dict, InflowAngle_Max_Deg_dict, NextTur_dict = [], [], [], []
    NextLength_M_dict, Diameter_dict, NextLength_D_dict, NextDeg_dict, Sectors_dict = [], [], [], [], []
    rate_dict, hours_year_dict, ongrid_power_dict, Elevation_dict = [], [], [], []
    ave_elevation, ave_powerGeneration, ave_weak_res, ave_hours_year, ave_ongrid_power = 0, 0, 0, 0, 0
    ave_AverageWindSpeed_Weak, total_powerGeneration, total_ongrid_power, total_powerGeneration_weak = 0, 0, 0, 0
    ave_weak_res_xz = 0

    @api.depends('recommend_id')
    def _compute_compare_case(self):
        for re in self:
            re.name_tur_suggestion = re.recommend_id.name_tur_words
            re.hub_height_suggestion = re.recommend_id.hub_height_suggestion
            re.turbine_numbers_suggestion = re.recommend_id.turbine_numbers
            re.project_capacity = re.recommend_id.farm_capacity
            re.rotor_diameter_suggestion = re.recommend_id.rotor_diameter_words
            re.TurbineCapacity_suggestion = float(re.recommend_id.capacity) / 1000
            re.rotor_swept_area_suggestion = re.recommend_id.rotor_swept_area_words
            re.blade_number_suggestion = re.recommend_id.blade_number_words
            re.cut_in_wind_speed_suggestion = re.recommend_id.cut_in_wind_speed_words
            re.cut_out_wind_speed_suggestion = re.recommend_id.cut_out_wind_speed_words
            re.rated_wind_speed_suggestion = re.recommend_id.rated_wind_speed_words
            re.three_second_maximum_suggestion = re.recommend_id.three_second_maximum_words
            re.rated_power_suggestion = re.recommend_id.rated_power_words
            re.voltage_suggestion = re.recommend_id.voltage_words
            # re.auto_word_wind_res = re.recommend_id.res_form.auto_word_wind_res
            re.weak = re.recommend_id.weak
            re.hours_year = re.recommend_id.hours_year
            re.rate = re.recommend_id.res_form.rate
            re.capacity_coefficient = re.recommend_id.res_form.capacity_coefficient
            re.investment_turbines_kws = re.recommend_id.investment_turbines_kw_words
            re.ongrid_power = re.recommend_id.ongrid_power
            re.tower_weight = re.recommend_id.tower_weight

    @api.multi
    def submit_wind(self):
        limited_str_1, limited_str_2, limited_str_3, limited_words = "", "", "", ""
        self.project_id.rate = self.rate
        self.project_id.wind_attachment_ok = u"已提交,版本：" + self.version_id
        self.project_id.case_name = str(self.recommend_id.case_name)
        self.project_id.turbine_model_suggestion = self.recommend_id.WTG_name
        self.project_id.turbine_numbers_suggestion = self.recommend_id.turbine_numbers
        self.project_id.hub_height_suggestion = self.recommend_id.hub_height_suggestion
        self.project_id.name_tur_suggestion = self.recommend_id.name_tur_words
        self.project_id.investment_E1 = self.recommend_id.investment_E1
        self.project_id.investment_E2 = self.recommend_id.investment_E2
        self.project_id.investment_E3 = self.recommend_id.investment_E3
        self.project_id.investment_E4 = self.recommend_id.investment_E4
        self.project_id.investment_E5 = self.recommend_id.investment_E5
        self.project_id.investment_E6 = self.recommend_id.investment_E6
        self.project_id.investment_E7 = self.recommend_id.investment_E7
        self.project_id.investment = self.recommend_id.investment
        self.project_id.investment_unit = self.recommend_id.investment_unit
        limited_str_0 = "本项目区域内存在部分限制性因素，需重点对"
        limited_str_2 = "等限制性因素进行排查。"
        # self.project_id.investment_turbines_kws = self.investment_turbines_kws

        self.project_id.tower_weight = self.tower_weight
        self.project_id.rate = self.rate
        self.project_id.IECLevel = self.IECLevel
        self.project_id.PWDLevel = self.PWDLevel
        self.project_id.farm_speed_range_words = self.farm_speed_range_words
        self.project_id.TerrainType = self.TerrainType

        self.project_id.cft_time_words = self.cft_time_words
        self.project_id.string_speed_words = self.string_speed_words
        self.project_id.cft_TI_words = self.cft_TI_words

        self.project_id.max_wind_txt = self.max_wind_txt

        if self.limited_1 == True:
            if self.limited_2 == False and self.limited_3 == False:
                limited_str_1 = "基本农田"
            elif self.limited_2 == True and self.limited_3 == False:
                limited_str_1 = "基本农田、生态红线"
            elif self.limited_2 == False and self.limited_3 == True:
                limited_str_1 = "基本农田、压覆矿"
            else:
                limited_str_1 = "基本农田、生态红线、压覆矿"

        elif self.limited_2 == True and self.limited_3 == False:
            limited_str_1 = "生态红线"
        elif self.limited_2 == True and self.limited_3 == False:
            limited_str_1 = "生态红线、压覆矿"
        elif self.limited_2 == False and self.limited_3 == True:
            limited_str_1 = "压覆矿"
        self.limited_words = limited_str_0 + limited_str_1 + limited_str_2

        if self.limited_1 == False and self.limited_2 == False and self.limited_3 == False:
            self.limited_words = "本项目区域内未存在限制性因素"

        self.project_id.limited_words = self.limited_words
        # 风能
        self.project_id.Lon_words = self.Lon_words
        self.project_id.Lat_words = self.Lat_words
        self.project_id.Elevation_words = self.Elevation_words
        self.project_id.Relative_height_difference_words = self.Relative_height_difference_words
        self.project_id.ongrid_power = self.ongrid_power
        self.project_id.weak = self.weak
        self.project_id.Hour_words = self.hours_year
        self.project_id.TurbineCapacity = self.TurbineCapacity_suggestion
        self.project_id.dict_5_submit_word = self.dict_5_submit_word
        self.project_id.area_words = self.area_words
        self.project_id.project_capacity = self.project_capacity

    def wind_generate(self):
        dict_5_words, dict_5_submit_word = cal_wind_result(self)
        # print("生成")
        # print(dict_5_words)
        self.dict_5_submit_word = dict_5_submit_word

        for re in self.report_attachment_id2:
            imgdata = base64.standard_b64decode(re.datas)
            t = re.name
            suffix = ".png"
            # suffix = ".xls"
            newfile = t + suffix
            Patt = os.path.join(self.path_images, '%s') % newfile
            if not os.path.exists(Patt):
                f = open(Patt, 'wb+')
                f.write(imgdata)
                f.close()
            else:
                print(Patt + " already existed.")
                f = open(Patt, 'wb+')
                f.write(imgdata)
                f.close()
            self.png_list.append(t)

        doc_5.generate_wind_docx1(dict_5_words, self.path_images, self.png_list)
        ###########################

        reportfile_name = open(file=os.path.join(self.path_images, '%s.docx') % 'result_chapter5',
                               mode='rb')
        byte = reportfile_name.read()
        reportfile_name.close()
        # print('file lenth=', len(byte))
        base64.standard_b64encode(byte)
        if (str(self.report_attachment_id) == 'ir.attachment()'):
            Attachments = self.env['ir.attachment']
            print('开始创建新纪录')
            New = Attachments.create({
                'name': self.project_id.project_name + '可研报告风电章节下载页',
                'datas_fname': self.project_id.project_name + '可研报告风电章节.docx',
                'datas': base64.standard_b64encode(byte),
                'display_name': self.project_id.project_name + '可研报告风电章节',
                'create_date': fields.date.today(),
                'public': True,  # 此处需设置为true 否则attachments.read  读不到
                # 'mimetype': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                # 'res_model': 'autoreport.project'
                # 'res_field': 'report_attachment_id'
            })
            print('已创建新纪录：', New)
            print('new dataslen：', len(New.datas))
            self.report_attachment_id = New
        else:
            self.report_attachment_id.datas = base64.standard_b64encode(byte)

        print('new attachment：', self.report_attachment_id)
        print('new datas len：', len(self.report_attachment_id.datas))

        print("生成的dict_5_submit_word")
        print(self.dict_5_submit_word)
        return True

    @api.multi
    def action_get_attachment_view(self):
        """附件上传动作视图"""
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('base', 'action_attachment')
        res['domain'] = [('res_model', '=', 'auto_word.wind'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'auto_word.wind', 'default_res_id': self.id}
        return res

    @api.multi
    def _compute_attachment_number(self):
        """附件上传"""
        attachment_data = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'auto_word.wind'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for expense in self:
            expense.attachment_number = attachment.get(expense.id, 0)
