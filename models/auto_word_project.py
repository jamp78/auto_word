# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import exceptions
import base64
import datetime


class auto_word_project(models.Model):
    _name = 'auto_word.project'
    _description = 'Project'
    _rec_name = 'project_name'
    path_images_chapter_2 = r"D:\GOdoo12_community\myaddons\auto_word\models\wind\chapter_2"
    path_images_chapter_5 = r"D:\GOdoo12_community\myaddons\auto_word\models\wind\chapter_5"
    economy_path = r'D:\GOdoo12_community\myaddons\auto_word\models\economy\chapter_'
    path_images_chapter_6 = r"D:\GOdoo12_community\myaddons\auto_word\models\electrical\chapter_6"
    path_chapter_8 = r'D:\GOdoo12_community\myaddons\auto_word\models\civil\chapter_8'

    # 项目字段
    project_name = fields.Char(u'项目名', required=True, write=['auto_word.project_group_user'])
    Farm_words = fields.Char(string=u'风电场名称', default='华润郁南欣茂风电项目')
    Location_words = fields.Char(string=u'建设地点', default='广东省云浮市')
    order_number = fields.Char(u'项目编号', required=True)
    active = fields.Boolean(u'续存？', default=True)
    date_start = fields.Date(u'项目启动日期', default=fields.date.today())
    date_end = fields.Date(u'项目要求完成日期', default=fields.date.today() + datetime.timedelta(days=10))
    company_id = fields.Many2one('res.company', string=u'项目所在大区')
    contacts_ids = fields.Many2many('res.partner', string=u'项目联系人')
    favorite_user_ids = fields.Many2many('res.users', string=u'项目组成员')
    staff = fields.Integer(u'工程定员')
    message_main_attachment_id = fields.Many2many('ir.attachment', string=u'任务资料')

    # 文件情况
    wind_attachment_id = fields.Many2one('auto_word.wind', string=u'风能数据', groups='auto_word.wind_group_user')
    wind_attachment_ok = fields.Char(u'风能数据', default="待提交", readonly=True)
    electrical_attachment_id = fields.Many2one('auto_word.electrical', string=u'电气数据',
                                               groups='auto_word.electrical_group_user')
    electrical_attachment_ok = fields.Char(u'电气数据', default="待提交", readonly=True)
    civil_attachment_id = fields.Many2one('auto_word.civil', string=u'土建数据', groups='auto_word.civil_group_user')
    civil_attachment_ok = fields.Char(u'土建数据', default="待提交", readonly=True)
    economic_attachment_id = fields.Many2one('auto_word.economic', string=u'经评数据',
                                             groups='auto_word.economic_group_user')
    economic_attachment_ok = fields.Char(u'经评数据', default="待提交", readonly=True)
    report_attachment_id = fields.Many2one('ir.attachment', string=u'可研报告成果')

    ###风能
    project_capacity = fields.Char(u'项目容量', default="待提交", readonly=True)
    name_tur_suggestion = fields.Char(u'风机推荐型号', default="待提交", readonly=True)
    name_tur_selection = fields.Char(u'风机比选型号', default="待提交", readonly=True)
    turbine_numbers_suggestion = fields.Char(u'机位数', default="0", readonly=True)
    hub_height_suggestion = fields.Char(u'推荐轮毂高度', readonly=True)
    capacity_suggestion = fields.Char(string=u'单机容量建议(kW)', readonly=True)
    investment_turbines_kws = fields.Char(u'风机kw投资')

    select_turbine_ids = fields.Many2many('auto_word_wind.turbines', string=u'机组选型')
    name_tur_selection = fields.Char(string=u'风机比选型号', readonly=True, default="待提交")
    turbine_model_suggestion = fields.Char(string=u'风机比选型号_WTG', readonly=True, default="待提交")
    string_speed_words = fields.Char(string=u'测风塔选定风速结果', default="待提交")
    string_deg_words = fields.Char(string=u'测风塔选定风向结果', default="待提交")
    cft_name_words = fields.Char(string=u'测风塔名字', default="待提交")
    rate = fields.Char(string=u'折减率', readonly=False)
    note = fields.Char(string=u'备注', readonly=False)
    limited_words = fields.Char(u'限制性因素', required=False)

    # 风能
    Lon_words = fields.Char(string=u'东经', default='待提交')
    Lat_words = fields.Char(string=u'北纬', default='待提交')
    Elevation_words = fields.Char(string=u'海拔高程', default='待提交')
    Relative_height_difference_words = fields.Char(string=u'相对高差', default='待提交')

    Turbine_number_words = fields.Char(string=u'风力发电机组', default="待提交", readonly=True)
    Farm_capacity_words = fields.Char(string=u'装机容量', default="待提交", readonly=True)
    Hour_words = fields.Char(string=u'满发小时', default="待提交", readonly=True)

    ongrid_power = fields.Char(u'上网电量', default="待提交")
    weak = fields.Char(u'尾流衰减', default="待提交")

    ###电气
    line_1 = fields.Char(u'线路总挖方', default="0", readonly=True)
    line_2 = fields.Char(u'线路总填方', default="0", readonly=True)
    overhead_line = fields.Char(u'架空线路用地', default="0", readonly=True)
    direct_buried_cable = fields.Char(u'直埋电缆用地', default="0", readonly=True)
    overhead_line_num = fields.Char(u'架空线路塔基数量', default="0", readonly=True)
    direct_buried_cable_num = fields.Char(u'直埋电缆长度', default="0", readonly=True)
    main_booster_station_num = fields.Char(u'主变数量', default="0", readonly=True)

    voltage_class = fields.Char(u'地形', default="待提交", readonly=True)
    length_single_jL240 = fields.Char(u'单回线路JL/G1A-240/30长度（km）', default="0", readonly=True)
    length_double_jL240 = fields.Char(u'双回线路JL/G1A-240/30长度（km）', default="0", readonly=True)
    yjlv95 = fields.Char(u'直埋电缆YJLV22-26/35-3×95（km）', default="0", readonly=True)
    yjv300 = fields.Char(u'直埋电缆YJV22-26/35-1×300（km）', default="0", readonly=True)
    circuit_number = fields.Char(u'线路回路数', default="0", readonly=True)

    jidian_air_wind = fields.Char(u'架空长度', readonly=True, default="0")
    jidian_cable_wind = fields.Char(u'电缆长度', readonly=True, default="0")

    ###土建
    road_1_num = fields.Char(u'场外改扩建道路', default="待提交", readonly=True)
    road_2_num = fields.Char(u'进站道路', default="待提交", readonly=True)
    road_3_num = fields.Char(u'施工检修道路工程', default="待提交", readonly=True)
    total_civil_length = fields.Float(u'道路工程长度', default="0", readonly=True)

    basic_type = fields.Char(u'基础形式', default="待提交", readonly=True)
    ultimate_load = fields.Char(u'极限载荷', default="待提交", readonly=True)
    fortification_intensity = fields.Char(u'设防烈度', default="待提交", readonly=True)
    temporary_land_area = fields.Char(u'临时用地面积（亩）', default="0", readonly=True)
    permanent_land_area = fields.Char(u'永久用地面积（亩）', default="0", readonly=True)
    TurbineCapacity = fields.Char(u'风机容量', default="0", readonly=True)
    excavation = fields.Char(u'总开挖量（m3）', default="0", readonly=True)
    backfill = fields.Char(u'总回填量（m3）', default="0", readonly=True)
    spoil = fields.Char(u'弃土量（m3）', default="0", readonly=True)

    Status = fields.Char(u'升压站状态', default="待提交", readonly=True)
    Grade = fields.Char(u'升压站等级', default="待提交", readonly=True)
    Capacity = fields.Char(u'升压站容量', default="待提交", readonly=True)

    TerrainType = fields.Char(u'山地类型', default="待提交", readonly=True)

    ProjectLevel = fields.Char(u'项目工程等别', default="待提交", readonly=True)
    ProjectLevel_all = fields.Many2one('auto_word_civil.design_safety_standard', string=u'项目工程等别')

    civil_all = fields.Many2one('auto_word.civil', string=u'详细用量表')

    # 土建结果
    # 风机基础工程数量表
    EarthExcavation_WindResource = fields.Char(u'土方开挖（m3）')
    StoneExcavation_WindResource = fields.Char(u'石方开挖（m3）')
    EarthWorkBackFill_WindResource = fields.Char(u'土石方回填（m3）')
    Volume = fields.Char(u'C40混凝土（m3）')
    Cushion = fields.Char(u'C15混凝土（m3）')
    Reinforcement = fields.Char(u'钢筋（t）')
    Based_Waterproof = fields.Char(u'基础防水', default=1)
    Settlement_Observation = fields.Char(u'沉降观测', default=4)
    SinglePileLength = fields.Char(u'总预制桩长（m）')
    M48PreStressedAnchor = fields.Char(u'M48预应力锚栓（m）')
    C80SecondaryGrouting = fields.Char(u'C80二次灌浆（m3）')
    stake_number = fields.Char(u'单台风机桩根数（根）')

    case_name = fields.Char(u'方案名', readonly=True, default="待提交")
    investment_E1 = fields.Char(u'塔筒投资(万元)', readonly=True, default="0")
    investment_E2 = fields.Char(u'风机设备投资(万元)', readonly=True, default="0")
    investment_E3 = fields.Char(u'基础投资(万元)', readonly=True, default="0")
    investment_E4 = fields.Char(u'道路投资(万元)', readonly=True, default="0")
    investment_E5 = fields.Char(u'吊装费用(万元)', readonly=True, default="0")
    investment_E6 = fields.Char(u'箱变投资(万元)', readonly=True, default="0")
    investment_E7 = fields.Char(u'集电线路(万元)', readonly=True, default="0")
    investment = fields.Char(u'发电部分投资(万元)', readonly=True, default="0")
    investment_unit = fields.Char(u'单位度电投资(万元)', readonly=True, default="0")

    static_investment_13 = fields.Char(string=u'静态总投资')
    static_investment_unit = fields.Char(string=u'单位千瓦静态投资')
    dynamic_investment_13 = fields.Char(string=u'动态总投资')
    dynamic_investment_unit = fields.Char(string=u'单位千瓦动态投资')
    Internal_financial_rate_before = fields.Char(string=u'税前财务内部收益率(%)')
    Internal_financial_rate_after = fields.Char(string=u'税后财务内部收益率(%)')
    Internal_financial_rate_capital = fields.Char(string=u'资本金税后内部收益率(%)')
    payback_period = fields.Char(string=u'投资回收期(年)')
    ROI_13 = fields.Char(string=u'总投资收益率(%)')
    ROE_13 = fields.Char(string=u'资本金利润率(%)')


class auto_word_null_project(models.Model):
    _name = 'auto_word_null.project'
    _description = 'null Project'
