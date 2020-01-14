# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
from RoundUp import round_up, Get_Average, Get_Sum


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

    TurbineCapacity = fields.Float(string=u'风机容量', readonly=False)
    rate = fields.Float(string=u'折减率', readonly=False)
    ongrid_power = fields.Float(string=u'上网电量', readonly=False)
    hours_year = fields.Float(string=u'满发小时', readonly=False)


class auto_word_wind_res_form(models.Model):
    _name = 'auto_word_wind_res.form'
    _description = 'auto_word_wind_res_form'
    _rec_name = 'case_name'
    _inherit = ['auto_word_wind.res']
    project_id = fields.Many2one('auto_word.project', string=u'项目名', required=True)
    content_id = fields.Many2one('auto_word.wind', string=u'章节分类', required=True)

    # --------结果参数---------
    case_name = fields.Char(u'方案名称(结果)', required=True)
    auto_word_wind_res = fields.Many2many('auto_word_wind.res', string=u'机位结果', required=True)
    rate = fields.Float(string=u'折减率', readonly=False)
    note = fields.Char(string=u'备注', readonly=False)


    hub_height_calcuation = fields.Char(string=u'计算轮毂高度', readonly=True)
    ongrid_power_sum = fields.Char(u'上网电量', readonly=True)
    hours_year_average = fields.Char(u'满发小时', readonly=True)
    wake_average = fields.Char(u'尾流', readonly=True)
    capacity_coefficient = fields.Char(u'容量系数', readonly=True)

    @api.multi
    def wind_res_submit(self):

        for re in self:
            if re.rate != 0:
                re.content_id.rate = re.rate * 100
            else:
                re.content_id.rate = re.auto_word_wind_res[0].rate * 100

            re.content_id.note = re.note

            # re.env['auto_word_wind_turbines.compare'].compare_id = re
            # re.compare_id.case_name = re.auto_word_wind_res[0].case_name
            # re.compare_id.ongrid_power = re.ongrid_power_sum
            # re.compare_id.hours_year = re.hours_year_average

    @api.multi
    def wind_res_cal(self):
        for re in self:
            ongrid_power_list, hours_year_list, wake_list = [], [], []
            for vaule in re.auto_word_wind_res:
                print(vaule)
                if vaule.rate != 0:
                    re.rate=re.auto_word_wind_res[0].rate
                    vaule.ongrid_power = float(vaule.PowerGeneration_Weak) * vaule.rate
                    vaule.hours_year = float(
                        vaule.PowerGeneration_Weak) * vaule.rate / vaule.TurbineCapacity * 1000
                else:
                    vaule.ongrid_power = float(vaule.PowerGeneration_Weak) * re.rate
                    vaule.hours_year = float(vaule.PowerGeneration_Weak) * re.rate / vaule.TurbineCapacity * 1000

                print(vaule.hours_year)

                ongrid_power_list.append(vaule.ongrid_power)
                hours_year_list.append(vaule.hours_year)
                wake_list.append(float(vaule.Weak))

            re.ongrid_power_sum = round_up(Get_Sum(ongrid_power_list), 1)
            re.hours_year_average = round_up(Get_Average(hours_year_list), 1)
            re.wake_average = round_up(Get_Average(wake_list), 2)

            re.capacity_coefficient = round_up(float(re.hours_year_average) / 8760 * 100, 2)
            re.hub_height_calcuation = re.auto_word_wind_res[0].H