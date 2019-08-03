import math
import pandas as pd
from connect_sql import connect_sql_pandas
import numpy as np


# from docxtpl import DocxTemplate
# from RoundUp import round_dict_numbers

# 4.1 110kV配电装置
class v110kVSwitChgearType:

    def __init__(self):
        # ===========selecting parameters=============
        self.TypeID = 0
        # ===========basic parameters==============
        self.Data110kVSwitChgearType = pd.DataFrame()
        self.TypeName, self.RatedVoltage, self.RatedCurrent = "", 0, ""
        self.RatedFrequency, self.RatedBreakingCurrent, self.RatedClosingCurrent = "", "", ""
        self.RatedPeakWCurrent, self.RatedShortTimeWCurrent, self.LineSpacing = "", "", ""
        self.PTSpacing, self.AccuracyClass = "", ""

        # ===========Calculated parameters==============
        # self.earth_excavation_wind_resource, self.stone_excavation_wind_resource = 0, 0
        # self.earth_work_back_fill_wind_resource, self.earth_excavation_wind_resource_numbers = 0, 0
        # self.stone_excavation_wind_resource_numbers, self.earth_work_back_fill_wind_resource_numbers = 0, 0
        # self.c40_wind_resource_numbers, self.c15_wind_resource_numbers, self.c80_wind_resource_numbers = 0, 0, 0
        # self.c80_wind_resource_numbers, self.reinforcement_wind_resource_numbers = 0, 0

    def extraction_data_110kVSwitChgearType_resource(self, TypeID):
        self.TypeID = TypeID

        sql = "SELECT * FROM auto_word_electrical_110kVSwitChgearType"
        self.Data110kVSwitChgearType = connect_sql_pandas(sql)
        self.Data110kVSwitChgearType = \
            self.Data110kVSwitChgearType.loc[
                self.Data110kVSwitChgearType['TypeID'] == self.TypeID]
        return self.Data110kVSwitChgearType

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

    def generate_dict_110kVSwitChgearType_resource(self, data, turbine_num):
        self.v110kVSwitChgearType = data
        self.turbine_numbers = turbine_num
        self.TypeName = self.v110kVSwitChgearType.at[self.v110kVSwitChgearType.index[0], 'TypeName']
        self.RatedVoltage = self.v110kVSwitChgearType.at[self.v110kVSwitChgearType.index[0], 'RatedVoltage']
        self.RatedCurrent = self.v110kVSwitChgearType.at[self.v110kVSwitChgearType.index[0], 'RatedCurrent']
        self.RatedFrequency = self.v110kVSwitChgearType.at[self.v110kVSwitChgearType.index[0], 'RatedFrequency']
        self.RatedBreakingCurrent = self.v110kVSwitChgearType.at[self.v110kVSwitChgearType.index[0], 'RatedBreakingCurrent']
        self.RatedClosingCurrent = self.v110kVSwitChgearType.at[self.v110kVSwitChgearType.index[0], 'RatedClosingCurrent']

        self.RatedPeakWCurrent = self.v110kVSwitChgearType.at[self.v110kVSwitChgearType.index[0], 'RatedPeakWCurrent']
        self.RatedShortTimeWCurrent = self.v110kVSwitChgearType.at[self.v110kVSwitChgearType.index[0], 'RatedShortTimeWCurrent']
        self.LineSpacing = self.v110kVSwitChgearType.at[self.v110kVSwitChgearType.index[0], 'LineSpacing']
        self.PTSpacing = self.v110kVSwitChgearType.at[self.v110kVSwitChgearType.index[0], 'PTSpacing']
        self.AccuracyClass = self.v110kVSwitChgearType.at[self.v110kVSwitChgearType.index[0], 'AccuracyClass']


        self.dict_110kVSwitChgearType_resource = {
            'turbine_numbers': int(self.turbine_numbers),
            '型号_110kV配电装置': self.TypeName,
            '额定电压_110kV配电装置': self.RatedVoltage,
            '额定电流_110kV配电装置': self.RatedCurrent,
            '额定频率_110kV配电装置': self.RatedFrequency,
            '额定开断电流_110kV配电装置': self.RatedBreakingCurrent,
            '额定关合电流_110kV配电装置': self.RatedClosingCurrent,
            '额定峰值耐受电流_110kV配电装置': self.RatedPeakWCurrent,
            '额定短时耐受电流_110kV配电装置': self.RatedShortTimeWCurrent,
            '出线间隔_110kV配电装置': self.LineSpacing,
            'PT间隔_110kV配电装置': self.PTSpacing,
            '准确级_110kV配电装置': self.AccuracyClass,
        }


        return self.dict_110kVSwitChgearType_resource

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
