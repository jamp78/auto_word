# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64


# 功率曲线
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

# 风机效率
class auto_word_wind_turbines_efficiency(models.Model):
    _name = 'auto_word_wind_turbines.efficiency'
    _description = 'Generator efficiency'
    _rec_name = 'name_efficiency'
    name_efficiency = fields.Char(u'风机型号', required=True)
    speed2p5 = fields.Float(u'2.5m/s', required=True)
    speed3 = fields.Float(u'3m/s', required=True)
    speed4 = fields.Float(u'4m/s', required=True)
    speed5 = fields.Float(u'5m/s', required=True)
    speed6 = fields.Float(u'6m/s', required=True)
    speed7 = fields.Float(u'7m/s', required=True)
    speed8 = fields.Float(u'8m/s', required=True)
    speed9 = fields.Float(u'9m/s', required=True)
    speed10 = fields.Float(u'10m/s', required=True)
    speed11 = fields.Float(u'11m/s', required=True)
    speed12 = fields.Float(u'12m/s', required=True)
    speed13 = fields.Float(u'13m/s', required=True)
    speed14 = fields.Float(u'14m/s', required=True)
    speed15 = fields.Float(u'15m/s', required=True)
    speed16 = fields.Float(u'16m/s', required=True)
    speed17 = fields.Float(u'17m/s', required=True)
    speed18 = fields.Float(u'18m/s', required=True)
    speed19 = fields.Float(u'19m/s', required=True)
    speed20 = fields.Float(u'20m/s', required=True)
    speed21 = fields.Float(u'21m/s', required=True)
    speed22 = fields.Float(u'22m/s', required=True)
    speed23 = fields.Float(u'23m/s', required=True)
    speed24 = fields.Float(u'24m/s', required=True)
    speed25 = fields.Float(u'25m/s', required=True)

# 风机参数
class auto_word_wind_turbines(models.Model):
    _name = 'auto_word_wind.turbines'
    _description = 'Generator'
    _rec_name = 'name_tur'
    name_tur = fields.Char(u'风机型号')
    capacity = fields.Integer(u'额定功率(kW)')
    blade_number = fields.Integer(u'叶片数')
    rotor_diameter = fields.Float(u'叶轮直径')
    rotor_swept_area = fields.Float(u'扫风面积')
    hub_height = fields.Char(u'轮毂高度')
    power_regulation = fields.Char(u'风机类型')
    cut_in_wind_speed = fields.Float(u'切入风速')
    cut_out_wind_speed = fields.Float(u'切出风速')
    rated_wind_speed = fields.Float(u'额定风速')
    generator_type = fields.Char(u'发电机类型')
    rated_power = fields.Float(u'额定功率')
    voltage = fields.Float(u'额定电压')
    frequency = fields.Float(u'频率')
    tower_type = fields.Char(u'塔筒类型')
    tower_weight = fields.Float(u'塔筒重量')
    pneumatic_brake = fields.Char(u'安全制动类型')
    mechanical_brake = fields.Char(u'机械制动类型')
    three_second_maximum = fields.Char(u'生存风速')

# 推荐机组(只读)
class auto_word_wind_turbines_case(models.Model):
    _name = 'wind_turbines.case'
    _description = 'Generator'
    _rec_name = 'name_tur'
    _inherit = ['auto_word_wind.turbines']
    # name_tur = fields.Char(u'风机型号', readonly=False)
    # capacity = fields.Integer(u'额定功率(kW)', readonly=False)
    # blade_number = fields.Integer(u'叶片数', readonly=False)
    # rotor_diameter = fields.Float(u'叶轮直径', readonly=False)
    # rotor_swept_area = fields.Float(u'扫风面积', readonly=False)
    # hub_height = fields.Char(u'轮毂高度', readonly=False)
    # power_regulation = fields.Char(u'风机类型', readonly=False)
    # cut_in_wind_speed = fields.Float(u'切入风速', readonly=False)
    # cut_out_wind_speed = fields.Float(u'切出风速', readonly=False)
    # rated_wind_speed = fields.Float(u'额定风速', readonly=False)
    # generator_type = fields.Char(u'发电机类型', readonly=False)
    # rated_power = fields.Float(u'额定功率', readonly=False)
    # voltage = fields.Float(u'额定电压', readonly=False)
    # frequency = fields.Float(u'频率', readonly=False)
    # tower_type = fields.Char(u'塔筒类型', readonly=False)
    # tower_weight = fields.Float(u'塔筒重量', readonly=False)
    # pneumatic_brake = fields.Char(u'安全制动类型', readonly=False)
    # mechanical_brake = fields.Char(u'机械制动类型', readonly=False)
    # three_second_maximum = fields.Char(u'生存风速', readonly=False)

    turbine_numbers = fields.Integer(u'机位数')
    investment_turbines_kw = fields.Float(u'风机kw投资')


# 风能结果
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