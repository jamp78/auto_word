# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
import sys,win32ui
sys.path.append(r'D:\GOdoo12_community\myaddons\auto_word\models\wind')
import tkinter as tk
import doc_5

# class Ui_MainWindow(object):
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(800, 600)
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.label = QtWidgets.QLabel(self.centralwidget)
#         self.label.setGeometry(QtCore.QRect(240, 80, 72, 15))
#         self.label.setObjectName("label")
#         self.pushButton = QtWidgets.QPushButton(self.centralwidget)
#         self.pushButton.setGeometry(QtCore.QRect(240, 120, 93, 28))
#         self.pushButton.setObjectName("pushButton")
#         MainWindow.setCentralWidget(self.centralwidget)
#         self.menubar = QtWidgets.QMenuBar(MainWindow)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
#         self.menubar.setObjectName("menubar")
#         MainWindow.setMenuBar(self.menubar)
#         self.statusbar = QtWidgets.QStatusBar(MainWindow)
#         self.statusbar.setObjectName("statusbar")
#         MainWindow.setStatusBar(self.statusbar)
#
#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)
#
#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
#         self.label.setText(_translate("MainWindow", "TextLabel"))
#         self.pushButton.setText(_translate("MainWindow", "PushButton"))
#
# class MyWindow(QMainWindow, Ui_MainWindow):
#     def __init__(self, parent=None):
#         super(MyWindow, self).__init__(parent)
#         self.setupUi(self)


