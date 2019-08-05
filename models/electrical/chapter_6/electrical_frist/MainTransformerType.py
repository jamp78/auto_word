import math
import pandas as pd
from connect_sql import connect_sql_pandas
import numpy as np


# from docxtpl import DocxTemplate
# from RoundUp import round_dict_numbers

# 3主变压器
class MainTransformerType:

    def __init__(self):
        # ===========selecting parameters=============
        self.TypeID = 0
        # ===========basic parameters==============
        self.DataMainTransformerType = pd.DataFrame()
        self.TypeName, self.RatedCapacity, self.RatedVoltageRatio = "", 0, ""
        self.WiringGroup, self.ImpedanceVoltage, self.Noise = "", "", ""
        self.CoolingType, self.OnloadTapChanger, self.MTGroundingMode = "", "", ""
        self.TransformerRatedVoltage, self.TransformerNPC, self.ZincOxideArrester = "", "", ""
        self.DischargingGap, self.CurrentTransformer = "", ""

        # ===========Calculated parameters==============
        # self.earth_excavation_wind_resource, self.stone_excavation_wind_resource = 0, 0
        # self.earth_work_back_fill_wind_resource, self.earth_excavation_wind_resource_numbers = 0, 0
        # self.stone_excavation_wind_resource_numbers, self.earth_work_back_fill_wind_resource_numbers = 0, 0
        # self.c40_wind_resource_numbers, self.c15_wind_resource_numbers, self.c80_wind_resource_numbers = 0, 0, 0
        # self.c80_wind_resource_numbers, self.reinforcement_wind_resource_numbers = 0, 0

    def extraction_data_MainTransformerType_resource(self, TypeID):
        self.TypeID = TypeID

        sql = "SELECT * FROM auto_word_electrical_maintransformertype"
        self.DataMainTransformerType = connect_sql_pandas(sql)
        self.DataMainTransformerType = \
            self.DataMainTransformerType.loc[
                self.DataMainTransformerType['TypeID'] == self.TypeID]
        return self.DataMainTransformerType

    def excavation_cal_BoxVoltageType_resource(self, DataBoxVoltageType, basic_earthwork_ratio, basic_stone_ratio,
                                               turbine_num):
        self.DataBoxVoltageType = DataBoxVoltageType
        self.basic_earthwork_ratio = basic_earthwork_ratio
        self.basic_stone_ratio = basic_stone_ratio
        self.turbine_numbers = turbine_num

        self.earth_excavation_wind_resource = \
            math.pi * (self.DataBoxVoltageType['FloorRadiusR'] + 1.3) ** 2 * \
            (self.DataBoxVoltageType['H1'] + self.DataBoxVoltageType['H2'] + self.DataBoxVoltageType['H3'] + 0.15) \
            * self.basic_earthwork_ratio

        self.stone_excavation_wind_resource = \
            math.pi * (self.DataBoxVoltageType['FloorRadiusR'] + 1.3) ** 2 * \
            (self.DataBoxVoltageType['H1'] + self.DataBoxVoltageType['H2'] + self.DataBoxVoltageType['H3'] + 0.15) \
            * self.basic_stone_ratio

        self.earth_work_back_fill_wind_resource = \
            self.earth_excavation_wind_resource + self.stone_excavation_wind_resource - \
            self.DataBoxVoltageType['Volume'] - self.DataBoxVoltageType['Cushion']

        self.stone_excavation_wind_resource_numbers = self.stone_excavation_wind_resource * int(self.turbine_numbers)
        self.earth_excavation_wind_resource_numbers = self.earth_excavation_wind_resource * self.turbine_numbers
        self.earth_work_back_fill_wind_resource_numbers = self.earth_work_back_fill_wind_resource * self.turbine_numbers

        print(self.DataBoxVoltageType.at[self.DataBoxVoltageType.index[0], 'Volume'])
        print(self.turbine_numbers)
        self.c40_wind_resource_numbers = \
            self.DataBoxVoltageType.at[self.DataBoxVoltageType.index[0], 'Volume'] * self.turbine_numbers
        self.c15_wind_resource_numbers = \
            self.DataBoxVoltageType.at[self.DataBoxVoltageType.index[0], 'Cushion'] * self.turbine_numbers
        self.c80_wind_resource_numbers = \
            self.DataBoxVoltageType.at[self.DataBoxVoltageType.index[0], 'C80SecondaryGrouting'] * \
            self.turbine_numbers
        self.DataBoxVoltageType['EarthExcavation_WindResource'] = self.earth_excavation_wind_resource
        self.DataBoxVoltageType['StoneExcavation_WindResource'] = self.stone_excavation_wind_resource
        self.DataBoxVoltageType['EarthWorkBackFill_WindResource'] = self.earth_work_back_fill_wind_resource
        self.DataBoxVoltageType['Reinforcement'] = self.DataBoxVoltageType['Volume'] * 0.1
        self.reinforcement_wind_resource_numbers = \
            self.DataBoxVoltageType.at[self.DataBoxVoltageType.index[0], 'Reinforcement'] * self.turbine_numbers

        return self.DataBoxVoltageType

    def generate_dict_MainTransformerType_resource(self, data, num):
        self.DataMainTransformerType = data
        self.numbers = num
        self.TypeName = self.DataMainTransformerType.at[self.DataMainTransformerType.index[0], 'TypeName']
        self.RatedCapacity = self.DataMainTransformerType.at[self.DataMainTransformerType.index[0], 'RatedCapacity']
        self.RatedVoltageRatio = self.DataMainTransformerType.at[self.DataMainTransformerType.index[0], 'RatedVoltageRatio']
        self.WiringGroup = self.DataMainTransformerType.at[self.DataMainTransformerType.index[0], 'WiringGroup']
        self.ImpedanceVoltage = self.DataMainTransformerType.at[self.DataMainTransformerType.index[0], 'ImpedanceVoltage']
        self.Noise = self.DataMainTransformerType.at[self.DataMainTransformerType.index[0], 'Noise']

        self.CoolingType = self.DataMainTransformerType.at[self.DataMainTransformerType.index[0], 'CoolingType']
        self.OnloadTapChanger = self.DataMainTransformerType.at[self.DataMainTransformerType.index[0], 'OnloadTapChanger']
        self.MTGroundingMode = self.DataMainTransformerType.at[self.DataMainTransformerType.index[0], 'MTGroundingMode']
        self.TransformerRatedVoltage = self.DataMainTransformerType.at[self.DataMainTransformerType.index[0], 'TransformerRatedVoltage']
        self.TransformerNPC = self.DataMainTransformerType.at[self.DataMainTransformerType.index[0], 'TransformerNPC']
        self.ZincOxideArrester = self.DataMainTransformerType.at[self.DataMainTransformerType.index[0], 'ZincOxideArrester']
        self.DischargingGap = self.DataMainTransformerType.at[self.DataMainTransformerType.index[0], 'DischargingGap']
        self.CurrentTransformer = self.DataMainTransformerType.at[self.DataMainTransformerType.index[0], 'CurrentTransformer']

        self.dict_MainTransformerType_resource = {
            'numbers_主变压器': int(self.numbers),
            '型号_主变压器': self.TypeName,
            '额定容量_主变压器': self.RatedCapacity,
            '额定电压比_主变压器': self.RatedVoltageRatio,
            '接线组别_主变压器': self.WiringGroup,
            '阻抗电压_主变压器': self.ImpedanceVoltage,
            '噪音_主变压器': self.Noise,
            '冷却方式_主变压器': self.CoolingType,
            '有载调压开关_主变压器': self.OnloadTapChanger,
            '主变压器接地方式_主变压器': self.MTGroundingMode,
            '变压器额定电压_主变压器': self.TransformerRatedVoltage,
            '变压器中性点耐受电流_主变压器': self.TransformerNPC,
            '氧化锌避雷器_主变压器': self.ZincOxideArrester,
            '放电间隙_主变压器': self.DischargingGap,
            '电流互感器_主变压器': self.CurrentTransformer,
        }


        return self.dict_MainTransformerType_resource

# project01 = WindResourceDatabase()
# data = project01.extraction_DataBoxVoltageType(basic_type='扩展基础', ultimate_load=70000, fortification_intensity=7)
# turbine_numbers = 15
# data_cal = project01.excavation_cal_wind_resource(data,0.8, 0.2, turbine_numbers)
# dict_wind_resource = project01.generate_dict_wind_resource(data_cal, turbine_numbers)
# Dict = round_dict_numbers(dict_wind_resource, dict_wind_resource['numbers_tur'])
#
# docx_box = ['cr8', 'result_chapter8']
# save_path = r'C:\Users\Administrator\PycharmProjects\Odoo_addons_NB\autocrword\models\chapter_8'
# readpath = os.path.join(save_path, '%s.docx') % docx_box[0]
# savepath = os.path.join(save_path, '%s.docx') % docx_box[1]
# tpl = DocxTemplate(readpath)
# tpl.render(Dict)
# tpl.save(savepath)
