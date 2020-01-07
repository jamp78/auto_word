import os
from docxtpl import DocxTemplate
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../GOdoo12_community/myaddons/auto_word/models/electrical/chapter_6")))
# print(os.path.abspath(os.path.join(os.getcwd(), "../GOdoo12_community/myaddons/auto_word/models/electrical/chapter_6")))

from WireRod import WireRod
from ElectricalInsulator import ElectricalInsulator
from TowerType import TowerType
from TowerBase import TowerBase
from Cable import Cable
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../GOdoo12_community/myaddons/auto_word/models/electrical/chapter_6/electrical_frist")))

from BoxVoltageType import BoxVoltageType
from MainTransformerType import MainTransformerType
from v110kVSwitChgearType import v110kVSwitChgearType
from v110kVArresterType import v110kVArresterType
from v35kVTICType import v35kVTICType
from v35kVMTOCType import v35kVMTOCType
from v35kVSCType import v35kVSCType
from v35kVRPCDCType import v35kVRPCDCType
from v35kVGCType import v35kVGCType
from v35kVPTCType import v35kVPTCType
from SRGSType import SRGSType
from STType import STType
from CCGISType import CCGISType
from CCMTLVType import CCMTLVType


def generate_electrical_TypeID_dict(TypeID_boxvoltagetype, TypeID_maintransformertype,
                                    TypeID_v110kvswitchgeartype, TypeID_v110kvarrestertype, TypeID_v35kvtictype,
                                    TypeID_v35kvmtovctype, TypeID_v35kvsctype, TypeID_v35kvrpcdctype,
                                    TypeID_v35kvgctype, TypeID_v35kvptctype, TypeID_srgstype, TypeID_sttype,
                                    TypeID_ccgistype, TypeID_ccmtlvtype,
                                    Numbers_boxvoltagetype, Numbers_maintransformertype,
                                    Numbers_v110kvswitchgeartype, Numbers_v110kvarrestertype, Numbers_v35kvtictype,
                                    Numbers_v35kvmtovctype, Numbers_v35kvsctype, Numbers_v35kvptctype,
                                    Numbers_v35kvgctype, Numbers_srgstype, Numbers_sttype,
                                    Numbers_ccgistype, Numbers_ccmtlvtype,
                                    turbine_numbers):
    dictsum = {}
    project1 = BoxVoltageType()
    project2 = MainTransformerType()
    project3 = v110kVSwitChgearType()
    project4 = v110kVArresterType()
    project5 = v35kVTICType()
    project6 = v35kVMTOCType()
    project7 = v35kVSCType()
    project8 = v35kVRPCDCType()
    project9 = v35kVGCType()
    project10 = v35kVPTCType()
    project11 = SRGSType()
    project12 = STType()
    project13 = CCGISType()
    project14 = CCMTLVType()

    DataBoxVoltageType = project1.extraction_data_BoxVoltageType_resource(TypeID_boxvoltagetype)
    DataMainTransformerType = project2.extraction_data_MainTransformerType_resource(TypeID_maintransformertype)
    Datav110kVSwitChgearType = project3.extraction_data_110kVSwitChgearType_resource(TypeID_v110kvswitchgeartype)
    Datav110kVArresterType = project4.extraction_data_110kVArresterType_resource(TypeID_v110kvarrestertype)
    Datav35kVTICType = project5.extraction_data_35kVTICType_resource(TypeID_v35kvtictype)
    Datav35kVMTOCType = project6.extraction_data_35kVMTOCType_resource(TypeID_v35kvmtovctype)
    Datav35kVSCType = project7.extraction_data_35kVSCType_resource(TypeID_v35kvsctype)
    Datav35kVRPCDCType = project8.extraction_data_35kVRPCDCType_resource(TypeID_v35kvrpcdctype)
    # DataMainTransformerType = project9.extraction_data_MainTransformerType_resource(TypeID_v35kvptctype)
    # DataMainTransformerType = project10.extraction_data_MainTransformerType_resource(TypeID_srgstype)
    # DataMainTransformerType = project11.extraction_data_MainTransformerType_resource(TypeID_sttype)
    DataSTType = project12.extraction_data_STType_resource(TypeID_sttype)
    DataCCGISType = project13.extraction_data_CCGISType_resource(TypeID_ccgistype)
    DataCCMTLVTypeType = project14.extraction_data_CCMTLVType_resource(TypeID_ccmtlvtype)

    # dict1 = project1.generate_dict_BoxVoltageType_resource(DataBoxVoltageType, Numbers_boxvoltagetype)
    # dict2 = project2.generate_dict_MainTransformerType_resource(DataMainTransformerType, Numbers_maintransformertype)
    # dict3 = project3.generate_dict_110kVSwitChgearType_resource(Datav110kVSwitChgearType, Numbers_v110kvswitchgeartype)
    # dict4 = project4.generate_dict_110kVArresterType_resource(Datav110kVArresterType, Numbers_v110kvarrestertype)
    # dict5 = project5.generate_dict_35kVTICType_resource(Datav35kVTICType, Numbers_v35kvtictype)
    # dict6 = project6.generate_dict_35kVMTOCType_resource(Datav35kVMTOCType, Numbers_v35kvmtovctype)
    # dict7 = project7.generate_dict_35kVSCType_resource(Datav35kVSCType, Numbers_v35kvsctype)
    # dict8 = project8.generate_dict_35kVRPCDCType_resource(Datav35kVRPCDCType, Numbers_v35kvptctype)
    #
    # dict12 = project12.generate_dict_STType_resource(DataSTType, Numbers_sttype)
    # dict13 = project13.generate_dict_CCGISType_resource(DataCCGISType, Numbers_ccgistype)
    # dict14 = project14.generate_dict_CCMTLVType_resource(DataCCMTLVTypeType, Numbers_ccmtlvtype)


    dict1 = project1.generate_dict_BoxVoltageType_resource(DataBoxVoltageType, turbine_numbers)
    dict2 = project2.generate_dict_MainTransformerType_resource(DataMainTransformerType, turbine_numbers)
    dict3 = project3.generate_dict_110kVSwitChgearType_resource(Datav110kVSwitChgearType, turbine_numbers)
    dict4 = project4.generate_dict_110kVArresterType_resource(Datav110kVArresterType, turbine_numbers)
    dict5 = project5.generate_dict_35kVTICType_resource(Datav35kVTICType, turbine_numbers)
    dict6 = project6.generate_dict_35kVMTOCType_resource(Datav35kVMTOCType, turbine_numbers)
    dict7 = project7.generate_dict_35kVSCType_resource(Datav35kVSCType, turbine_numbers)
    dict8 = project8.generate_dict_35kVRPCDCType_resource(Datav35kVRPCDCType, turbine_numbers)

    dict12 = project12.generate_dict_STType_resource(DataSTType, turbine_numbers)
    dict13 = project13.generate_dict_CCGISType_resource(DataCCGISType, turbine_numbers)
    dict14 = project14.generate_dict_CCMTLVType_resource(DataCCMTLVTypeType, turbine_numbers)

    dictsum = dict(dict1, **dict2, **dict3, **dict4, **dict5, **dict6, **dict7, **dict8, **dict12, **dict13, **dict14)
    return dictsum


