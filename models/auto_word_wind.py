# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
import doc_5
from . import auto_word_electrical
from . import auto_word_civil
from . import auto_word_wind_cft


class auto_word_wind(models.Model):
    _name = 'auto_word.wind'
    _description = 'Wind energy input'
    _rec_name = 'project_id'
    project_id = fields.Many2one('auto_word.project', string=u'项目名', required=True)
    version_id = fields.Char(u'版本', required=True, default="1.0")
    turbine_numbers = fields.Integer(string=u'机位数', readonly=True, compute='_compute_turbine_numbers')
    farm_capacity = fields.Float(string=u'风电场容量', readonly=True, compute='_compute_turbine_numbers')
    generator_ids = fields.Many2many('auto_word_wind.turbines', required=True, string=u'比选机型')

    select_ids = fields.Many2many('wind_turbines.selection', required=True, string=u'机型推荐')
    report_attachment_id = fields.Many2one('ir.attachment', string=u'可研报告风能章节')

    select_hub_height = fields.Integer(u'推荐轮毂高度', required=True)
    rotor_diameter = fields.Char(string=u'叶轮直径', default="待提交")

    string_speed_words = fields.Char(string=u'测风塔选定风速结果', default="待提交")
    string_deg_words = fields.Char(string=u'测风塔选定风向结果', default="待提交")
    cft_name_words = fields.Char(string=u'测风塔名字', default="待提交")

    IECLevel = fields.Selection([("IA", u"IA"), ("IIA", u"IIA"), ("IIIA", u"IIIA"),
                                 ("IB", u"IB"), ("IIB", u"IIB"), ("IIIB", u"IIIB"),
                                 ("IC", u"IC"), ("IIC", u"IIC"), ("IIIC", u"IIIC"),
                                 ], string=u"IEC等级", default="IIIB")

    farm_elevation = fields.Char(string=u'海拔高程', default="待提交")
    farm_area = fields.Char(string=u'区域面积', default="待提交")
    farm_speed_range = fields.Char(string=u'风速区间', default="待提交")

    rotor_diameter = fields.Char(string=u'叶轮直径', default="待提交")
    case_number = fields.Char(string=u'方案数', default="待提交")

    @api.depends('select_ids')
    def _compute_turbine_numbers(self):
        self.turbine_numbers = 0
        self.farm_capacity = 0
        for i in range(0, len(self.select_ids)):
            self.turbine_numbers = self.select_ids[i].turbine_numbers + self.turbine_numbers
            self.farm_capacity = self.select_ids[i].turbine_numbers * self.select_ids[i].capacity + self.farm_capacity
        self.farm_capacity = self.farm_capacity / 1000

    # project_res= fields.Many2many('auto_word.windres', string=u'机位结果', required=True)

    @api.multi
    def button_wind(self):
        projectname = self.project_id
        myself = self
        projectname.wind_attachment_id = myself
        projectname.wind_attachment_ok = u"已提交,版本：" + self.version_id
        projectname.turbine_numbers = self.turbine_numbers
        projectname.select_hub_height = self.select_hub_height
        return True

    @api.multi
    def wind_generate(self):
        tur_name = []
        for i in range(0, len(self.generator_ids)):
            tur_name.append(self.generator_ids[i].name_tur)
        path_images = r"D:\GOdoo12_community\myaddons\auto_word\models\source\chapter_5"

        dict5 = doc_5.generate_wind_dict(tur_name, path_images)
        dict_5_word = {
            "叶轮直径": self.rotor_diameter,
            "方案数": self.case_number,
            "海拔高程": self.farm_elevation,
            "区域面积": self.farm_area,
            "平均风速区间": self.farm_speed_range,
            '测风塔名字': self.cft_name_words,
            '测风塔风速信息': self.string_speed_words,
            '测风塔风向信息': self.string_deg_words,
            '推荐轮毂高度': self.select_hub_height,
            'IEC等级': self.IECLevel,
        }
        Dict5 = dict(dict_5_word, **dict5)
        print(Dict5)
        doc_5.generate_wind_docx(Dict5, path_images)
        ###########################

        reportfile_name = open(
            file=r'D:\GOdoo12_community\myaddons\auto_word\models\source\chapter_5\result_chapter5.docx',
            mode='rb')
        byte = reportfile_name.read()
        reportfile_name.close()
        print('file lenth=', len(byte))
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
        return True


