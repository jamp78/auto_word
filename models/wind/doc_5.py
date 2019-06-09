from docxtpl import DocxTemplate, InlineImage
import sys
sys.path.append(r'D:\GOdoo12_community\myaddons\auto_word\models\source')
import connect_sql
import sys
sys.path.append(r'D:\GOdoo12_community\myaddons\auto_word\models\wind\chapter_5')
import generate_images, generate_dict
import os


def generate_wind_dict(tur_name, path_images):
    data_tur_np, data_power_np, data_efficiency_np, data_compare_np = connect_sql.connect_sql_chapter5(*tur_name)

    #####################
    generate_images.generate_images(path_images, data_power_np, data_efficiency_np)  # 一会儿注释generate_images

    #####################
    #  chapter 5

    dict_keys_chapter5 = ['id', '机组类型', '功率', '叶片数', '风轮直径', '扫风面积', '轮毂高度',
                          '功率调节', '切入风速', '切出风速', '额定风速', '发电机型式', '额定功率', '电压', '频率',
                          '塔架型式', '塔筒重量', '主制动系统', '第二制动', '三秒最大值', 'datetime1id', 'datetime1',
                          'datetime2id', 'datetime2' ]
    context_keys_chapter5 = ['机组类型', '功率', '叶片数', '风轮直径', '扫风面积', '轮毂高度', '功率调节', '切入风速',
                             '切出风速', '额定风速', '发电机型式', '额定功率', '电压', '主制动系统', '第二制动', '三秒最大值']

    dict_keys_compare_chapter5 = ['id', 'turbine_numbers', 'power_generation', 'weak', 'power_hours',
                                  'TerrainType_turbines_compare', 'project_id', 'create_uid', 'create_date',
                                  'write_uid', 'write_date', 'case_hub_height', 'case_name', 'investment_E3',
                                  'investment_turbines_kws', 'wind_ids']

    context_keys_compare_chapter5 = ['power_generation', 'case_hub_height', 'weak', 'power_hours',
                                     'investment_turbines_kws', 'investment_E3',
                                     '切出风速', '额定风速', '发电机型式', '额定功率', '电压', '主制动系统', '第二制动', '三秒最大值']

    print("---------开始 chapter 5--------")
    # chapter 5

    Dict_5 = generate_dict.get_dict(data_tur_np, dict_keys_chapter5)
    print(Dict_5)
    Dict = generate_dict.write_context(Dict_5, *context_keys_chapter5)


    return Dict


def generate_wind_docx(Dict, path_images):
    filename_box = ['cr5', 'result_chapter5']
    read_path = os.path.join(path_images, '%s.docx') % filename_box[0]
    save_path = os.path.join(path_images, '%s.docx') % filename_box[1]
    tpl = DocxTemplate(read_path)
    png_box = ('powers', 'efficiency')
    for i in range(0, 2):
        key = 'myimage' + str(i)
        value = InlineImage(tpl, os.path.join(path_images, '%s.png') % png_box[i])
        Dict[key] = value

    tpl.render(Dict)
    tpl.save(save_path)