def generate_electrical_dict(project_chapter6_type, args):
    # step:1
    # 载入参数
    print("---------step:1  载入参数--------")
    #  chapter 6
    Dict_6 = {}
    # project_chapter6_type = ['山地']
    # args=[19, 22, 8, 1.5, 40, 6]
    print(project_chapter6_type, args)
    project01 = WireRod(project_chapter6_type, *args)
    project01.aluminium_cable_steel_reinforced("LGJ_240_30")
    args_chapter6_01_name = ['钢芯铝绞线']
    args_chapter6_01_type = ['LGJ_240_30']


    for i in range(0, len(args_chapter6_01_name)):
        if args_chapter6_01_name[i] == '钢芯铝绞线':
            print("---------线材:钢芯铝绞线--------")
            key_dict = args_chapter6_01_type[i]
            if key_dict == 'LGJ_240_30':
                value_dict = str(project01.aluminium_cable_steel_reinforced_length_weight)
                Dict_6[key_dict] = value_dict
    print("---------线材生成完毕--------")

    electrical_insulator_name_list = ['复合绝缘子', '瓷绝缘子', '复合针式绝缘子', '复合外套氧化锌避雷器']
    electrical_insulator_type_list = ['FXBW4_35_70', 'U70BP_146D', 'FPQ_35_4T16', 'YH5WZ_51_134']

    tower_type_list = ['单回耐张塔', '单回耐张塔', '单回耐张塔', '单回直线塔', '单回直线塔', '双回耐张塔', '双回耐张塔', '双回直线塔', '双回直线塔', '铁塔电缆支架']
    tower_type_high_list = ['J2_24', 'J4_24', 'FS_18', 'Z2_30', 'ZK_42', 'SJ2_24', 'SJ4_24', 'SZ2_30', 'SZK_42', '角钢']
    tower_weight_list = [6.8, 8.5, 7, 5.5, 8.5, 12.5, 17, 6.5, 10, 0.5, ]
    tower_height_list = [32, 32, 27, 37, 49, 37, 37, 42, 54, 0]
    tower_foot_distance_list = [5.5, 5.5, 6, 5, 6, 7, 8, 6, 8, 0]

    project02 = ElectricalInsulator(project_chapter6_type, *args)
    project02.sum_cal_tower_type(tower_type_list, tower_type_high_list, tower_weight_list, tower_height_list,
                                 tower_foot_distance_list)
    project02.electrical_insulator_model(project_chapter6_type, electrical_insulator_name_list,
                                         electrical_insulator_type_list)

    args_chapter6_02_type = electrical_insulator_type_list

    for i in range(0, len(args_chapter6_02_type)):
        key_dict = args_chapter6_02_type[i]
        if key_dict == 'FXBW4_35_70':
            value_dict = str(project02.used_numbers_FXBW4_35_70)
            Dict_6[key_dict] = value_dict
        if key_dict == 'U70BP_146D':
            value_dict = str(project02.used_numbers_U70BP_146D)
            Dict_6[key_dict] = value_dict
        if key_dict == 'FPQ_35_4T16':
            value_dict = str(project02.used_numbers_FPQ_35_4T16)
            Dict_6[key_dict] = value_dict
        if key_dict == 'YH5WZ_51_134':
            value_dict = str(project02.used_numbers_YH5WZ_51_134)
            Dict_6[key_dict] = value_dict

    print("---------绝缘子生成完毕--------")

    args_chapter6_03_type = tower_type_high_list
    project03 = TowerType(project_chapter6_type, *args)
    project03.sum_cal_tower_type(tower_type_list, tower_type_high_list, tower_weight_list, tower_height_list,
                                 tower_foot_distance_list)

    for i in range(0, len(args_chapter6_03_type)):
        key_dict = args_chapter6_03_type[i]
        if key_dict == 'J2_24':
            value_dict = str(project03.used_numbers_single_J2_24)
            value_dict_kg = float(str(project03.used_numbers_single_J2_24))*6.8
            key_dict_kg=key_dict+"_kg"
            Dict_6[key_dict] = value_dict
            Dict_6[key_dict_kg] = value_dict_kg

        if key_dict == 'J4_24':
            value_dict = str(project03.used_numbers_single_J4_24)
            value_dict_kg = float(str(project03.used_numbers_single_J4_24)) * 8.5
            key_dict_kg = key_dict + "_kg"
            Dict_6[key_dict] = value_dict
            Dict_6[key_dict_kg] = value_dict_kg

        if key_dict == 'FS_18':
            value_dict = str(project03.used_numbers_single_FS_18)
            value_dict_kg = float(str(project03.used_numbers_single_FS_18)) * 7
            key_dict_kg = key_dict + "_kg"
            Dict_6[key_dict] = value_dict
            Dict_6[key_dict_kg] = value_dict_kg

        if key_dict == 'Z2_30':
            value_dict = str(project03.used_numbers_single_Z2_30)
            value_dict_kg = float(str(project03.used_numbers_single_Z2_30)) * 5.5
            key_dict_kg = key_dict + "_kg"
            Dict_6[key_dict] = value_dict
            Dict_6[key_dict_kg] = value_dict_kg
        if key_dict == 'ZK_42':
            value_dict = str(project03.used_numbers_single_ZK_42)
            value_dict_kg = float(str(project03.used_numbers_single_ZK_42)) * 8.5
            key_dict_kg = key_dict + "_kg"
            Dict_6[key_dict] = value_dict
            Dict_6[key_dict_kg] = value_dict_kg
        if key_dict == 'SJ2_24':
            value_dict = str(project03.used_numbers_double_SJ2_24)
            value_dict_kg = float(str(project03.used_numbers_double_SJ2_24)) * 12.5
            key_dict_kg = key_dict + "_kg"
            Dict_6[key_dict] = value_dict
            Dict_6[key_dict_kg] = value_dict_kg
        if key_dict == 'SJ4_24':
            value_dict = str(project03.used_numbers_double_SJ4_24)
            value_dict_kg = float(str(project03.used_numbers_double_SJ4_24)) * 17
            key_dict_kg = key_dict + "_kg"
            Dict_6[key_dict] = value_dict
            Dict_6[key_dict_kg] = value_dict_kg
        if key_dict == 'SZ2_30':
            value_dict = str(project03.used_numbers_double_SZ2_30)
            value_dict_kg = float(str(project03.used_numbers_double_SZ2_30)) * 6.5
            key_dict_kg = key_dict + "_kg"
            Dict_6[key_dict] = value_dict
            Dict_6[key_dict_kg] = value_dict_kg
        if key_dict == 'SZK_42':
            value_dict = str(project03.used_numbers_double_SZK_42)
            value_dict_kg = float(str(project03.used_numbers_double_SZK_42)) * 10
            key_dict_kg = key_dict + "_kg"
            Dict_6[key_dict] = value_dict
            Dict_6[key_dict_kg] = value_dict_kg
        if key_dict == '角钢':
            value_dict = str(project03.used_numbers_angle_steel)
            value_dict_kg = float(str(project03.used_numbers_angle_steel)) * 0.5
            key_dict_kg = key_dict + "_kg"
            Dict_6[key_dict] = value_dict
            Dict_6[key_dict_kg] = value_dict_kg

    Dict_6['铁塔合计'] = str(project03.sum_used_numbers)
    Dict_6['铁塔合计_kg'] = str(project03.sum_tower_number_weight)

    print("---------铁塔生成完毕--------")

    tower_base_list = ['ZJC1', 'ZJC2', 'JJC1', 'JJC2', 'TW1', 'TW2', '基础垫层']
    c25_unit_list = [12, 16, 42, 80, 8.8, 10.2, 2.4]
    steel_unit_list = [300, 500, 750, 900, 600, 800, 0]
    foot_bolt_list = [100, 180, 280, 360, 100, 180, 0]

    args_chapter6_04_type = tower_base_list
    project04 = TowerBase(project_chapter6_type, *args)
    project04.sum_cal_tower_type(tower_type_list, tower_type_high_list, tower_weight_list, tower_height_list,
                                 tower_foot_distance_list)
    project04.sum_cal_tower_base(tower_base_list, c25_unit_list, steel_unit_list, foot_bolt_list)

    for i in range(0, len(args_chapter6_04_type)):
        key_dict = args_chapter6_04_type[i]
        if key_dict == 'ZJC1':
            Dict_6['ZJC1_num'] = str(project04.used_numbers_base_zjc1)
            Dict_6['c25_sum_zjc1'] = str(project04.c25_sum_zjc1)
            Dict_6['steel_sum_zjc1'] = str(project04.steel_sum_zjc1)

        if key_dict == 'ZJC2':
            Dict_6['ZJC2_num'] = str(project04.used_numbers_base_zjc2)
            Dict_6['c25_sum_zjc2'] = str(project04.c25_sum_zjc2)
            Dict_6['steel_sum_zjc2'] = str(project04.steel_sum_zjc2)

        if key_dict == 'JJC1':
            Dict_6['JJC1_num'] = str(project04.used_numbers_base_jjc1)
            Dict_6['c25_sum_jjc1'] = str(project04.c25_sum_jjc1)
            Dict_6['steel_sum_jjc1'] = str(project04.steel_sum_jjc1)

        if key_dict == 'JJC2':
            Dict_6['jjc2_num'] = str(project04.used_numbers_base_jjc2)
            Dict_6['c25_sum_jjc2'] = str(project04.c25_sum_jjc2)
            Dict_6['steel_sum_jjc2'] = str(project04.steel_sum_jjc2)

        if key_dict == 'TW1':
            Dict_6['tw1_num'] = str(project04.used_numbers_base_tw1)
            Dict_6['c25_sum_tw1'] = str(project04.c25_sum_tw1)
            Dict_6['steel_sum_tw1'] = str(project04.steel_sum_tw1)
        if key_dict == 'TW2':
            Dict_6['tw2_num'] = str(project04.used_numbers_base_tw2)
            Dict_6['c25_sum_tw2'] = str(project04.c25_sum_tw2)
            Dict_6['steel_sum_tw2'] = str(project04.steel_sum_tw2)

        if key_dict == '基础垫层':
            Dict_6['base_layer'] = str(project04.used_numbers_base_layer)
            Dict_6['c25_sum_layer'] = str(project04.c25_sum_layer)
            Dict_6['steel_sum_layer'] = str(project04.steel_sum_layer)

    Dict_6['基础数量合计'] = str(project04.used_numbers_base_sum)
    Dict_6['基础混凝土合计'] = str(project04.c25_sum)
    Dict_6['基础钢筋合计'] = str(project04.steel_sum)

    print("---------铁塔基础生成完毕--------")

    cable_project_list = ['高压电缆', '高压电缆', '电缆沟', '电缆终端', '电缆终端']
    cable_model_list = ['YJLV22_26_35_3_95_gaoya', 'YJV22_26_35_1_300_gaoya', '电缆沟长度',
                        'YJLV22_26_35_3_95_dianlanzhongduan',
                        'YJV22_26_35_1_300_dianlanzhongduan']

    args_chapter6_05_type = cable_model_list
    project05 = Cable(project_chapter6_type, *args)
    project05.sum_cal_cable(cable_project_list, cable_model_list)

    for i in range(0, len(args_chapter6_05_type)):
        key_dict = args_chapter6_05_type[i]
        if key_dict == 'YJLV22_26_35_3_95_gaoya':
            Dict_6['YJLV22_26_35_3_95_gaoya'] = str(project05.cable_model_YJLV22_26_35_3_95_gaoya)
        if key_dict == 'YJV22_26_35_1_300_gaoya':
            Dict_6['YJV22_26_35_1_300_gaoya'] = str(project05.cable_model_YJV22_26_35_1_300_gaoya)
        if key_dict == '电缆沟长度':
            Dict_6['电缆沟长度'] = str(project05.cable_model_cable_duct)
        if key_dict == 'YJLV22_26_35_3_95_dianlanzhongduan':
            Dict_6['YJLV22_26_35_3_95_dianlanzhongduan'] = str(project05.cable_model_YJLV22_26_35_3_95_dianlanzhongduan)
        if key_dict == 'YJV22_26_35_1_300_dianlanzhongduan':
            Dict_6['YJV22_26_35_1_300_dianlanzhongduan'] = str(project05.cable_model_YJV22_26_35_1_300_dianlanzhongduan)
    return Dict_6


def generate_electrical_docx(Dict, path_images):
    filename_box = ['cr6_集电线路', 'result_chapter6']
    read_path = os.path.join(path_images, '%s.docx') % filename_box[0]
    save_path = os.path.join(path_images, '%s.docx') % filename_box[1]
    tpl = DocxTemplate(read_path)
    tpl.render(Dict)
    tpl.save(save_path)