class outputcurve(models.Model):
    _name = 'auto_word_wind_turbines.power'
    _description = 'Generator outputcurve'
    _rec_name = 'name_power'
    name_power = fields.Char(u'风机型号', required=True)
    speed2p5 = fields.Float(u'2.5m/s（kW）', required=True)
    speed3 = fields.Float(u'3m/s（kW）', required=True)
    speed4 = fields.Float(u'4m/s（kW）', required=True)
    speed5 = fields.Float(u'5m/s（kW）', required=True)
    speed6 = fields.Float(u'6m/s（kW）', required=True)
    speed7 = fields.Float(u'7m/s（kW）', required=True)
    speed8 = fields.Float(u'8m/s（kW）', required=True)
    speed9 = fields.Float(u'9m/s（kW）', required=True)
    speed10 = fields.Float(u'10m/s（kW）', required=True)
    speed11 = fields.Float(u'11m/s（kW）', required=True)
    speed12 = fields.Float(u'12m/s（kW）', required=True)
    speed13 = fields.Float(u'13m/s（kW）', required=True)
    speed14 = fields.Float(u'14m/s（kW）', required=True)
    speed15 = fields.Float(u'15m/s（kW）', required=True)
    speed16 = fields.Float(u'16m/s（kW）', required=True)
    speed17 = fields.Float(u'17m/s（kW）', required=True)
    speed18 = fields.Float(u'18m/s（kW）', required=True)
    speed19 = fields.Float(u'19m/s（kW）', required=True)
    speed20 = fields.Float(u'20m/s（kW）', required=True)
    speed21 = fields.Float(u'21m/s（kW）', required=True)
    speed22 = fields.Float(u'22m/s（kW）', required=True)
    speed23 = fields.Float(u'23m/s（kW）', required=True)
    speed24 = fields.Float(u'24m/s（kW）', required=True)
    speed25 = fields.Float(u'25m/s（kW）', required=True)


class auto_word_wind_turbines_efficiency(models.Model):
    _name = 'auto_word_wind_turbines.efficiency'
    _description = 'Generator efficiency'
    _rec_name = 'name_efficiency'
    name_efficiency = fields.Char(u'风机型号', required=True)
    speed2p5 = fields.Float(u'2.5m/s（kW）', required=True)
    speed3 = fields.Float(u'3m/s（kW）', required=True)
    speed4 = fields.Float(u'4m/s（kW）', required=True)
    speed5 = fields.Float(u'5m/s（kW）', required=True)
    speed6 = fields.Float(u'6m/s（kW）', required=True)
    speed7 = fields.Float(u'7m/s（kW）', required=True)
    speed8 = fields.Float(u'8m/s（kW）', required=True)
    speed9 = fields.Float(u'9m/s（kW）', required=True)
    speed10 = fields.Float(u'10m/s（kW）', required=True)
    speed11 = fields.Float(u'11m/s（kW）', required=True)
    speed12 = fields.Float(u'12m/s（kW）', required=True)
    speed13 = fields.Float(u'13m/s（kW）', required=True)
    speed14 = fields.Float(u'14m/s（kW）', required=True)
    speed15 = fields.Float(u'15m/s（kW）', required=True)
    speed16 = fields.Float(u'16m/s（kW）', required=True)
    speed17 = fields.Float(u'17m/s（kW）', required=True)
    speed18 = fields.Float(u'18m/s（kW）', required=True)
    speed19 = fields.Float(u'19m/s（kW）', required=True)
    speed20 = fields.Float(u'20m/s（kW）', required=True)
    speed21 = fields.Float(u'21m/s（kW）', required=True)
    speed22 = fields.Float(u'22m/s（kW）', required=True)
    speed23 = fields.Float(u'23m/s（kW）', required=True)
    speed24 = fields.Float(u'24m/s（kW）', required=True)
    speed25 = fields.Float(u'25m/s（kW）', required=True)


