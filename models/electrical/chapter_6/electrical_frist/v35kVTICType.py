import math
import pandas as pd
from connect_sql import connect_sql_pandas
import numpy as np


# from docxtpl import DocxTemplate
# from RoundUp import round_dict_numbers

# 5.1 35kV风机进线柜
class v35kVTICType:

    def __init__(self):
        # ===========selecting parameters=============
        self.TypeID = 0
        # ===========basic parameters==============
        self.Data35kVTICType = pd.DataFrame()
        self.TypeName, self.RatedVoltage, self.RatedCurrent = "", 0, ""
        self.RatedBreakingCurrent, self.DynamicCurrent, self.RatedShortTimeWCurrent = "", "", ""
        self.CurrentTransformerRatio, self.CurrentTransformerAccuracyClass, self.CurrentTransformerArrester = "", "", ""


        # ===========Calculated parameters==============
        # self.earth_excavation_wind_resource, self.stone_excavation_wind_resource = 0, 0
        # self.earth_work_back_fill_wind_resource, self.earth_excavation_wind_resource_numbers = 0, 0
        # self.stone_excavation_wind_resource_numbers, self.earth_work_back_fill_wind_resource_numbers = 0, 0
        # self.c40_wind_resource_numbers, self.c15_wind_resource_numbers, self.c80_wind_resource_numbers = 0, 0, 0
        # self.c80_wind_resource_numbers, self.reinforcement_wind_resource_numbers = 0, 0

    def extraction_data_35kVTICType_resource(self, TypeID):
        self.TypeID = TypeID

        sql = "SELECT * FROM auto_word_electrical_35kVTICType"
        self.Data35kVTICType = connect_sql_pandas(sql)
        self.Data35kVTICType = \
            self.Data35kVTICType.loc[
                self.Data35kVTICType['TypeID'] == self.TypeID]
        return self.Data35kVTICType

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

    def generate_dict_35kVTICType_resource(self, data, num):
        self.Data35kVTICType = data
        self.numbers = num
        self.TypeName = self.Data35kVTICType.at[self.Data35kVTICType.index[0], 'TypeName']
        self.RatedVoltage = self.Data35kVTICType.at[self.Data35kVTICType.index[0], 'RatedVoltage']
        self.RatedCurrent = self.Data35kVTICType.at[self.Data35kVTICType.index[0], 'RatedCurrent']
        self.RatedBreakingCurrent = self.Data35kVTICType.at[self.Data35kVTICType.index[0], 'RatedBreakingCurrent']
        self.DynamicCurrent = self.Data35kVTICType.at[self.Data35kVTICType.index[0], 'DynamicCurrent']
        self.RatedShortTimeWCurrent = self.Data35kVTICType.at[self.Data35kVTICType.index[0], 'RatedShortTimeWCurrent']

        self.CurrentTransformerRatio = self.Data35kVTICType.at[self.Data35kVTICType.index[0], 'CurrentTransformerRatio']
        self.CurrentTransformerAccuracyClass = self.Data35kVTICType.at[self.Data35kVTICType.index[0], 'CurrentTransformerAccuracyClass']
        self.CurrentTransformerArrester = self.Data35kVTICType.at[self.Data35kVTICType.index[0], 'CurrentTransformerArrester']
     
        self.dict_35kVTICType_resource = {
            'numbers_35kV风机进线柜': int(self.numbers),
            '型号_35kV风机进线柜': self.TypeName,
            '额定电压_35kV风机进线柜': self.RatedVoltage,
            '额定电流_35kV风机进线柜': self.RatedCurrent,
            '额定开断电流_35kV风机进线柜': self.RatedBreakingCurrent,
            '动稳定电流_35kV风机进线柜': self.DynamicCurrent,
            '额定短时耐受电流_35kV风机进线柜': self.RatedShortTimeWCurrent,
            '电流互感器变比_35kV风机进线柜': self.CurrentTransformerRatio,
            '电流互感器准确级_35kV风机进线柜': self.CurrentTransformerAccuracyClass,
            '电流互感器避雷器_35kV风机进线柜': self.CurrentTransformerArrester,
        }


        return self.dict_35kVTICType_resource

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
