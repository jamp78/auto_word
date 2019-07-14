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
    rate = fields.Float(string=u'折减率', readonly=False)
    ongrid_power = fields.Float(string=u'上网电量', readonly=False)
    hours_year = fields.Float(string=u'年发电小时数', readonly=False)


class auto_word_wind_res_form(models.Model):
    _name = 'auto_word_wind_res.form'
    _description = 'auto_word_wind_res_form'
    _rec_name = 'project_id'
    _inherit = ['auto_word_wind.res']
    project_id = fields.Many2one('auto_word.project', string=u'项目名', required=False)
    # content_id = fields.Many2one('auto_word.wind', string=u'章节分类', required=False)
    compare_id = fields.Many2one('auto_word_wind_turbines.compare', string=u'章节分类', required=True)
    auto_word_wind_res = fields.Many2many('auto_word_wind.res', string=u'机位结果', required=True)
    rate = fields.Float(string=u'折减率', readonly=False)
    note = fields.Char(string=u'备注', readonly=False)

    @api.multi
    def wind_res_submit(self):
        for re in self.auto_word_wind_res:
            if re.rate != 0:
                re.ongrid_power = float(re.PowerGeneration_Weak) * re.rate
                re.hours_year = float(re.PowerGeneration_Weak) * re.rate / re.turbine_capacity_each * 1000
            else:
                re.ongrid_power = float(re.PowerGeneration_Weak) * self.rate
                re.hours_year = float(re.PowerGeneration_Weak) * self.rate / re.turbine_capacity_each * 1000

        if self.rate != 0:
            self.project_id.rate = self.rate*100
        else:
            self.project_id.rate = self.auto_word_wind_res[0].rate*100

        self.project_id.note = self.note

        re.ongrid_power = re.compare_id.ongrid_power
        re.weak = re.compare_id.weak
        re.hours_year = re.compare_id.hours_year