class auto_word_wind_turbines(models.Model):
    _name = 'auto_word_wind.turbines'
    _description = 'Generator'
    _rec_name = 'name_tur'
    name_tur = fields.Char(u'风机型号', required=True)
    capacity = fields.Integer(u'额定功率(kW)', required=True)
    blade_number = fields.Integer(u'叶片数', required=True)
    rotor_diameter = fields.Float(u'叶轮直径', required=True)
    rotor_swept_area = fields.Float(u'扫风面积', required=True)
    hub_height = fields.Char(u'轮毂高度')
    power_regulation = fields.Char(u'风机类型', required=True)
    cut_in_wind_speed = fields.Float(u'切入风速', required=True)
    cut_out_wind_speed = fields.Float(u'切出风速', required=True)
    rated_wind_speed = fields.Float(u'额定风速', required=True)
    generator_type = fields.Char(u'发电机类型', required=True)
    rated_power = fields.Float(u'额定功率')
    voltage = fields.Float(u'额定电压', required=True)
    frequency = fields.Float(u'频率', required=True)
    tower_type = fields.Char(u'塔筒类型')
    tower_weight = fields.Float(u'塔筒重量')
    pneumatic_brake = fields.Char(u'安全制动类型')
    mechanical_brake = fields.Char(u'机械制动类型')
    three_second_maximum = fields.Char(u'生存风速', required=True)


# 推荐机组
class auto_word_wind_turbines_selection(models.Model):
    _name = 'wind_turbines.selection'
    _description = 'Generator'
    _rec_name = 'name_tur'
    _inherit = ['auto_word_wind.turbines']
    name_tur = fields.Char(u'风机型号')
    turbine_numbers = fields.Integer(u'机位数', required=True)
    capacity = fields.Integer(u'额定功率(kW)', readonly=False)
    blade_number = fields.Integer(u'叶片数', readonly=False)
    rotor_diameter = fields.Float(u'叶轮直径', readonly=False)
    rotor_swept_area = fields.Float(u'扫风面积', readonly=False)
    hub_height = fields.Char(u'轮毂高度', readonly=False)
    power_regulation = fields.Char(u'风机类型', readonly=False)
    cut_in_wind_speed = fields.Float(u'切入风速', readonly=False)
    cut_out_wind_speed = fields.Float(u'切出风速', readonly=False)
    rated_wind_speed = fields.Float(u'额定风速', readonly=False)
    generator_type = fields.Char(u'发电机类型', readonly=False)
    rated_power = fields.Float(u'额定功率', readonly=False)
    voltage = fields.Float(u'额定电压', readonly=False)
    frequency = fields.Float(u'频率', readonly=False)
    tower_type = fields.Char(u'塔筒类型', readonly=False)
    tower_weight = fields.Float(u'塔筒重量', readonly=False)
    pneumatic_brake = fields.Char(u'安全制动类型', readonly=False)
    mechanical_brake = fields.Char(u'机械制动类型', readonly=False)
    three_second_maximum = fields.Char(u'生存风速', readonly=False)

    investment_turbines_kw = fields.Float(u'风机kw投资', required=True)
    case_hub_height = fields.Integer(u'采用轮毂高度', required=True)


class windres(models.Model):
    _name = 'auto_word.windres'
    _description = 'Wind energy result input'
    _rec_name = 'tur_id'

    Turbine = fields.Char(u'风力发电机(kW)')
    tur_id = fields.Char(u'风机编号', required=True)
    X = fields.Float(u'X', required=True)
    Y = fields.Float(u'Y', required=True)
    Z = fields.Float(u'Z', required=True)
    H = fields.Float(u'轮毂高度', required=True)
    Latitude = fields.Float(u'经度', required=True)
    Longitude = fields.Float(u'纬度', required=True)
    TrustCoefficient = fields.Char(u'信任系数')
    WeibullA = fields.Float(u'A')
    WeibullK = fields.Float(u'K')
    EnergyDensity = fields.Float(u'能量密度')
    PowerGeneration = fields.Float(u'发电量', required=True)
    PowerGeneration_Weak = fields.Float(u'考虑尾流效应的发电量', required=True)
    CapacityCoe = fields.Float(u'容量系数')
    AverageWindSpeed = fields.Float(u'平均风速')
    TurbulenceEnv_StrongWind = fields.Float(u'强风状态下的平均环境湍流强度')
    Turbulence_StrongWind = fields.Float(u'强风状态下的平均总体湍流强度', required=True)
    AverageWindSpeed_Weak = fields.Float(u'考虑尾流效应的平均风速', required=True)
    Weak = fields.Float(u'尾流效应导致的平均折减率', required=True)
    AirDensity = fields.Float(u'该点的空气密度')
    WindShear_Avg = fields.Float(u'平均风切变指数')
    WindShear_Max = fields.Float(u'最大风切变指数')
    WindShear_Max_Deg = fields.Float(u'最大风切变指数对应方向扇区')
    InflowAngle_Avg = fields.Float(u'绝对值平均入流角')
    InflowAngle_Max = fields.Float(u'最大入流角', required=True)
    InflowAngle_Max_Deg = fields.Float(u'出现最大入流角的风向扇区', required=True)
    NextTur = fields.Char(u' 最近相邻风机的标签', required=True)
    NextLength_M = fields.Char(u'相邻风机的最近距离')
    Diameter = fields.Char(u'叶轮直径')
    NextLength_D = fields.Char(u'以叶轮直径为单位的相邻风机最近距离')
    NextDeg = fields.Char(u'最近相邻风机的方位角')
    Sectors = fields.Char(u'扇区数量', required=True)