class auto_word_wind(models.Model):
    _name = 'auto_word.wind'
    _description = 'Wind energy input'
    _rec_name = 'content_id'
    project_id = fields.Many2one('auto_word.project', string=u'项目名', required=True)
    content_id = fields.Selection([("风能", u"风能"), ("电气", u"电气"), ("土建", u"土建"),
                                   ("其他", u"其他")], string=u"章节分类", required=True)
    version_id = fields.Char(u'版本', required=True, default="1.0")

    IECLevel = fields.Selection([("IA", u"IA"), ("IIA", u"IIA"), ("IIIA", u"IIIA"),
                                 ("IB", u"IB"), ("IIB", u"IIB"), ("IIIB", u"IIIB"),
                                 ("IC", u"IC"), ("IIC", u"IIC"), ("IIIC", u"IIIC"),
                                 ], string=u"IEC等级", default="IIIB", required=True)
    farm_elevation = fields.Char(string=u'海拔高程', default="510~680", required=True)
    farm_area = fields.Char(string=u'区域面积', default="150", required=True)
    farm_speed_range = fields.Char(string=u'风速区间', default="5.2~6.4", required=True)
    report_attachment_id = fields.Many2one('ir.attachment', string=u'可研报告风能章节')


    select_turbine_ids = fields.Many2many('auto_word_wind.turbines', string=u'机组选型')

    # name_tur_selection = fields.Char(string=u'风机比选型号', readonly=True, default="待提交")
    string_speed_words = fields.Char(string=u'测风塔选定风速结果', default="待提交")
    string_deg_words = fields.Char(string=u'测风塔选定风向结果', default="待提交")

    cft_name_words = fields.Char(string=u'测风塔名字', default="待提交")
    case_number = fields.Char(string=u'方案数', default="待提交")

    case_names = fields.Many2many('auto_word_wind_turbines.compare',string=u'方案比选')


    #机型推荐
    compare_id = fields.Many2one('auto_word_wind_turbines.compare', string=u'方案名')

    # case_name_suggestion = fields.Char(u'方案名称', compute='_compute_compare_case', readonly=True)
    name_tur_suggestion = fields.Char(u'推荐机型', compute='_compute_compare_case', readonly=True)
    turbine_numbers_suggestion = fields.Char(u'机位数', compute='_compute_compare_case', readonly=True)
    hub_height_suggestion = fields.Char(u'推荐轮毂高度', compute='_compute_compare_case', readonly=True)
    rotor_diameter_suggestion = fields.Char(string=u'叶轮直径', readonly=True, default="待提交",
                                            compute='_compute_compare_case')
    farm_capacity = fields.Char(string=u'风电场容量', readonly=True, compute='_compute_compare_case', default="待提交")

    file_excel_path = fields.Char(u'文件路径')

    @api.depends('compare_id')
    def _compute_compare_case(self):
        for re in self:
            # re.case_name_suggestion = re.compare_id.case_name #？？？？？？？？？
            re.name_tur_suggestion = re.compare_id.name_tur
            re.hub_height_suggestion = re.compare_id.hub_height_suggestion
            re.turbine_numbers_suggestion = re.compare_id.turbine_numbers
            re.farm_capacity = re.compare_id.farm_capacity
            re.rotor_diameter_suggestion = re.compare_id.rotor_diameter_case

            # re.case_name = re.compare_id.case_name
            # re.investment_E1 = re.compare_id.investment_E1
            # re.investment_E2 = re.compare_id.investment_E2
            # re.investment_E3 = re.compare_id.investment_E3
            # re.investment_E4 = re.compare_id.investment_E4
            # re.investment_E5 = re.compare_id.investment_E5
            # re.investment_E6 = re.compare_id.investment_E6
            # re.investment_E7 = re.compare_id.investment_E7
            # re.investment = re.compare_id.investment
            # re.investment_unit = re.compare_id.investment_unit


    @api.multi
    def button_wind(self):
        projectname = self.project_id
        myself = self
        projectname.wind_attachment_id = myself
        projectname.wind_attachment_ok = u"已提交,版本：" + self.version_id
        projectname.turbine_numbers_suggestion = self.turbine_numbers_suggestion
        projectname.hub_height_suggestion = self.hub_height_suggestion
        projectname.project_capacity = self.farm_capacity
        # projectname.name_tur_selection = self.name_tur_selection
        projectname.name_tur_suggestion = self.name_tur_suggestion

        projectname.case_name = self.compare_id.case_name
        projectname.investment_E1 = self.compare_id.investment_E1
        projectname.investment_E2 = self.compare_id.investment_E2
        projectname.investment_E3 = self.compare_id.investment_E3
        projectname.investment_E4 = self.compare_id.investment_E4
        projectname.investment_E5 = self.compare_id.investment_E5
        projectname.investment_E6 = self.compare_id.investment_E6
        projectname.investment_E7 = self.compare_id.investment_E7
        projectname.investment = self.compare_id.investment
        projectname.investment_unit = self.compare_id.investment_unit




        return True

    @api.multi
    def wind_open(self):
        dlg = win32ui.CreateFileDialog(1)
        dlg.SetOFNInitialDir("C:")
        flag = dlg.DoModal()
        print(flag)
        if 1 == flag:
            filename=dlg.GetPathName()
        else:
            print("取消打开...")
        self.file_excel_path=filename

    def wind_generate(self):
        tur_name = []
        for i in range(0, len(self.select_turbine_ids)):
            tur_name.append(self.select_turbine_ids[i].name_tur)
        path_images = r"D:\GOdoo12_community\myaddons\auto_word\models\wind\chapter_5"

        case_name_dict, name_tur_dict, turbine_numbers_dict, capacity_dict = [], [], [], []
        farm_capacity_dict, rotor_diameter_dict, tower_weight_dict = [], [], []
        case_hub_height_dict, power_generation_dict, weak_dict = [], [], []
        power_hours_dict, investment_dict, investment_unit_dict = [], [], []
        investment_E1_dict, investment_E2_dict, investment_E3_dict = [], [], []
        investment_E4_dict, investment_E5_dict, investment_E6_dict, investment_E7_dict = [], [], [], []
        investment_turbines_kws_dict = []
        for i in range(0, len(self.case_names)):
            case_name_dict.append(self.case_names[i].case_name)
            name_tur_dict.append('WTG' + str(int(i + 1)))
            turbine_numbers_dict.append(self.case_names[i].turbine_numbers)
            capacity_dict.append(self.case_names[i].capacity)
            farm_capacity_dict.append(self.case_names[i].farm_capacity)
            rotor_diameter_dict.append(self.case_names[i].rotor_diameter_case)
            case_hub_height_dict.append(self.case_names[i].hub_height_suggestion)
            power_generation_dict.append(self.case_names[i].power_generation)
            weak_dict.append(self.case_names[i].weak)
            power_hours_dict.append(self.case_names[i].power_hours)
            tower_weight_dict.append(str(self.case_names[i].tower_weight))
            investment_E1_dict.append(str(self.case_names[i].investment_E1))
            investment_E2_dict.append(str(self.case_names[i].investment_E2))
            investment_E3_dict.append(str(self.case_names[i].investment_E3))
            investment_E4_dict.append(str(self.case_names[i].investment_E4))
            investment_E5_dict.append(str(self.case_names[i].investment_E5))
            investment_E6_dict.append(str(self.case_names[i].investment_E6))
            investment_E7_dict.append(str(self.case_names[i].investment_E7))

            investment_dict.append(str(self.case_names[i].investment))
            investment_unit_dict.append(str(self.case_names[i].investment_unit))

            investment_turbines_kws_dict.append(str(self.case_names[i].investment_turbines_kws))
        dict5 = doc_5.generate_wind_dict(tur_name, path_images)
        dict_5_word = {
            "最终方案": self.project_id.case_name,
            "方案e": case_name_dict,
            "风机类型e": name_tur_dict,
            "风机台数e": turbine_numbers_dict,
            "单机容量e": capacity_dict,
            "装机容量e": farm_capacity_dict,
            "叶轮直径e": rotor_diameter_dict,
            "轮毂高度e": case_hub_height_dict,
            "上网电量e": power_generation_dict,
            "尾流衰减e": weak_dict,
            "满发小时e": power_hours_dict,
            "塔筒重量e": tower_weight_dict,
            "风机投资e": investment_turbines_kws_dict,
            "塔筒投资e": investment_E1_dict,
            "风机设备投资e": investment_E2_dict,
            "基础投资e": investment_E3_dict,
            "道路投资e": investment_E4_dict,
            "吊装费用e": investment_E5_dict,
            "箱变投资e": investment_E6_dict,
            "集电线路e": investment_E7_dict,
            "发电部分投资e": investment_dict,
            "单位度电投资e": investment_unit_dict,

            "叶轮直径": self.rotor_diameter_suggestion,
            "方案数": self.case_number,
            "海拔高程": self.farm_elevation,
            "区域面积": self.farm_area,
            "平均风速区间": self.farm_speed_range,
            '测风塔名字': self.cft_name_words,
            '测风塔风速信息': self.string_speed_words,
            '测风塔风向信息': self.string_deg_words,
            '推荐轮毂高度': self.hub_height_suggestion,
            'IEC等级': self.IECLevel,
        }
        Dict5 = dict(dict_5_word, **dict5)
        print(Dict5)
        doc_5.generate_wind_docx(Dict5, path_images)
        ###########################

        reportfile_name = open(
            file=r'D:\GOdoo12_community\myaddons\auto_word\models\wind\chapter_5\result_chapter5.docx',
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
