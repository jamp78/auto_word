# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
import doc_5
from . import auto_word_electrical
from . import auto_word_civil


class auto_word_wind(models.Model):
    _name = 'auto_word.wind'
    _description = 'Wind energy input'
    _rec_name = 'project_id'
    project_id = fields.Many2one('auto_word.project', string=u'项目名', required=True)
    version_id = fields.Char(u'版本', required=True, default="1.0")
    turbine_numbers = fields.Integer(u'机位数', required=True)
    generator_ids = fields.Many2many('auto_word_wind.turbines', required=True, string=u'比选机型')
    report_attachment_id = fields.Many2one('ir.attachment', string=u'可研报告风能章节')
    Dict_5 = {}

    # project_res= fields.Many2many('auto_word.windres', string=u'机位结果', required=True)

    @api.multi
    def button_wind(self):
        projectname = self.project_id
        myself = self
        projectname.wind_attachment_id = myself
        projectname.wind_attachment_ok = u"已提交,版本：" + self.version_id
        projectname.turbine_numbers_wind = self.turbine_numbers

        return True

    @api.multi
    def wind_generate(self):
        tur_name = []
        for i in range(0, len(self.generator_ids)):
            tur_name.append(self.generator_ids[i].name_tur)
        path_images = r"D:\GOdoo12_community\myaddons\auto_word\models\source\chapter_5"

        self.Dict_5 = doc_5.generate_wind_docx(tur_name, path_images)
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
    capacity = fields.Float(u'额定功率(kW)', required=True)
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


class auto_word_wind_turbines_compare(models.Model):
    _inherit = 'auto_word.wind'
    _name = 'auto_word_wind_turbines.compare'
    _description = 'turbines_compare'

    mixed_turbines_bool = fields.Boolean(string=u'是否为混排方案',
                                         help='若是混排方案请勾选')

    generator_id = fields.Many2one('auto_word_wind.turbines', required=True, string=u'风机型号')
    installed_capacity = fields.Float(compute='_compute_installed_capacity', string=u'装机容量')
    hub_height = fields.Char(compute='_compute_turbine', string=u'塔筒高度')
    turbine_numbers = fields.Char(string=u'风机数量')
    capacity = fields.Char(compute='_compute_turbine', string=u'风机容量')
    tower_weight = fields.Char(compute='_compute_turbine', string=u'塔筒重量')
    rotor_diameter = fields.Char(compute='_compute_turbine', string=u'叶轮直径')

    power_generation = fields.Float(u'上网电量', required=True)
    weak = fields.Float(u'尾流衰减', required=True)
    power_hours = fields.Float(u'满发小时', required=True)
    investment_turbines_kw = fields.Float(u'风机kw投资', required=True)

    TerrainType_turbines_compare = fields.Selection(
        [("平原", u"平原"), ("丘陵", u"丘陵"), ("山地", u"山地")], string=u"山地类型", required=True)

    investment_e1 = fields.Float(compute='_compute_investment_e1', string=u'塔筒投资')
    investment_e2 = fields.Float(compute='_compute_investment_e2', string=u'风机设备投资')
    investment_e3 = fields.Float(string=u'基础投资', readonly=True)
    investment_e4 = fields.Float(string=u'道路投资', readonly=True, compute='_compute_investment_e4')
    investment_e5 = fields.Float(string=u'吊装费用', readonly=True, compute='_compute_investment_e5')
    investment_e6 = fields.Float(string=u'箱变投资', readonly=True, compute='_compute_investment_e6')
    investment_e7 = fields.Float(string=u'集电线路', readonly=True, compute='_compute_investment_e7')

    investment = fields.Float(string=u'发电部分投资', readonly=True, compute='_compute_investment')
    investment_unit = fields.Float(string=u'单位度电投资', readonly=True, compute='_compute_investment_unit')

    @api.one
    @api.depends("generator_id", "project_id")
    def _compute_turbine(self):
        self.hub_height = self.generator_id.hub_height
        self.turbine_numbers = self.project_id.turbine_numbers_wind
        self.capacity = self.generator_id.capacity
        self.tower_weight = self.generator_id.tower_weight
        self.rotor_diameter = self.generator_id.rotor_diameter

    def _compute_installed_capacity(self):
        for re in self:
            if re.mixed_turbines_bool:
                re.installed_capacity = int(self.turbine_numbers) * float(self.capacity)
            else:
                re.installed_capacity = int(self.turbine_numbers) * float(self.capacity) + 1
    # def _compute_investment_e1(self):
    #     for re in self:
    #         re.investment_e1 = auto_word_wind.turbine_numbers * re.generator_id.tower_weight * 1.05
    #
    # @api.depends('installed_capacity', 'investment_turbines_kw')
    # def _compute_investment_e2(self):
    #     for re in self:
    #         re.investment_e1 = re.installed_capacity * re.investment_turbines_kw * 1000 / 10000
    #
    # @api.depends('TerrainType_turbines_compare')
    # def _compute_investment_e4(self):
    #     for re in self:
    #         if re.TerrainType_turbines_compare == "平原":
    #             re.investment_e4 = auto_word_civil.auto_word_civil.total_civil_length * 50
    #
    #         elif re.TerrainType_turbines_compare == "丘陵":
    #             re.investment_e4 = auto_word_civil.auto_word_civil.total_civil_length * 80
    #
    #         elif re.TerrainType_turbines_compare == "山地":
    #             re.investment_e4 = auto_word_civil.auto_word_civil.total_civil_length * 140
    #
    # def _compute_investment_e5(self):
    #     for re in self:
    #         if re.hub_height <= 90:
    #             re.investment_e4 = auto_word_wind.turbine_numbers * 38
    #
    #         elif 90 < re.hub_height <= 100:
    #             re.investment_e4 = auto_word_wind.turbine_numbers * 45
    #
    #         elif 100 < re.hub_height <= 120:
    #             re.investment_e4 = auto_word_wind.turbine_numbers * 55
    #
    #         elif 120 < re.hub_height <= 140:
    #             re.investment_e4 = auto_word_wind.turbine_numbers * 65
    #
    # def _compute_investment_e6(self):
    #     for re in self:
    #         if re.generator_id.capacity <= 2000:
    #             re.investment_e4 = auto_word_wind.turbine_numbers * 23
    #
    #         elif 2000 < re.generator_id.capacity <= 2200:
    #             re.investment_e4 = auto_word_wind.turbine_numbers * 25
    #
    #         elif 2200 < re.generator_id.capacity <= 2500:
    #             re.investment_e4 = auto_word_wind.turbine_numbers * 28
    #
    #         elif 2500 < re.generator_id.capacity <= 4000:
    #             re.investment_e4 = auto_word_wind.turbine_numbers * 32
    #
    # @api.depends('TerrainType_turbines_compare')
    # def _compute_investment_e7(self):
    #     for re in self:
    #         re.investment_e7 = auto_word_electrical.auto_word_electrical.length_single_jL240 * 50
    #
    # @api.depends('investment_e1', 'investment_e2', 'investment_e3', 'investment_e4', 'investment_e5', 'investment_e6',
    #              'investment_e7')
    # def _compute_investment(self):
    #     for re in self:
    #         re.investment = re.investment_e1 + re.investment_e2 + re.investment_e3 + re.investment_e4 + \
    #                         re.investment_e5 + re.investment_e6 + re.investment_e7
    #
    # @api.depends('investment')
    # def _compute_investment(self):
    #     for re in self:
    #         re.investment_unit = re.investment / re.power_generation * 10
