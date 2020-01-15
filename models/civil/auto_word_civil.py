# -*- coding: utf-8 -*-

from doc_8 import generate_civil_dict, generate_civil_docx, get_dict_8
import base64, os
import numpy
from RoundUp import round_up
from odoo import models, fields, api
from odoo import exceptions
import global_dict as gl


class auto_word_civil_geology(models.Model):
    _name = 'auto_word_civil.geology'
    _description = 'Civil geology'
    _rec_name = 'project_id'

    # --------项目参数---------
    project_id = fields.Many2one('auto_word.project', string=u'项目名', required=True)
    version_id = fields.Char(u'版本', required=True, default="1.0")
    report_attachment_id = fields.Many2one('ir.attachment', string=u'可研报告地质章节')
    # --------地质参数---------
    regional_geology = fields.Char(u'区域地质构造')
    neotectonic_movements_earthquakes = fields.Char(u'新构造运动及地震')
    topographical_evaluation = fields.Char(u'地形地貌评价')
    formation_evaluation = fields.Char(u'地层岩性评价')

    bad_geology_special_rock = fields.Char(u'不良地质作用')

    evaluation_stability_site = fields.Char(u'工程场地稳定性评价')
    evaluation_building_foundation = fields.Char(u'建筑地基评价')

    ground_motion_parameters = fields.Char(u'地震动参数')
    stability_suitability = fields.Char(u'场地的稳定性与适宜性')
    construction_water = fields.Char(u'施工用水及生活用水水源调查及评价')
    natural_building_material = fields.Char(u'天然建筑材料')
    engineering_hydrogeology = fields.Char(u'工程水文地质')

    conclusion = fields.Char(u'结论和建议')


    # 提交
    dict_3_submit_word = fields.Char(u'字典3_提交')
    # 提取
    dict_1_submit_word = fields.Char(u'字典1_提交')
    dict_5_submit_word = fields.Char(u'字典5_提交')

    def civil_geology_generate(self):
        self.dict_1_submit_word = eval(self.project_id.dict_1_submit_word)
        self.dict_5_submit_word = eval(self.project_id.dict_5_submit_word)

        dict_3_word = {
            '区域地质构造': self.regional_geology,
            '新构造运动及地震': self.neotectonic_movements_earthquakes,
            '地形地貌评价': self.topographical_evaluation,
            '地层岩性评价': self.formation_evaluation,
            '不良地质作用': self.bad_geology_special_rock,

            '工程场地稳定性评价': self.evaluation_stability_site,
            '建筑地基评价': self.evaluation_building_foundation,
            '地震动参数': self.ground_motion_parameters,
            '场地的稳定性与适宜性': self.stability_suitability,

            '施工用水及生活用水水源调查及评价': self.construction_water,
            '天然建筑材料': self.natural_building_material,
            '工程水文地质': self.engineering_hydrogeology,
            '结论和建议': self.conclusion,
        }

        self.dict_3_submit_word = dict_3_word

        dict_3_words = dict(dict_3_word, **eval(self.dict_1_submit_word), **eval(self.dict_5_submit_word))

        for key, value in dict_3_word.items():
            gl.set_value(key, value)

        path_chapter_8 = self.env['auto_word.project'].path_chapter_8
        generate_civil_docx(dict_3_words, path_chapter_8, 'cr3', 'result_chapter3')
        reportfile_name = open(
            file=os.path.join(path_chapter_8, '%s.docx') % 'result_chapter3',
            mode='rb')
        byte = reportfile_name.read()
        reportfile_name.close()
        print('file lenth=', len(byte))
        base64.standard_b64encode(byte)
        if (str(self.report_attachment_id) == 'ir.attachment()'):
            Attachments = self.env['ir.attachment']
            print('开始创建新纪录')
            New = Attachments.create({
                'name': self.project_id.project_name + '可研报告地质章节下载页',
                'datas_fname': self.project_id.project_name + '可研报告地质章节.docx',
                'datas': base64.standard_b64encode(byte),
                'display_name': self.project_id.project_name + '可研报告地质章节',
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

    def submit_civil_geology(self):
        self.project_id.dict_3_submit_word = self.dict_3_submit_word
        return True


class auto_word_civil_design_safety_standard(models.Model):
    _name = 'auto_word_civil.design_safety_standard'
    _description = 'Civil Design Safety Standard'
    _rec_name = 'civil_id'
    civil_id = fields.Many2one('auto_word.civil', string=u'项目名称', required=False)

    ProjectLevel = fields.Selection([("I", u"I"), ("II", u"II"), ("III", u"III")],
                                    string=u"项目工程等别", default="I")
    ProjectSize = fields.Selection([("大型", u"大型"), ("中型", u"中型"), ("小型", u"小型")],
                                   string=u"工程规模", defult='大型')
    BuildingLevel = fields.Selection([("1级", u"1级"), ("2级", u"2级"), ("3级", u"3级")],
                                     string=u"建筑物级别", defult='2级')
    EStructuralSafetyLevel = fields.Selection([("1级", u"1级"), ("2级", u"2级"), ("3级", u"3级")],
                                              string=u"变电站结构安全等级", defult='1级')
    TStructuralSafetyLevel = fields.Selection([("1级", u"1级"), ("2级", u"2级"), ("3级", u"3级")],
                                              string=u"风机结构安全等级", defult='1级')
    FloodDesignLevel = fields.Integer(u'洪水设计标准', defult='50')
    ReFloodDesignLevel = fields.Selection([("1%", u"1%"), ("2%", u"2%"), ("3%", u"3%")],
                                          string=u"重现期洪水位", defult="2%")
    # TerrainType_words = fields.Selection([("山地起伏较大，基础周边可能会形成高边坡，需要进行高边坡特别设计", u"山地"),
    #                                       ("地形较为平缓，不需要进行高边坡特别设计", u"平原")], string=u"地形描述")
    #
    TurbineTowerDesignLevel = fields.Selection([("1级", u"1级"), ("2级", u"2级"), ("3级", u"3级")],
                                               string=u"机组塔架地基设计级别", defult="1级")
    # 抗震
    BuildingEarthquakeDesignLevel = fields.Selection([("甲类", u"甲类"), ("乙类", u"乙类"), ("丙类", u"丙类")],
                                                     string=u"建筑物抗震设防类别")
    DesignEarthquakeLevel = fields.Selection([("第一组", u"第一组"), ("第二组", u"第二组"), ("第三组", u"第三组")],
                                             string=u"设计地震分组", defult="第一组")
    Earthquake_g = fields.Float(u'设计基本地震加速度值')
    BuildingYardLevel = fields.Selection([("I", u"I"), ("II", u"II"), ("III", u"III")],
                                         string=u"建筑物场地类别", defult="I")

    BuildingYardLevel_word = fields.Selection([("抗震不利地段", u"抗震不利地段"), ("抗震有利地段", u"抗震有利地段")],
                                              string=u"建筑物场地抗震类别", defult="抗震不利地段")

    def button_civil_design_safety_standard(self):
        self.civil_id.ProjectSize = self.ProjectSize
        self.civil_id.BuildingLevel = self.BuildingLevel
        self.civil_id.EStructuralSafetyLevel = self.EStructuralSafetyLevel
        self.civil_id.TStructuralSafetyLevel = self.TStructuralSafetyLevel
        self.civil_id.FloodDesignLevel = self.FloodDesignLevel
        self.civil_id.ReFloodDesignLevel = self.ReFloodDesignLevel
        # self.civil_id.TerrainType_words = self.TerrainType_words
        self.civil_id.TurbineTowerDesignLevel = self.TurbineTowerDesignLevel
        # 抗震
        self.civil_id.BuildingEarthquakeDesignLevel = self.BuildingEarthquakeDesignLevel
        self.civil_id.DesignEarthquakeLevel = self.DesignEarthquakeLevel
        self.civil_id.Earthquake_g = self.Earthquake_g
        self.civil_id.BuildingYardLevel = self.BuildingYardLevel
        self.civil_id.BuildingYardLevel_word = self.BuildingYardLevel_word

        self.civil_id.ProjectLevel = self.ProjectLevel

        self.civil_id.project_id.ProjectLevel_all = self
        self.civil_id.is_dict_8_word_part = True

        return True


class civil_windbase(models.Model):
    _name = 'auto_word_civil.windbase'
    _description = 'Civil windbase'
    _rec_name = 'BasicType'
    FortificationIntensity = fields.Selection([(6, "6"), (7, "7"), (8, "8"), (9, "9")], string=u"设防烈度", required=True)
    BearingCapacity = fields.Selection(
        [(60, "60"), (80, "80"), (100, "100"), (120, "120"), (140, "140"), (160, "160"), (180, "180"), (200, "200"),
         (220, "220"), (240, "240"), (260, "260")], string=u"地基承载力(kpa)", required=True)
    BasicType = fields.Selection(
        [('扩展基础', u'扩展基础'), ('预制桩承台基础', u'预制桩承台基础'), ('灌注桩承台基础', u'灌注桩承台基础'), ('复合地基', u'复合地基')],
        string=u'基础形式', required=True)
    UltimateLoad = fields.Selection(
        [(50000, "50000"), (60000, "60000"), (70000, "70000"), (80000, "80000"), (90000, "90000"),
         (100000, "100000"), (110000, "110000"), (120000, "120000")], string=u"极限载荷", required=True)
    FloorRadiusR = fields.Float(u'底板半径R')
    R1 = fields.Float(u'棱台顶面半径R1')
    R2 = fields.Float(u'台柱半径R2')
    H1 = fields.Float(u'底板外缘高度H1')
    H2 = fields.Float(u'底板棱台高度H2')
    H3 = fields.Float(u'台柱高度H3')
    PileDiameter = fields.Float(u'桩直径')
    Number = fields.Float(u'根数')
    Length = fields.Float(u'长度')
    SinglePileLength = fields.Float(u'单台总桩长')
    Area = fields.Float(u'面积m²')
    Volume = fields.Float(u'体积m³')
    Cushion = fields.Float(u'垫层')
    M48PreStressedAnchor = fields.Float(u'M48预应力锚栓（m)')
    C80SecondaryGrouting = fields.Float(u'C80二次灌浆')


class civil_convertbase(models.Model):
    _name = 'auto_word_civil.convertbase'
    _description = 'Civil ConvertBase'
    _rec_name = 'TurbineCapacity'
    TurbineCapacity = fields.Char(string=u"风机容量", required=True)

    ConvertStation = fields.Selection(
        [(2200, "2200"), (2500, "2500"), (2750, "2750"), (3300, "3300"), (3520, "3520"), (4000, "4000")],
        string=u"箱变容量", required=True)

    Long = fields.Float(u'长')
    Width = fields.Float(u'宽')
    High = fields.Float(u'高')
    WallThickness = fields.Float(u'壁厚')
    HighPressure = fields.Float(u'压顶高')
    C35ConcreteTop = fields.Float(u'C35混凝土压顶')
    C15Cushion = fields.Float(u'C15垫层')
    MU10Brick = fields.Float(u'MU10砖')
    Reinforcement = fields.Float(u'钢筋')
    Area = fields.Float(u'面积')


def civil_generate_docx_dict(self):
    self.dict_1_submit_word = self.project_id.dict_1_submit_word
    self.dict_3_submit_word = self.project_id.dict_3_submit_word
    self.dict_5_submit_word = self.project_id.dict_5_submit_word
    print("check dict_1_submit_word")
    print(self.dict_1_submit_word)
    if self.dict_1_submit_word == False:
        s = "项目"
        raise exceptions.Warning('请点选 %s，并点击 --> 分发信息（%s 位于软件上方，自动编制报告系统右侧）。' % (s, s))
    if self.dict_5_submit_word == False:
        s = "风能部分"
        raise exceptions.Warning('请点选 %s，并点击风能详情 --> 提交报告（%s 位于软件上方，自动编制报告系统右侧）。' % (s, s))

    if self.is_dict_8_word_part == False:
        s = "土建部分"
        raise exceptions.Warning('请点选 %s，并点击 --> 设计安全标准。' % (s))

    if self.project_id.dict_3_submit_word == False:
        self.dict_3_submit_word = {}
    else:
        self.dict_3_submit_word = eval(self.project_id.dict_3_submit_word)

    self.line_data = [float(self.line_1), float(self.line_2)]
    self.basic_stone_ratio = 10 - self.basic_earthwork_ratio
    self.road_stone_ratio = 10 - self.road_earthwork_ratio

    self.numbers_list_road = [self.road_1_num, self.road_2_num, self.road_3_num, int(self.turbine_numbers)]
    list = [int(self.turbine_numbers), self.BasicType, self.UltimateLoad, self.FortificationIntensity,
            self.basic_earthwork_ratio / 10, self.basic_stone_ratio / 10, float(self.TurbineCapacity),
            self.road_earthwork_ratio / 10,
            self.road_stone_ratio / 10, self.project_id.Status, self.project_id.Grade, self.project_id.Capacity,
            self.TerrainType,
            self.numbers_list_road,
            float(self.overhead_line), float(self.direct_buried_cable), self.line_data,
            float(self.main_booster_station_num),
            float(self.overhead_line_num), float(self.direct_buried_cable_num)]
    np = numpy.array(list)
    dict_keys = ['turbine_numbers', 'BasicType', 'UltimateLoad', 'FortificationIntensity',
                 'basic_earthwork_ratio',
                 'basic_stone_ratio', 'TurbineCapacity', 'road_earthwork_ratio', 'road_stone_ratio', 'Status',
                 'Grade', 'Capacity', 'TerrainType', 'numbers_list_road', 'overhead_line', 'direct_buried_cable',
                 'line_data', 'main_booster_station_num', 'overhead_line_num', 'direct_buried_cable_num']

    dict_8 = get_dict_8(np, dict_keys)
    dict8 = generate_civil_dict(**dict_8)
    dict5 = eval(self.dict_5_submit_word)
    dict3 = eval(self.dict_3_submit_word)
    dict1 = eval(self.dict_1_submit_word)

    dict_8_word_part = {
        # 设计安全标准
        '项目工程等别': self.ProjectLevel,
        '工程规模': self.ProjectSize,
        '建筑物级别': self.BuildingLevel,
        '变电站结构安全等级': self.EStructuralSafetyLevel,
        '风机结构安全等级': self.TStructuralSafetyLevel,

        '洪水设计标准': self.FloodDesignLevel,
        '重现期洪水位': self.ReFloodDesignLevel,
        '地形描述': self.TerrainType_words,
        '机组塔架地基设计级别': self.TurbineTowerDesignLevel,

        '建筑物抗震设防类别': self.BuildingEarthquakeDesignLevel,
        '设计地震分组': self.DesignEarthquakeLevel,
        '设计基本地震加速度值': self.Earthquake_g,
        '建筑物场地类别': self.BuildingYardLevel,
        '建筑物场地抗震类别': self.BuildingYardLevel_word,

        "周边道路": self.road_names,
        "改扩建道路": self.road_1_num,
        "进站道路": self.road_2_num,
        "新建施工检修道路": self.road_3_num,
        "道路工程长度": self.total_civil_length,
        "合计亩_永久用地面积": self.permanent_land_area,
        "合计亩_临时用地面积": self.temporary_land_area,
        "总用地面积": self.land_area,
        "运输车辆": self.cars

    }

    dict_8_word = dict(dict_8_word_part, **dict8)

    dict_8_words = dict(dict_8_word, **dict5, **dict3, **dict1)

    for key, value in dict_8_word.items():
        gl.set_value(key, value)

    self.dict_8_submit_word=dict_8_word
    self.dict_8_submit_words = dict_8_words

    return True


class auto_word_civil(models.Model):
    _name = 'auto_word.civil'
    _description = 'Civil input'
    _rec_name = 'project_id'
    _inherit = ['auto_word_civil.design_safety_standard', 'auto_word_civil.windbase', 'auto_word_civil.convertbase']

    # 提交
    dict_8_submit_word = fields.Char(u'字典8_提交')
    dict_8_submit_words = fields.Char(u'字典8_提交s')
    # 提取
    dict_1_submit_word = fields.Char(u'字典1_提交')
    dict_3_submit_word = fields.Char(u'字典3_提交')
    dict_5_submit_word = fields.Char(u'字典5_提交')

    # --------项目参数---------
    project_id = fields.Many2one('auto_word.project', string=u'项目名', required=True)
    version_id = fields.Char(u'版本', required=True, default="1.0")
    report_attachment_id = fields.Many2one('ir.attachment', string=u'可研报告土建章节')
    is_dict_8_word_part = fields.Boolean("dict_8_word_part?", default=False)

    # --------风能参数---------
    turbine_numbers = fields.Char(u'推荐机组数量', readonly=True)
    name_tur_suggestion = fields.Char(u'推荐机型', readonly=True)
    hub_height_suggestion = fields.Char(u'推荐轮毂高度', readonly=True)
    TurbineCapacity = fields.Char(string=u"风机容量", required=False, readonly=True)
    # --------土建参数---------
    # fortification_intensity = fields.Selection([(6, "6"), (7, "7"), (8, "8"), (9, "9")], string=u"设防烈度", required=False,
    #                                            default=7)
    # basic_type = fields.Selection(
    #     [('扩展基础', u'扩展基础'), ('预制桩承台基础', u'预制桩承台基础'), ('灌注桩承台基础', u'灌注桩承台基础'), ('复合地基', u'复合地基')],
    #     string=u'基础形式', required=False, default="扩展基础")
    # ultimate_load = fields.Selection(
    #     [(50000, "50000"), (60000, "60000"), (70000, "70000"), (80000, "80000"), (90000, "90000"), (100000, "100000"),
    #      (110000, "110000"), (120000, "120000")], string=u"极限载荷", required=False, default=70000)
    basic_earthwork_ratio = fields.Selection(
        [(0, "0"), (1, "10%"), (2, "20%"), (3, "30%"), (4, "40%"), (5, "50%"), (6, "60%"), (7, "70%"),
         (8, "80%"), (9, "90%"), (1, '100%')], string=u"基础土方比", required=False, default=8)
    road_earthwork_ratio = fields.Selection(
        [(0, "0"), (1, "10%"), (2, "20%"), (3, "30%"), (4, "40%"), (5, "50%"), (6, "60%"), (7, "70%"),
         (8, "80%"), (9, "90%"), (1, '100%')], string=u"道路土方比", required=False, default=8)

    TerrainType = fields.Char(u'山地类型', readonly=True)
    road_1_num = fields.Float(u'改扩建道路', required=False, default=5)
    road_2_num = fields.Float(u'进站道路', required=False, default=1.5)
    road_3_num = fields.Float(u'新建施工检修道路', required=False, default=10)
    total_civil_length = fields.Float(compute='_compute_total_civil_length', string=u'道路工程长度')

    # --------电气参数---------
    line_1 = fields.Float(u'线路总挖方', required=False, default="15000")
    line_2 = fields.Float(u'线路总填方', required=False, default="10000")
    overhead_line = fields.Float(u'架空线路用地', required=False, default="1500")
    direct_buried_cable = fields.Float(u'直埋电缆用地', required=False, default="3000")

    overhead_line_num = fields.Char(u'架空线路塔基数量', default="0", readonly=True)
    direct_buried_cable_num = fields.Char(u'直埋电缆长度', default="0", readonly=True)
    main_booster_station_num = fields.Char(u'主变数量', default="0", readonly=True)

    # --------经评参数---------
    investment_E4 = fields.Float(compute='_compute_total_civil_length', string=u'道路投资(万元)')

    # --------设计安全标准---------
    ProjectLevel = fields.Char(u'项目工程等别', default="待提交", readonly=True)

    ProjectLevel_all = fields.Many2one('auto_word_civil.design_safety_standard', string=u'项目工程等别')
    TerrainType_words = fields.Char(u'地形描述', default="待提交", readonly=True, compute='_compute_terrain_type_words')

    # ProjectSize = fields.Char(u'工程规模', default="待提交", readonly=True)
    # BuildingLevel = fields.Char(u'建筑物级别', default="待提交", readonly=True)
    # EStructuralSafetyLevel = fields.Char(u'变电站结构安全等级', default="待提交", readonly=True)
    # TStructuralSafetyLevel = fields.Char(u'风机结构安全等级', default="待提交", readonly=True)
    #
    # FloodDesignLevel = fields.Char(u'洪水设计标准', default="待提交", readonly=True)
    # ReFloodDesignLevel = fields.Char(u'重现期洪水位', default="待提交", readonly=True)

    # TurbineTowerDesignLevel = fields.Char(u'机组塔架地基设计级别', default="待提交", readonly=True)
    # BuildingEarthquakeDesignLevel = fields.Char(u'建筑物抗震设防类别', default="待提交", readonly=True)
    # DesignEarthquakeLevel = fields.Char(u'设计地震分组', default="待提交", readonly=True)
    # Earthquake_g = fields.Char(u'设计基本地震加速度值', default="待提交", readonly=True)
    # BuildingYardLevel = fields.Char(u'建筑物场地类别', default="待提交", readonly=True)
    # BuildingYardLevel_word = fields.Char(u'建筑物场地抗震类别', default="待提交", readonly=True)

    # 土建结果
    # 风机基础工程数量表
    EarthExcavation_WindResource = fields.Char(u'土方开挖（m3）', readonly=True)
    StoneExcavation_WindResource = fields.Char(u'石方开挖（m3）', readonly=True)
    EarthWorkBackFill_WindResource = fields.Char(u'土石方回填（m3）', readonly=True)
    # Volume = fields.Char(u'C40混凝土（m3）', readonly=True)
    # Cushion = fields.Char(u'C15混凝土（m3）', readonly=True)
    # Reinforcement = fields.Char(u'钢筋（t）', readonly=True)
    Based_Waterproof = fields.Char(u'基础防水', default=1)
    Settlement_Observation = fields.Char(u'沉降观测', default=4)
    # SinglePileLength = fields.Char(u'总预制桩长（m）', readonly=True)
    # M48PreStressedAnchor = fields.Char(u'M48预应力锚栓（m）', readonly=True)
    # C80SecondaryGrouting = fields.Char(u'C80二次灌浆（m3）', readonly=True)
    stake_number = fields.Char(u'单台风机桩根数（根）', readonly=True)

    # 土石方平衡表

    turbine_foundation_box_voltage_excavation = fields.Char(u'开挖', readonly=True)
    turbine_foundation_box_voltage_back_fill = fields.Char(u'回填', readonly=True)
    turbine_foundation_box_voltage_spoil = fields.Char(u'弃土', readonly=True)
    booster_station_engineering_excavation = fields.Char(u'开挖', readonly=True)
    booster_station_engineering_back_fill = fields.Char(u'回填', readonly=True)
    booster_station_engineering_spoil = fields.Char(u'弃土', readonly=True)
    road_engineering_excavation = fields.Char(u'开挖', readonly=True)
    road_engineering_back_fill = fields.Char(u'回填', readonly=True)
    road_engineering_spoil = fields.Char(u'弃土', readonly=True)
    hoisting_platform_excavation = fields.Char(u'开挖', readonly=True)
    hoisting_platform_back_fill = fields.Char(u'回填', readonly=True)
    hoisting_platform_spoil = fields.Char(u'弃土', readonly=True)
    total_line_excavation = fields.Char(u'开挖', readonly=True)
    total_line_back_fill = fields.Char(u'回填', readonly=True)
    total_line_spoil = fields.Char(u'弃土', readonly=True)
    sum_EarthStoneBalance_excavation = fields.Char(u'开挖', readonly=True)
    sum_EarthStoneBalance_back_fill = fields.Char(u'回填', readonly=True)
    sum_EarthStoneBalance_spoil = fields.Char(u'弃土', readonly=True)

    temporary_land_area = fields.Char(u'临时用地面积（亩）', readonly=True)
    permanent_land_area = fields.Char(u'永久用地面积（亩）', readonly=True)
    land_area = fields.Char(u'总用地面积', readonly=True)
    road_names = fields.Char(string=u'周边道路')
    cars = fields.Char(u'运输车辆', readonly=True, compute='_compute_terrain_type_words')

    @api.depends('TerrainType')
    def _compute_terrain_type_words(self):
        for re in self:
            if re.TerrainType == "平原" or "缓坡" in re.TerrainType:
                re.TerrainType_words = "地形较为平缓，不需要进行高边坡特别设计."
                re.cars = "举升车运输技术上更为先进，较适合山地、重丘风场。因此，本风场建议叶片运输采用特种运输车辆。"
                if re.TerrainType == "平原":
                    re.cars = "本风场建议叶片运输采用平板车。"
            else:
                re.TerrainType_words = "山地起伏较大，基础周边可能会形成高边坡，需要进行高边坡特别设计."
                re.cars = "举升车运输技术上更为先进，较适合山地、重丘风场。因此，本风场建议叶片运输采用特种运输车辆。"

    @api.depends('road_1_num', 'road_2_num', 'road_3_num', 'TerrainType')
    def _compute_total_civil_length(self):
        for re in self:
            re.total_civil_length = re.road_1_num + re.road_2_num + re.road_3_num
            if re.TerrainType == "平原":
                re.investment_E4 = float(re.total_civil_length) * 50
            elif re.TerrainType == "丘陵":
                re.investment_E4 = float(re.total_civil_length) * 80
            else:
                re.investment_E4 = float(re.total_civil_length) * 140

    def submit_civil(self):
        self.basic_stone_ratio = 10 - self.basic_earthwork_ratio
        self.road_stone_ratio = 10 - self.road_earthwork_ratio

        projectname = self.project_id
        projectname.civil_attachment_id = self
        projectname.civil_attachment_ok = u"已提交,版本：" + self.version_id

        projectname.road_1_num = self.road_1_num
        projectname.road_2_num = self.road_2_num
        projectname.road_3_num = self.road_3_num
        projectname.total_civil_length = self.total_civil_length
        projectname.investment_E4 = self.investment_E4

        projectname.basic_type = self.BasicType
        projectname.ultimate_load = self.UltimateLoad
        projectname.fortification_intensity = self.FortificationIntensity
        projectname.basic_earthwork_ratio = str(self.basic_earthwork_ratio * 10) + "%"
        projectname.basic_stone_ratio = str(self.basic_stone_ratio * 10) + "%"
        projectname.road_earthwork_ratio = str(self.road_earthwork_ratio * 10) + "%"
        projectname.road_stone_ratio = str(self.road_stone_ratio * 10) + "%"
        projectname.ProjectLevel = self.ProjectLevel

        projectname.EarthExcavation_WindResource = self.EarthExcavation_WindResource
        projectname.StoneExcavation_WindResource = self.StoneExcavation_WindResource
        projectname.EarthWorkBackFill_WindResource = self.EarthWorkBackFill_WindResource
        projectname.Volume = self.Volume
        projectname.Cushion = self.Cushion
        projectname.Reinforcement = self.Reinforcement
        projectname.Based_Waterproof = self.Based_Waterproof
        projectname.Settlement_Observation = self.Settlement_Observation
        projectname.SinglePileLength = self.SinglePileLength
        projectname.M48PreStressedAnchor = self.M48PreStressedAnchor
        projectname.C80SecondaryGrouting = self.C80SecondaryGrouting
        projectname.stake_number = self.stake_number

        if self.dict_8_submit_word == False:
            raise exceptions.Warning('请先点击 --> 计算按钮')

        dict_8_submit_word=eval(self.dict_8_submit_word)
        projectname.BasicType = dict_8_submit_word['基础形式']
        projectname.FloorRadiusR = dict_8_submit_word['基础底面圆直径']
        projectname.H1 = dict_8_submit_word['基础底板外缘高度']
        projectname.R2 = dict_8_submit_word['台柱圆直径']
        projectname.H2 = dict_8_submit_word['基础底板圆台高度']
        projectname.H3 = dict_8_submit_word['台柱高度']

        projectname.temporary_land_area = dict_8_submit_word['合计亩_临时用地面积']
        projectname.permanent_land_area = dict_8_submit_word['合计亩_永久用地面积']
        projectname.land_area = self.land_area

        projectname.excavation = dict_8_submit_word['合计_开挖']
        projectname.backfill = dict_8_submit_word['合计_回填']
        projectname.spoil = dict_8_submit_word['合计_弃土']

        projectname.line_1 = self.line_1
        projectname.line_2 = self.line_2

        projectname.civil_all = self
        self.project_id.dict_8_submit_word = self.dict_8_submit_word

        return True

    #   计算
    def cal_civil(self):
        projectname = self.project_id

        if projectname.turbine_numbers_suggestion == "待提交":
            s = "风能部分"
            raise exceptions.Warning('请完成 %s，并点击 --> 提交报告（%s 位于软件上方，自动编制报告系统右侧）。' % (s, s))
        if projectname.main_booster_station_num == "待提交":
            s = "电一次、二次部分"
            raise exceptions.Warning('请完成 %s，并点击 --> 提交报告（%s 位于软件上方，自动编制报告系统右侧）。' % (s, s))

        if projectname.direct_buried_cable_num == "待提交" or projectname.overhead_line_num == "待提交":
            s = "电气集电线路部分"
            raise exceptions.Warning('请完成 %s，并点击 --> 提交报告（%s 位于软件上方，自动编制报告系统右侧）。' % (s, s))

        self.turbine_numbers = projectname.turbine_numbers_suggestion
        self.name_tur_suggestion = projectname.name_tur_suggestion
        self.hub_height_suggestion = projectname.hub_height_suggestion
        self.ProjectLevel_all = self.env['auto_word_civil.design_safety_standard'].search(
            [('civil_id.project_id.project_name', '=', self.project_id.project_name)])

        if projectname.line_1 == "待提交":
            self.line_1 = 0
        else:
            self.line_1 = projectname.line_1

        if projectname.line_2 == "待提交":
            self.line_2 = 0
        else:
            self.line_2 = projectname.line_2

        self.overhead_line_num = projectname.overhead_line_num
        self.direct_buried_cable_num = projectname.direct_buried_cable_num
        self.main_booster_station_num = projectname.main_booster_station_num

        self.TurbineCapacity = projectname.capacity_suggestion
        self.TerrainType = projectname.TerrainType

        civil_generate_docx_dict(self)

        if self.dict_8_submit_words == False:
            raise exceptions.Warning('计算出错，请查询填写参数是否正确' % (s))
        dict_8_submit_words=eval(self.dict_8_submit_words)

        self.EarthExcavation_WindResource = dict_8_submit_words['土方开挖_风机_numbers']
        self.StoneExcavation_WindResource = dict_8_submit_words['石方开挖_风机_numbers']
        self.EarthWorkBackFill_WindResource = dict_8_submit_words['土石方回填_风机_numbers']
        self.Volume = dict_8_submit_words['C40混凝土_风机_numbers']
        self.Cushion = dict_8_submit_words['C15混凝土_风机_numbers']
        self.Reinforcement = dict_8_submit_words['钢筋_风机_numbers']
        self.SinglePileLength = dict_8_submit_words['预制桩长_风机_numbers']
        self.M48PreStressedAnchor = dict_8_submit_words['M48预应力锚栓_风机_numbers']
        self.C80SecondaryGrouting = dict_8_submit_words['C80二次灌浆_风机_numbers']
        self.stake_number = dict_8_submit_words['单台风机桩根数_风机']

        self.turbine_foundation_box_voltage_excavation = dict_8_submit_words['风机基础及箱变_开挖']
        self.turbine_foundation_box_voltage_back_fill = dict_8_submit_words['风机基础及箱变_回填']
        self.turbine_foundation_box_voltage_spoil = dict_8_submit_words['风机基础及箱变_弃土']
        self.booster_station_engineering_excavation = dict_8_submit_words['升压站工程_开挖']
        self.booster_station_engineering_back_fill = dict_8_submit_words['升压站工程_回填']
        self.booster_station_engineering_spoil = dict_8_submit_words['升压站工程_弃土']

        self.road_engineering_excavation = dict_8_submit_words['道路工程_开挖']
        self.road_engineering_back_fill = dict_8_submit_words['道路工程_回填']
        self.road_engineering_spoil = dict_8_submit_words['道路工程_弃土']
        self.hoisting_platform_excavation = dict_8_submit_words['吊装平台_开挖']
        self.hoisting_platform_back_fill = dict_8_submit_words['吊装平台_回填']
        self.hoisting_platform_spoil = dict_8_submit_words['吊装平台_弃土']
        self.total_line_excavation = dict_8_submit_words['集电线路_开挖']
        self.total_line_back_fill = dict_8_submit_words['集电线路_回填']
        self.total_line_spoil = dict_8_submit_words['集电线路_弃土']
        self.sum_EarthStoneBalance_excavation = dict_8_submit_words['合计_开挖']
        self.sum_EarthStoneBalance_back_fill = dict_8_submit_words['合计_回填']
        self.sum_EarthStoneBalance_spoil = dict_8_submit_words['合计_弃土']

        self.temporary_land_area = dict_8_submit_words['合计亩_临时用地面积']
        self.permanent_land_area = dict_8_submit_words['合计亩_永久用地面积']
        self.land_area = round_up(float(self.permanent_land_area) + float(self.temporary_land_area), 2)

    #   生成报告
    def civil_generate(self):
        # dict_8_words, dict_8_word = civil_generate_docx_dict(self)
        path_chapter_8 = self.env['auto_word.project'].path_chapter_8
        generate_civil_docx(eval(self.dict_8_submit_words), path_chapter_8, 'cr8', 'result_chapter8')
        reportfile_name = open(
            file=os.path.join(path_chapter_8, '%s.docx') % 'result_chapter8',
            mode='rb')
        byte = reportfile_name.read()
        reportfile_name.close()
        print('file lenth=', len(byte))
        base64.standard_b64encode(byte)
        if (str(self.report_attachment_id) == 'ir.attachment()'):
            Attachments = self.env['ir.attachment']
            print('开始创建新纪录')
            New = Attachments.create({
                'name': self.project_id.project_name + '可研报告土建章节下载页',
                'datas_fname': self.project_id.project_name + '可研报告土建章节.docx',
                'datas': base64.standard_b64encode(byte),
                'display_name': self.project_id.project_name + '可研报告土建章节',
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


class civil_boosterstation(models.Model):
    _name = 'auto_word_civil.boosterstation'
    _description = 'Civil boosterstation'
    _rec_name = 'Grade'
    Status = fields.Char(string=u"状态", required=True)
    Grade = fields.Char(string=u"升压站等级", required=True)
    Capacity = fields.Char(string=u"容量", required=True)
    Long = fields.Float(u'长')
    Width = fields.Float(u'宽')
    InnerWallArea = fields.Float(u'围墙内面积')
    WallLength = fields.Float(u'围墙长度')
    StoneMasonryFoot = fields.Float(u'浆砌石护脚')
    StoneMasonryDrainageDitch = fields.Float(u'浆砌石排水沟')
    RoadArea = fields.Float(u'道路面积')
    GreenArea = fields.Float(u'绿化面积')
    ComprehensiveBuilding = fields.Float(u'综合楼')
    EquipmentBuilding = fields.Float(u'设备楼')
    AffiliatedBuilding = fields.Float(u'附属楼')
    C30Concrete = fields.Float(u'主变基础C30混凝土')
    C15ConcreteCushion = fields.Float(u'C15混凝土垫层')
    MainTransformerFoundation = fields.Float(u'主变压器基础钢筋')
    AccidentOilPoolC30Concrete = fields.Float(u'事故油池C30混凝土')
    AccidentOilPoolC15Cushion = fields.Float(u'事故油池C15垫层')
    AccidentOilPoolReinforcement = fields.Float(u'事故油池钢筋')
    FoundationC25Concrete = fields.Float(u'设备及架构基础C25混凝土')
    OutdoorStructure = fields.Float(u'室外架构（型钢）')
    PrecastConcretePole = fields.Float(u'预制混凝土杆')
    LightningRod = fields.Float(u'避雷针')


class auto_word_civil_road1(models.Model):
    _name = 'auto_word_civil.road1'
    _description = 'Civil road1'
    _rec_name = 'TerrainType'
    TerrainType = fields.Selection(
        [("平原", u"平原"), ("丘陵", u"丘陵"), ("缓坡低山", u"缓坡低山"), ("陡坡低山", u"陡坡低山"), ("缓坡中山", u"缓坡中山"),
         ("陡坡中山", u"陡坡中山"), ("缓坡高山", u"缓坡高山"), ("陡坡高山", u"陡坡高山")], string=u"山地类型", required=True)
    GradedGravelPavement_1 = fields.Float(u'级配碎石路面(20cm厚)')
    RoundTubeCulvert_1 = fields.Float(u'D1000mm圆管涵')
    StoneMasonryDrainageDitch_1 = fields.Float(u'浆砌石排水沟')
    MortarStoneRetainingWall_1 = fields.Float(u'M7.5浆砌片石挡墙')
    TurfSlopeProtection_1 = fields.Float(u'草皮护坡')


class auto_word_civil_road2(models.Model):
    _name = 'auto_word_civil.road2'
    _description = 'Civil road2'
    _rec_name = 'TerrainType'
    TerrainType = fields.Selection(
        [("平原", u"平原"), ("丘陵", u"丘陵"), ("缓坡低山", u"缓坡低山"), ("陡坡低山", u"陡坡低山"), ("缓坡中山", u"缓坡中山"),
         ("陡坡中山", u"陡坡中山"), ("缓坡高山", u"缓坡高山"), ("陡坡高山", u"陡坡高山")], string=u"山地类型", required=True)
    GradedGravelBase_2 = fields.Float(u'级配碎石基层(20cm厚)')
    C30ConcretePavement_2 = fields.Float(u'C30混凝土路面(20cm厚)')
    RoundTubeCulvert_2 = fields.Float(u'D1000mm圆管涵')
    StoneMasonryDrainageDitch_2 = fields.Float(u'浆砌石排水沟')
    MortarStoneRetainingWall_2 = fields.Float(u'M7.5浆砌片石挡墙')
    TurfSlopeProtection_2 = fields.Float(u'草皮护坡')
    Signage_2 = fields.Float(u'标志标牌')
    WaveGuardrail_2 = fields.Float(u'波形护栏')


class auto_word_civil_road3(models.Model):
    _name = 'auto_word_civil.road3'
    _description = 'Civil road3'
    _rec_name = 'TerrainType'
    TerrainType = fields.Selection(
        [("平原", u"平原"), ("丘陵", u"丘陵"), ("缓坡低山", u"缓坡低山"), ("陡坡低山", u"陡坡低山"), ("缓坡中山", u"缓坡中山"),
         ("陡坡中山", u"陡坡中山"), ("缓坡高山", u"缓坡高山"), ("陡坡高山", u"陡坡高山")], string=u"山地类型", required=True)
    MountainPavement_3 = fields.Float(u'山皮石路面(20cm厚)')
    C30ConcretePavement_3 = fields.Float(u'C30混凝土路面(20cm厚)')
    RoundTubeCulvert_3 = fields.Float(u'D1000mm圆管涵')
    StoneMasonryDrainageDitch_3 = fields.Float(u'浆砌石排水沟')
    MortarStoneRetainingWall_3 = fields.Float(u'M7.5浆砌片石挡墙')
    TurfSlopeProtection_3 = fields.Float(u'草皮护坡')
    Signage_3 = fields.Float(u'标志标牌')
    WaveGuardrail_3 = fields.Float(u'波形护栏')
    LandUse_3 = fields.Float(u'用地')


class auto_word_civil_road4(models.Model):
    _name = 'auto_word_civil.road4'
    _description = 'Civil road4'
    _rec_name = 'TerrainType'
    TerrainType = fields.Selection(
        [("平原", u"平原"), ("丘陵", u"丘陵"), ("缓坡低山", u"缓坡低山"), ("陡坡低山", u"陡坡低山"), ("缓坡中山", u"缓坡中山"),
         ("陡坡中山", u"陡坡中山"), ("缓坡高山", u"缓坡高山"), ("陡坡高山", u"陡坡高山")], string=u"山地类型", required=True)
    GeneralSiteLeveling_4 = fields.Float(u'一般场地平整')
    StoneMasonryDrainageDitch_4 = fields.Float(u'浆砌石排水沟')
    MortarStoneProtectionSlope_4 = fields.Float(u'M7.5浆砌片石护坡')
    TurfSlopeProtection_4 = fields.Float(u'草皮护坡')

# class auto_word_windresourcedatabase(models.Model):
#     _name = 'auto_word_civil.windresourcedatabase'
#     _description = 'WindResourceDatabase'
#     _rec_name = 'project_id'
#
#     project_id = fields.Many2one('auto_word.project', string=u'项目名', required=False)
#     EarthExcavation_WindResource = fields.Char(u'土方开挖')
#     StoneExcavation_WindResource = fields.Char(u'石方开挖')
#     EarthWorkBackFill_WindResource = fields.Char(u'土石方回填')
#
#     Volume = fields.Char(u'C40混凝土')
#     Cushion = fields.Char(u'C15混凝土')
#     Reinforcement = fields.Char(u'钢筋')
#     Based_Waterproof = fields.Char(u'基础防水', default=1)
#     Settlement_Observation = fields.Char(u'沉降观测', default=4)
#
#     SinglePileLength = fields.Char(u'预制桩长')
#     M48PreStressedAnchor = fields.Char(u'M48预应力锚栓')
#     C80SecondaryGrouting = fields.Char(u'C80二次灌浆')