# 机型比选
class auto_word_wind_turbines_compare(models.Model):
    # _inherit = 'auto_word.wind'
    _name = 'auto_word_wind_turbines.compare'
    _description = 'turbines_compare'
    _rec_name = 'case_name'
    # mixed_turbines_bool = fields.Boolean(string=u'是否为混排方案',
    #                                      help='若是混排方案请勾选')
    project_id = fields.Many2one('auto_word.project', string=u'项目名', required=True)
    case_ids = fields.Many2many('wind_turbines.selection', string=u'比选方案')
    wind_ids = fields.Many2one('auto_word.wind', string=u'项目名')

    case_name = fields.Char(u'方案名称', required=True, default="方案1")
    turbine_numbers = fields.Char(string=u'风机数量', readonly=True, compute='_compute_turbine', default="待提交")
    farm_capacity = fields.Char(string=u'风机容量', readonly=True, compute='_compute_turbine', default="待提交")
    tower_weight = fields.Char(compute='_compute_turbine', string=u'塔筒重量', default="待提交")
    rotor_diameter = fields.Char(compute='_compute_turbine', string=u'叶轮直径', default="待提交")
    case_number = fields.Char(compute='_compute_turbine', string=u'方案数')

    power_generation = fields.Float(u'上网电量')
    weak = fields.Float(u'尾流衰减')
    power_hours = fields.Float(u'满发小时')

    TerrainType_turbines_compare = fields.Selection(
        [("平原", u"平原"), ("丘陵", u"丘陵"), ("山地", u"山地")], string=u"山地类型")

    investment_E1 = fields.Float(compute='_compute_turbine', string=u'塔筒投资(万元)')
    investment_E2 = fields.Float(compute='_compute_turbine', string=u'风机设备投资(万元)')
    investment_E3 = fields.Float(string=u'基础投资(万元)')
    investment_E4 = fields.Float(string=u'道路投资(万元)', readonly=True, compute='_compute_turbine')
    investment_E5 = fields.Float(string=u'吊装费用(万元)', readonly=True, compute='_compute_turbine')
    investment_E6 = fields.Float(string=u'箱变投资(万元)', readonly=True, compute='_compute_turbine')
    investment_E7 = fields.Float(string=u'集电线路(万元)', readonly=True, compute='_compute_turbine')

    investment_turbines_kws = fields.Char(u'风机kw投资', readonly=True, compute='_compute_turbine')
    case_hub_height = fields.Char(u'推荐轮毂高度', readonly=True, compute='_compute_turbine')

    investment = fields.Float(string=u'发电部分投资(万元)', readonly=True, compute='_compute_turbine')
    investment_unit = fields.Float(string=u'单位度电投资', readonly=True, compute='_compute_turbine')

    @api.depends('case_ids', 'TerrainType_turbines_compare')
    def _compute_turbine(self):
        self.turbine_numbers = 0
        self.farm_capacity, investment_e1_sum, investment_e2_sum = 0, 0, 0
        investment_e5_sum, investment_e6_sum = 0, 0

        tower_weight_word, tower_weight_words = '', ''
        rotor_diameter_word, rotor_diameter_words = '', ''
        investment_turbines_kw_word, investment_turbines_kw_words = '', ''
        case_hub_height_word, case_hub_height_words = '', ''
        self.case_number=str(len(self.case_ids))
        for i in range(0, len(self.case_ids)):

            tower_weight_word = str(self.case_ids[i].tower_weight)
            rotor_diameter_word = str(self.case_ids[i].rotor_diameter)
            investment_turbines_kw_word = str(self.case_ids[i].investment_turbines_kw)
            case_hub_height_word = str(self.case_ids[i].case_hub_height)

            self.turbine_numbers = int(self.case_ids[i].turbine_numbers) + int(self.turbine_numbers)
            self.farm_capacity = int(self.case_ids[i].turbine_numbers) * int(self.case_ids[i].capacity) + int(
                self.farm_capacity)
            investment_e1 = self.case_ids[i].tower_weight * self.case_ids[i].turbine_numbers * 1.05
            investment_e1_sum = investment_e1_sum + investment_e1

            investment_e2 = int(self.case_ids[i].turbine_numbers) * int(self.case_ids[i].capacity) * int(
                self.case_ids[i].investment_turbines_kw) / 10000
            investment_e2_sum = investment_e2_sum + investment_e2

            if self.case_ids[i].case_hub_height <= 90:
                investment_e5 = self.case_ids[i].turbine_numbers * 38
            elif 90 < self.case_ids[i].case_hub_height <= 100:
                investment_e5 = self.case_ids[i].turbine_numbers * 45
            elif 100 < self.case_ids[i].case_hub_height <= 120:
                investment_e5 = self.case_ids[i].turbine_numbers * 55
            elif 120 < self.case_ids[i].case_hub_height <= 140:
                investment_e5 = self.case_ids[i].turbine_numbers * 65

            if self.case_ids[i].capacity <= 2000:
                investment_e6 = self.case_ids[i].turbine_numbers * 23
            elif 2000 < self.case_ids[i].capacity <= 2200:
                investment_e6 = self.case_ids[i].turbine_numbers * 25
            elif 2200 < self.case_ids[i].capacity <= 2500:
                investment_e6 = self.case_ids[i].turbine_numbers * 28
            elif 2500 < self.case_ids[i].capacity <= 4000:
                investment_e6 = self.case_ids[i].turbine_numbers * 32

            investment_e5_sum = investment_e5_sum + investment_e5
            investment_e6_sum = investment_e6_sum + investment_e6
            if i != len(self.case_ids) - 1:
                tower_weight_words = tower_weight_word + "/" + tower_weight_words
                rotor_diameter_words = rotor_diameter_word + "/" + rotor_diameter_words
                investment_turbines_kw_words = investment_turbines_kw_word + "/" + investment_turbines_kw_words
                case_hub_height_words = case_hub_height_word + "/" + case_hub_height_words

            else:
                tower_weight_words = tower_weight_words + tower_weight_word
                rotor_diameter_words = rotor_diameter_words + rotor_diameter_word
                investment_turbines_kw_words = investment_turbines_kw_words + investment_turbines_kw_word
                case_hub_height_words = case_hub_height_words + case_hub_height_word

        self.tower_weight = tower_weight_words
        self.rotor_diameter = rotor_diameter_words
        self.investment_turbines_kws = investment_turbines_kw_words
        self.case_hub_height = case_hub_height_words

        self.farm_capacity = int(self.farm_capacity) / 1000
        self.investment_E1 = investment_e1_sum
        self.investment_E2 = investment_e2_sum

        if self.TerrainType_turbines_compare == "平原":
            self.investment_E4 = float(self.project_id.total_civil_length) * 50
        elif self.TerrainType_turbines_compare == "丘陵":
            self.investment_E4 = float(self.project_id.total_civil_length) * 80
        elif self.TerrainType_turbines_compare == "山地":
            self.investment_E4 = float(self.project_id.total_civil_length) * 140

        self.investment_E5 = investment_e5_sum
        self.investment_E6 = investment_e6_sum
        self.investment_E7 = float(self.project_id.jidian_air_wind) * 40 + float(self.project_id.jidian_cable_wind) * 50

        self.investment = self.investment_E1 + self.investment_E2 + self.investment_E3 + self.investment_E4 + \
                          self.investment_E5 + self.investment_E6 + self.investment_E7

        self.investment_unit = self.investment / self.power_generation * 10

    def wind_turbines_compare_form_refresh(self):
        for re in self:
            re.wind_ids.rotor_diameter = re.rotor_diameter
            re.wind_ids.case_number = re.case_number

