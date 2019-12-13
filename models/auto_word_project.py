# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import exceptions
import base64, os
from docxtpl import DocxTemplate
from RoundUp import round_up
import datetime
import global_dict as gl
from energy_saving import energy_saving_cal, energy_using_cal
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../GOdoo12_community/myaddons/auto_word/models/wind")))
import auto_word_wind

import win32com.client as win32
import pythoncom

# from docx import Document
# from docxcompose.composer import Composer
# from docx import Document as Document_compose

gl._init()


def generate_docx(Dict, path_images, model_name, outputfile):
    filename_box = [model_name, outputfile]
    read_path = os.path.join(path_images, '%s') % filename_box[0]
    save_path = os.path.join(path_images, '%s') % filename_box[1]
    tpl = DocxTemplate(read_path)
    tpl.render(Dict)
    tpl.save(save_path)


def dict_project_1(self):
    dict_1_word = {
        "概述": self.summary_txt,
        "风电场名称": self.Farm_words,
        "建设地点": self.Location_words,
        "项目大区": self.company_id.name,
        "相对高差": self.Relative_height_difference_words,
    }

    return dict_1_word


def dict_project_x(self):
    dict_1_word = dict_project_1(self)
    mei_t = round_up(float(self.ongrid_power) / 10 * 2.29 / 7151.69)
    s02 = round_up(float(self.ongrid_power) / 10 * 1716.41 / 7151.69)
    n02 = round_up(float(self.ongrid_power) / 10 * 858.2 / 7151.69)
    c02 = round_up(float(self.ongrid_power) / 10 * 5.71 / 7151.69)

    # extreme_wind = round_up(float(self.max_wind_txt) * 1.4)

    if float(self.project_capacity) >= 100:
        self.environmental_protection_investment = '170'
    elif float(self.project_capacity) < 100 and float(self.project_capacity) >= 50:
        self.environmental_protection_investment = '123'
    elif float(self.project_capacity) < 50:
        self.environmental_protection_investment = '50'

    self.capacity_suggestion = float(self.TurbineCapacity) * 1000
    self.capacity_coefficient = round_up(float(self.Hour_words) / 8760)

    # self.land_area = float(self.permanent_land_area) + float(self.temporary_land_area)

    dict_14_1 = energy_saving_cal(self.ongrid_power, self.project_capacity, self.TurbineCapacity, self.Grade,
                                  self.Hour_words,
                                  self.turbine_numbers_suggestion, self.total_civil_length, self.grid_price)

    dict_14_2 = energy_using_cal(self.excavation, self.backfill, self.Concrete_words, self.Reinforcement)

    dict_1_res_word = {

        "标煤": mei_t,
        "SO2": s02,
        "NOx": n02,
        "CO2": c02,
        "环境保护总投资": self.environmental_protection_investment,
        "水土保持": self.conservation_water_soil,
    }

    dict_x = dict(dict_1_word, **dict_1_res_word, **dict_14_1, **dict_14_2)
    # for key, value in dict_x.items():
    #     gl.set_value(key, value)

    # dict_x = gl._global_dict
    #
    # print('gl._global_dict')
    # print(gl._global_dict)

    return dict_x


# Filename_master is the name of the file you want to merge all the document into
# files_list is a list containing all the filename of the docx file to be merged
# def combine_all_docx(filename_master,files_list,Pathoutput):
#     number_of_sections=len(files_list)
#     master = Document_compose(filename_master)
#     composer = Composer(master)
#     for i in range(0, number_of_sections):
#         doc_temp = Document_compose(files_list[i])
#         composer.append(doc_temp)
#     composer.save(Pathoutput)
# For Example
# filename_master="file1.docx"
# files_list=["file2.docx","file3.docx","file4.docx",file5.docx"]
# Calling the function
# combine_all_docx(filename_master,files_list)
# This function will combine all the document in the array files_list into the file1.docx and save the merged document into combined_file.docx

class auto_word_project(models.Model):
    _name = 'auto_word.project'
    _description = 'Project'
    _rec_name = 'project_name'
    path_images_chapter_2 = r"D:\GOdoo12_community\myaddons\auto_word\models\wind\chapter_2"
    path_images_chapter_5 = r"D:\GOdoo12_community\myaddons\auto_word\models\wind\chapter_5"
    project_path = r'D:\GOdoo12_community\myaddons\auto_word\models\project\chapter_'
    economy_path = r'D:\GOdoo12_community\myaddons\auto_word\models\economy\chapter_'
    path_images_chapter_6 = r"D:\GOdoo12_community\myaddons\auto_word\models\electrical\chapter_6"
    path_chapter_8 = r'D:\GOdoo12_community\myaddons\auto_word\models\civil\chapter_8'
    path_chapter_6 = r'D:\GOdoo12_community\myaddons\auto_word\models\electrical\chapter_6'

    # 项目字段
    project_name = fields.Char(u'项目名', required=True, write=['auto_word.project_group_user'])
    Farm_words = fields.Char(string=u'风电场名称', required=True)
    Location_words = fields.Char(string=u'建设地点', required=True)
    area_words = fields.Char(string=u'风场面积', required=True)

    order_number = fields.Char(u'项目编号')
    active = fields.Boolean(u'续存？', default=True)
    date_start = fields.Date(u'项目启动日期', default=fields.date.today())
    date_end = fields.Date(u'项目要求完成日期', default=fields.date.today() + datetime.timedelta(days=10))
    company_id = fields.Many2one('res.company', string=u'项目大区', required=True)
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
    project_capacity = fields.Char(u'项目容量', default="待提交", readonly=True)  ######################
    name_tur_suggestion = fields.Char(u'风机推荐型号', default="待提交", readonly=True)
    name_tur_selection = fields.Char(u'风机比选型号', default="待提交", readonly=True)
    turbine_numbers_suggestion = fields.Char(u'机组数量', default="0", readonly=True)
    hub_height_suggestion = fields.Char(u'推荐轮毂高度', readonly=True)
    capacity_suggestion = fields.Char(string=u'单机容量建议(kW)', readonly=True)

    investment_turbines_kws = fields.Char(u'风机kw投资', readonly=True)

    select_turbine_ids = fields.Many2many('auto_word_wind.turbines', string=u'机组选型')
    name_tur_selection = fields.Char(string=u'风机比选型号', readonly=True, default="待提交")
    turbine_model_suggestion = fields.Char(string=u'风机比选型号_WTG', readonly=True, default="待提交")
    string_speed_words = fields.Char(string=u'测风塔选定风速结果', default="待提交")
    string_deg_words = fields.Char(string=u'测风塔选定风向结果', default="待提交")
    cft_name_words = fields.Char(string=u'测风塔名字', default="待提交")
    rate = fields.Char(string=u'折减率', readonly=False)
    note = fields.Char(string=u'备注', readonly=False)
    limited_words = fields.Char(u'限制性因素', required=False)

    Lon_words = fields.Char(string=u'东经', default='待提交', required=True)
    Lat_words = fields.Char(string=u'北纬', default='待提交', required=True)
    Elevation_words = fields.Char(string=u'海拔高程', default='待提交', required=True)
    Relative_height_difference_words = fields.Char(string=u'相对高差', default='待提交', required=True)

    Turbine_number_words = fields.Char(string=u'机组数量', default="待提交", readonly=True)  ######################
    Farm_capacity_words = fields.Char(string=u'装机容量', default="待提交", readonly=True)  ######################
    Hour_words = fields.Char(string=u'满发小时', default="待提交", readonly=True)

    ongrid_power = fields.Char(u'上网电量', default="待提交", readonly=True)
    weak = fields.Char(u'尾流衰减', default="待提交")
    PWDLevel = fields.Char(u'风功率密度等级', default="待提交", readonly=True)

    main_wind_direction = fields.Char(u'主风向', default="待提交", readonly=True)
    summary_txt = fields.Char(u'概述', default="待提交", required=True)

    max_wind_txt = fields.Char(u'50年一遇最大风速', default="待提交", readonly=True)

    cft_name_words = fields.Char(string=u'测风塔名字', default="待提交", readonly=True)
    string_speed_words = fields.Char(string=u'风速信息', default="待提交", readonly=True)
    string_deg_words = fields.Char(string=u'风向信息', default="待提交", readonly=True)
    cft_number_words = fields.Char(string=u'测风塔数目', default="待提交", readonly=True)

    cft_TI_words = fields.Char(string=u'湍流信息', default="待提交", readonly=True)
    cft_time_words = fields.Char(string=u'选取时间段', default="待提交", readonly=True)

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
    road_1_num = fields.Char(u'改扩建进场道路', default="待提交", readonly=True)
    road_2_num = fields.Char(u'进站道路', default="待提交", readonly=True)
    road_3_num = fields.Char(u'新建施工检修道路', default="待提交", readonly=True)
    total_civil_length = fields.Float(u'道路工程长度', default="0", readonly=True)

    basic_type = fields.Char(u'基础形式', default="待提交", readonly=True)
    ultimate_load = fields.Char(u'极限载荷', default="待提交", readonly=True)
    fortification_intensity = fields.Char(u'设防烈度', default="待提交", readonly=True)
    temporary_land_area = fields.Char(u'临时用地面积（亩）', default="0", readonly=True)
    permanent_land_area = fields.Char(u'永久用地面积（亩）', default="0", readonly=True)
    TurbineCapacity = fields.Char(u'风机容量', default="0", readonly=True)  ######################
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

    BasicType = fields.Char(u'基础形式')
    FloorRadiusR = fields.Char(u'基础底面圆直径')
    H1 = fields.Char(u'基础底板外缘高度')
    R2 = fields.Char(u'台柱圆直径')
    H2 = fields.Char(u'基础底板圆台高度')
    H3 = fields.Char(u'台柱高度')

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

    Concrete_words = fields.Char(string=u'混凝土(万m³)', default='待提交')

    # 经评
    capital_rate_12 = fields.Char(string=u'资本金比例', readonly=True)

    static_investment_12 = fields.Char(string=u'静态总投资', readonly=True)
    construction_assistance = fields.Char(string=u'施工辅助工程', readonly=True)
    equipment_installation = fields.Char(string=u'设备及安装工程', readonly=True)
    constructional_engineering = fields.Char(string=u'建筑工程', readonly=True)
    other_expenses = fields.Char(string=u'其他费用', readonly=True)
    static_investment_unit = fields.Char(string=u'单位千瓦静态投资', readonly=True)

    domestic_bank_loan = fields.Char(string=u'国内银行贷款', readonly=True)
    interest_construction_loans_12 = fields.Char(string=u'建设期贷款利息', readonly=True)
    dynamic_investment_12 = fields.Char(string=u'动态总投资', readonly=True)
    dynamic_investment_unit = fields.Char(string=u'单位千瓦动态投资', readonly=True)

    static_investment_13 = fields.Char(string=u'静态总投资', readonly=True)
    static_investment_unit = fields.Char(string=u'单位千瓦静态投资', readonly=True)
    dynamic_investment_13 = fields.Char(string=u'动态总投资', readonly=True)
    dynamic_investment_unit = fields.Char(string=u'单位千瓦动态投资', readonly=True)
    Internal_financial_rate_before = fields.Char(string=u'税前财务收益率(%)', readonly=True)
    Internal_financial_rate_after = fields.Char(string=u'税后财务收益率(%)', readonly=True)
    Internal_financial_rate_capital = fields.Char(string=u'资本金税后收益率(%)', readonly=True)
    payback_period = fields.Char(string=u'投资回收期(年)', readonly=True)
    ROI_13 = fields.Char(string=u'总投资收益率(%)', readonly=True)
    ROE_13 = fields.Char(string=u'资本金利润率(%)', readonly=True)
    grid_price = fields.Char(string=u'上网电价', readonly=True)

    report_attachment_id_output1 = fields.Many2one('ir.attachment', string=u'可研报告章节-1')

    conservation_water_soil = fields.Char(string=u'水土保持费用（万元）', readonly=True)
    environmental_protection_investment = fields.Char(string=u'环境保护总投资（万元）')
    capacity_coefficient = fields.Char(string=u'容量系数')
    IECLevel = fields.Char(string=u'IEC等级', readonly=True)
    rotor_diameter_suggestion = fields.Char(string=u'叶轮直径')
    road_names = fields.Char(string=u'周边道路')
    land_area = fields.Char(string=u'总用地面积')
    farm_speed_range_words = fields.Char(string=u'平均风速区间')

    tower_weight = fields.Char(string=u'塔筒重量', default="待提交")
    Project_time_words = fields.Char(string=u'施工总工期', default='12')

    dict_1_word_post = fields.Char(string=u'字典1')

    dict_3_word_post = fields.Char(string=u'字典3')
    dict_4_word_post = fields.Char(string=u'字典4')

    dict_5_word_post = fields.Char(string=u'字典5')
    dict_8_word_post = fields.Char(string=u'字典8_9')
    dict_12_word_post = fields.Char(string=u'字典12')
    dict_13_word_post = fields.Char(string=u'字典13')

    Dict_12_Final = fields.Char(string=u'字典12')
    Dict_13_Final = fields.Char(string=u'字典13')

    dict_x = fields.Char(string=u'字典x')


    def merge_project(self):

        if self.Dict_12_Final==False:
            # raise ValidationError('验证错误信息!')
            raise exceptions.Warning('There are %d active tasks.' % self.Dict_12_Final)
        dict_x = dict_project_x(self)
        dict_12_final = eval(self.Dict_12_Final)
        print("dict_12_final")
        print(dict_12_final)
        dict_13_final = eval(self.Dict_13_Final)
        dict_x_all = dict(dict_x, **dict_12_final, **dict_13_final)
        chapter_number = 'x'
        project_path = self.env['auto_word.project'].project_path + str(chapter_number)
        suffix_in = ".xls"
        suffix_out = ".docx"
        name_first, file_second, name_second = "", "", ""
        outputfile = 'result_chapter' + str(chapter_number) + "_final" + suffix_out
        model_name = 'cr' + str(chapter_number) + "_final" + suffix_out
        # Pathinput = os.path.join(project_path, '%s') % inputfile
        Pathoutput = os.path.join(project_path, '%s') % outputfile

        generate_docx(dict_x_all, project_path, model_name, outputfile)

        # ###########################

        reportfile_name = open(file=Pathoutput, mode='rb')
        byte = reportfile_name.read()
        reportfile_name.close()
        if (str(self.report_attachment_id_output1) == 'ir.attachment()'):
            Attachments = self.env['ir.attachment']
            print('开始创建新纪录1')
            New = Attachments.create({
                'name': self.project_name + '可研报告章节chapter' + str(chapter_number) + '下载页',
                'datas_fname': self.project_name + '可研报告章节chapter' + str(chapter_number) + '.docx',
                'datas': base64.standard_b64encode(byte),
                'display_name': self.project_name + '可研报告章节',
                'create_date': fields.date.today(),
                'public': True,  # 此处需设置为true 否则attachments.read  读不到
            })
            print('已创建新纪录：', New)
            print('new dataslen：', len(New.datas))
            self.report_attachment_id_output1 = New
        else:
            self.report_attachment_id_output1.datas = base64.standard_b64encode(byte)

        return True

    def button_project(self):
        self.dict_1_word_post = dict_project_1(self)

        return True


class auto_word_null_project(models.Model):
    _name = 'auto_word_null.project'
    _description = 'null Project'
