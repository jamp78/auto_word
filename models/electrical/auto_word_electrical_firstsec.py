# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import exceptions
import doc_6
import base64, os
from docxtpl import DocxTemplate
import pandas as pd
import numpy as np
from RoundUp import round_up
import math


def generate_electrical_docx(Dict, path_images, model_name, outputfile):
    filename_box = [model_name, outputfile]
    read_path = os.path.join(path_images, '%s') % filename_box[0]
    save_path = os.path.join(path_images, '%s') % filename_box[1]
    tpl = DocxTemplate(read_path)
    tpl.render(Dict)
    tpl.save(save_path)


def get_dict_electrical_firstsec(self, index, col_name, data, sheet_name_array):
    self.dict_1_submit_word = self.project_id.dict_1_submit_word
    self.dict_4_submit_word = self.project_id.dict_4_submit_word
    self.dict_5_submit_word = self.project_id.dict_5_submit_word
    self.dict_6_jidian_submit_word = self.project_id.dict_6_jidian_submit_word
    print("check dict_1_submit_word")
    print(self.dict_1_submit_word)
    if self.dict_1_submit_word == False:
        s = "项目"
        raise exceptions.Warning('请点选 %s，并点击 --> 分发信息（%s 位于软件上方，自动编制报告系统右侧）。' % (s, s))
    if self.dict_4_submit_word == False:
        s = "电气部分"
        raise exceptions.Warning('请点选 %s，并点击电气详情 --> 提交报告（%s 位于软件上方，自动编制报告系统右侧）。' % (s, s))
    if self.dict_6_jidian_submit_word == False:
        s = "电气部分"
        raise exceptions.Warning('请点选 %s，并点击集电线路 --> 提交报告（%s 位于软件上方，自动编制报告系统右侧）。' % (s, s))

    if self.dict_5_submit_word == False:
        s = "风能部分"
        raise exceptions.Warning('请点选 %s，并点击风能详情 --> 提交报告（%s 位于软件上方，自动编制报告系统右侧）。' % (s, s))

    result_dict, context = {}, {}
    result_list = []

    result_labels_name = 'result_labels' + str(index)
    result_list_name = 'result_list' + str(index)
    context[result_labels_name] = col_name
    data_np = np.array(data)
    # print(data_np.shape[0], sheet_name_array)
    for i in range(0, data_np.shape[0]):
        key = str(data_np[i, 0])

        if index.strip() == '12_7':
            value = data_np[i, :].tolist()
        else:
            value = data_np[i, 1:].tolist()
        for j in range(0, len(value)):
            if type(value[j]).__name__ == 'float':
                if (index.strip() == '13_4' and i == 1) or ('12' in index.strip()):
                    value[j] = round_up(value[j], 2)
                else:
                    value[j] = round_up(value[j], 1)
        value = [str(i) for i in value]

        result_dict = {'number': key, 'cols': value}
        result_list.append(result_dict)
    context[result_list_name] = result_list

    # key = str(data_np[i, 0]) + "_" + sheet_name
    # value = data_np[i, 1:].tolist()
    # value = [str(i) for i in value]
    # Dict_e[key] = value
    return context


class auto_word_electrical_firstsec(models.Model):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    _name = 'auto_word_electrical.firstsec'
    _description = 'electrical input'
    _rec_name = 'project_id'

    # 提交
    dict_6_submit_word = fields.Char(u'字典6_提交')
    # 提取
    dict_1_submit_word = fields.Char(u'字典1_提交')
    dict_4_submit_word = fields.Char(u'字典4_提交')
    dict_5_submit_word = fields.Char(u'字典5_提交')

    project_id = fields.Many2one('auto_word.project', string='项目名', required=True)
    version_id = fields.Char(u'版本', required=True, default="1.0")
    report_attachment_id_input = fields.Many2many('ir.attachment', string=u'电气提资')
    attachment_number = fields.Integer(compute='_compute_attachment_number', string='Number of Attachments')
    report_attachment_id = fields.Many2one('ir.attachment', string=u'可研报告电气成果')
    ####升压站
    Status = fields.Selection([("新建", u"新建"), ("利用原有", u"利用原有")], string=u"升压站状态", default="新建")
    Grade = fields.Selection([(110, "110"), (220, "220")], string=u"升压站等级", default=110)
    Capacity = fields.Selection([(50, "50"), (100, "100"), (150, "150"), (200, "200")], string=u"升压站容量", default=100)

    Numbers_boxvoltagetype = fields.Integer(string='箱式变电站数量', default="0")
    Numbers_maintransformertype = fields.Integer(string='主变压器数量', default="0")
    Numbers_v110kvswitchgeartype = fields.Integer(string='110kV配电装置数量', default="0")
    Numbers_v110kvarrestertype = fields.Integer(string='110kV避雷器型号数量', default="0")
    Numbers_v35kvtictype = fields.Integer(string='35kV风机进线柜数量', default="0")
    Numbers_v35kvmtovctype = fields.Integer(string='35kV主变出线柜数量', default="0")
    Numbers_v35kvsctype = fields.Integer(string='35kV站用变柜数量', default="0")
    Numbers_v35kvrpcdctype = fields.Integer(string='35kV无功补偿数量', default="0")
    Numbers_v35kvgctype = fields.Integer(string='35kV接地变柜数量', default="0")
    Numbers_v35kvptctype = fields.Integer(string='35kVPT柜数量', default="0")
    Numbers_srgstype = fields.Integer(string='小电阻成套接地装置数量', default="0")
    Numbers_sttype = fields.Integer(string='站用变压器型号数量', default="0")
    Numbers_ccgistype = fields.Integer(string='导体选择1数量', default="0")
    Numbers_ccmtlvtype = fields.Integer(string='导体选择2数量', default="0")

    p1 = fields.Integer(string='P1', default="0")
    p2 = fields.Integer(string='P2', default="0")
    p3 = fields.Integer(string='P3', default="0")
    sum_p = fields.Integer(string='sum_p', default="0")
    sum_pp = fields.Integer(string='sum_pp', default="0")

    boxvoltagetype = fields.Many2one('auto_word_electrical.boxvoltagetype', string='箱式变电站型号', required=False)
    maintransformertype = fields.Many2one('auto_word_electrical.maintransformertype', string='主变压器型号', required=False)
    v110kvswitchgeartype = fields.Many2one('auto_word_electrical.110kvswitchgeartype', string='110kV配电装置型号',
                                           required=False)
    v110kvarrestertype = fields.Many2one('auto_word_electrical.110kvarrestertype', string='110kV避雷器型号', required=False)
    v35kvtictype = fields.Many2one('auto_word_electrical.35kvtictype', string='35kV风机进线柜型号', required=False)
    v35kvmtovctype = fields.Many2one('auto_word_electrical.35kvmtovctype', string='35kV主变出线柜型号', required=False)
    v35kvsctype = fields.Many2one('auto_word_electrical.35kvsctype', string='35kV站用变柜型号', required=False)

    v35kvrpcdctype = fields.Many2one('auto_word_electrical.35kvrpcdctype', string='35kV无功补偿型号', required=False)
    v35kvgctype = fields.Many2one('auto_word_electrical.35kvgctype', string='35kV接地变柜型号', required=False)
    v35kvptctype = fields.Many2one('auto_word_electrical.35kvptctype', string='35kVPT柜型号', required=False)
    srgstype = fields.Many2one('auto_word_electrical.srgstype', string='小电阻成套接地装置型号', required=False)
    sttype = fields.Many2one('auto_word_electrical.sttype', string='站用变压器型号', required=False)
    ccgistype = fields.Many2one('auto_word_electrical.ccgistype', string='导体选择1', required=False)
    ccmtlvtype = fields.Many2one('auto_word_electrical.ccmtlvtype', string='导体选择2', required=False)

    TypeID_boxvoltagetype = 0

    def electrical_firstsec_generate(self):
        dictMerged, Dict, dict_content, dict_head = {}, {}, {}, {}
        col_name_array = []
        # file_first = False
        # file_second = False
        file_exist = False
        for re in self.report_attachment_id_input:
            t = re.name
            chapter_number = 6

            if '电气提资' in t:
                xlsdata = base64.standard_b64decode(re.datas)
                name_first = t
                file_exist = True

        if file_exist == True:
            electrical_path = self.env['auto_word.project'].path_chapter_6
            suffix_in = ".xls"
            suffix_out = ".docx"
            inputfile = name_first + suffix_in
            outputfile = 'result_chapter' + str(chapter_number) + suffix_out
            model_name = 'cr' + str(chapter_number) + suffix_out
            Pathinput = os.path.join(electrical_path, '%s') % inputfile
            Pathoutput = os.path.join(electrical_path, '%s') % outputfile
            if not os.path.exists(Pathinput):
                f = open(Pathinput, 'wb+')
                f.write(xlsdata)
                # if '电气一次' in re.name:
                #     f.write(xlsdata_first)
                # elif '电气二次' in re.name:
                #     f.write(xlsdata_second)
                f.close()
            else:
                # print(Pathinput + " already existed.")
                os.remove(Pathinput)
                f = open(Pathinput, 'wb+')
                f.write(xlsdata)
                # if '电气一次' in re.name:
                #     f.write(xlsdata_first)
                # elif '电气二次' in re.name:
                #     f.write(xlsdata_second)
                f.close()

            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)

            sheet_name_array = ['01站用电负荷表', '02电气一次主要设备及材料表', '03电气二次设备主要材料清单', '04通信部分材料清单'
                , '消防措施', '消防灭火系统主要设备材料表'
                                ]
            for i in range(0, len(sheet_name_array)):
                if i == 0 or i == 4 or i == 5:
                    data = pd.read_excel(Pathinput, header=0, sheet_name=sheet_name_array[i],
                                         skip_footer=2)
                    col_name = data.columns.tolist()
                else:
                    data = pd.read_excel(Pathinput, header=0, sheet_name=sheet_name_array[i], )
                    # usecols=col_name_array[i])
                    col_name = data.columns.tolist()
                    if i == 1:
                        if ~data['数量'].isnull().values.all() == True:
                            take_data = data[data['数量'].isnull().values == True]
                            drop_number = take_data[take_data.ix[:, 0].str.contains("-") == True].index
                        data = data.drop(drop_number)
                        modifier_data = data.ix[:, 0][data.ix[:, 0].str.contains("-") == True]
                        modifier_number_list = modifier_data.index
                        for j in range(0, modifier_data.shape[0]):
                            number = modifier_data.iloc[j].split("-")
                            if j == 0:
                                Judging = number[0]
                                number_add = 1
                                string_number = Judging + "-" + str(number_add)
                                data.ix[modifier_number_list[j], 0] = string_number
                            else:
                                if number[0] == Judging:
                                    number_add = number_add + 1
                                    string_number = Judging + "-" + str(number_add)
                                    data.ix[modifier_number_list[j], 0] = string_number
                                elif number[0] != Judging:
                                    number_add = 1
                                    string_number = number[0] + "-" + str(number_add)
                                    Judging = number[0]
                                    data.ix[modifier_number_list[j], 0] = string_number
                data = data.replace(np.nan, '-', regex=True)
                col_name_array.append(col_name)
                tabel_number = str(chapter_number) + '_' + str(i)
                dict_content = get_dict_electrical_firstsec(self, tabel_number, col_name_array[i], data,
                                                            sheet_name_array[i])

                dictMerged.update(dict_content)

            for i in range(0, len(dictMerged['result_list6_0'])):
                if str(dictMerged['result_list6_0'][i]['cols'][0]) == '室外消防水泵':
                    self.p1 = str(dictMerged['result_list6_0'][i + 1]['cols'][3])
                if str(dictMerged['result_list6_0'][i]['cols'][0]) == '厨房动力':
                    self.p2 = str(dictMerged['result_list6_0'][i + 1]['cols'][3])
                if str(dictMerged['result_list6_0'][i]['cols'][0]) == '户外照明':
                    self.p3 = str(dictMerged['result_list6_0'][i + 1]['cols'][3])

            self.sum_p = 0.85 * float(self.p1) + float(self.p2) + float(self.p3)
            self.sum_pp = math.ceil(self.sum_p / 100) * 100

            dict_6_res_word = {
                '站用电负荷表说明_1': str('1、综合楼空调机为单冷型，该负荷仅在夏季使用；'),
                '站用电负荷表说明_2': str('2、设备楼空调机为冷暖型。'),
                '热镀锌扁钢': str(dictMerged['result_list6_1'][47]['cols'][1]),
                '热镀锌角钢': str(dictMerged['result_list6_1'][48]['cols'][1]),
                'p1': self.p1,
                'p2': self.p2,
                'p3': self.p3,
                'sum_p': self.sum_p,
                'sum_pp': self.sum_pp,
                "升压站等级": self.Grade,
                "升压站数量": self.Numbers_maintransformertype,
                "升压站容量": self.Capacity,
            }

            # 提交的生成chapter6的dict
            dict_6_word = dict(dictMerged, **dict_6_res_word)
            # 生成chapter6 所需要的总的dict
            dict_6_words = dict(dict_6_word, **eval(self.dict_1_submit_word),
                                **eval(self.dict_4_submit_word), **eval(self.dict_5_submit_word),
                                **eval(self.dict_6_jidian_submit_word))

            self.dict_6_submit_word = dict_6_word

            generate_electrical_docx(dict_6_words, electrical_path, model_name, outputfile)
            ###########################

            reportfile_name = open(file=os.path.join(electrical_path, '%s.docx') % 'result_chapter6',
                                   mode='rb')
            byte = reportfile_name.read()
            reportfile_name.close()
            base64.standard_b64encode(byte)
            if (str(self.report_attachment_id) == 'ir.attachment()'):
                Attachments = self.env['ir.attachment']
                print('开始创建新纪录')
                New = Attachments.create({
                    'name': self.project_id.project_name + '可研报告电气章节下载页',
                    'datas_fname': self.project_id.project_name + '可研报告电气章节.docx',
                    'datas': base64.standard_b64encode(byte),
                    'display_name': self.project_id.project_name + '可研报告电气章节',
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

    @api.multi
    def action_get_attachment_electrical_firstsec_view(self):
        """附件上传动作视图"""
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('base', 'action_attachment')
        res['domain'] = [('res_model', '=', 'auto_word_electrical.firstsec'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'auto_word_electrical.firstsec', 'default_res_id': self.id}
        return res

    @api.multi
    def _compute_attachment_number(self):
        """附件上传"""
        attachment_data = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'auto_word_electrical.firstsec'), ('res_id', 'in', self.ids)], ['res_id'],
            ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for expense in self:
            expense.attachment_number = attachment.get(expense.id, 0)

    def submit_electrical_firstsec(self):
        self.project_id.Status = self.Status
        self.project_id.Grade = self.Grade
        self.project_id.Capacity = self.Capacity
        self.project_id.main_booster_station_num = self.Numbers_maintransformertype
        self.project_id.dict_6_submit_word = self.dict_6_submit_word

        self.TypeID_boxvoltagetype = self.boxvoltagetype.TypeID
        self.TypeID_maintransformertype = self.maintransformertype.TypeID
        self.TypeID_v110kvswitchgeartype = self.v110kvswitchgeartype.TypeID
        self.TypeID_v110kvarrestertype = self.v110kvarrestertype.TypeID
        self.TypeID_v35kvtictype = self.v35kvtictype.TypeID
        self.TypeID_v35kvmtovctype = self.v35kvmtovctype.TypeID
        self.TypeID_v35kvsctype = self.v35kvsctype.TypeID
        self.TypeID_v35kvrpcdctype = self.v35kvrpcdctype.TypeID
        self.TypeID_v35kvgctype = self.v35kvgctype.TypeID
        self.TypeID_v35kvptctype = self.v35kvptctype.TypeID
        self.TypeID_srgstype = self.srgstype.TypeID
        self.TypeID_sttype = self.sttype.TypeID
        self.TypeID_ccgistype = self.ccgistype.TypeID
        self.TypeID_ccmtlvtype = self.ccmtlvtype.TypeID

        dict6 = doc_6.generate_electrical_TypeID_dict(
            TypeID_boxvoltagetype=self.TypeID_boxvoltagetype,
            TypeID_maintransformertype=self.TypeID_maintransformertype,
            TypeID_v110kvswitchgeartype=self.TypeID_v110kvswitchgeartype,
            TypeID_v110kvarrestertype=self.TypeID_v110kvarrestertype,
            TypeID_v35kvtictype=self.TypeID_v35kvtictype,
            TypeID_v35kvmtovctype=self.TypeID_v35kvmtovctype,
            TypeID_v35kvsctype=self.TypeID_v35kvsctype,
            TypeID_v35kvrpcdctype=self.TypeID_v35kvrpcdctype,
            TypeID_v35kvgctype=self.TypeID_v35kvgctype,
            TypeID_v35kvptctype=self.TypeID_v35kvptctype,
            TypeID_srgstype=self.TypeID_srgstype,
            TypeID_sttype=self.TypeID_sttype,
            TypeID_ccgistype=self.TypeID_ccgistype,
            TypeID_ccmtlvtype=self.TypeID_ccmtlvtype,

            Numbers_boxvoltagetype=self.Numbers_boxvoltagetype,
            Numbers_maintransformertype=self.Numbers_maintransformertype,
            Numbers_v110kvswitchgeartype=self.Numbers_v110kvswitchgeartype,
            Numbers_v110kvarrestertype=self.Numbers_v110kvarrestertype,
            Numbers_v35kvtictype=self.Numbers_v35kvtictype,
            Numbers_v35kvmtovctype=self.Numbers_v35kvmtovctype,
            Numbers_v35kvsctype=self.Numbers_v35kvsctype,
            Numbers_v35kvptctype=self.Numbers_v35kvptctype,
            Numbers_v35kvgctype=self.Numbers_v35kvgctype,
            Numbers_srgstype=self.Numbers_srgstype,
            Numbers_sttype=self.Numbers_sttype,
            Numbers_ccgistype=self.Numbers_ccgistype,
            Numbers_ccmtlvtype=self.Numbers_ccmtlvtype,
            turbine_numbers=self.project_id.turbine_numbers_suggestion
        )


# 2箱式变电站
class electrical_BoxVoltageType(models.Model):
    _name = 'auto_word_electrical.boxvoltagetype'
    _description = 'electrical_boxvoltagetype'
    _rec_name = 'TypeName'
    TypeID = fields.Integer(u'型号ID')
    TypeName = fields.Char(u'型号')
    Capacity = fields.Integer(u'容量')
    VoltageClasses = fields.Char(u'电压等级')
    WiringGroup = fields.Char(u'接线组别')
    CoolingType = fields.Char(u'冷却方式')
    ShortCircuitImpedance = fields.Char(u'短路阻抗')


# 3主变压器
class electrical_MainTransformerType(models.Model):
    _name = 'auto_word_electrical.maintransformertype'
    _description = 'electrical_maintransformertype'
    _rec_name = 'TypeName'
    TypeID = fields.Integer(u'型号ID')
    TypeName = fields.Char(u'型号')
    RatedCapacity = fields.Integer(u'额定容量')
    RatedVoltageRatio = fields.Char(u'额定电压比')
    WiringGroup = fields.Char(u'接线组别')
    ImpedanceVoltage = fields.Char(u'阻抗电压')
    Noise = fields.Char(u'噪音')
    CoolingType = fields.Char(u'冷却方式')
    OnloadTapChanger = fields.Char(u'有载调压开关')
    MTGroundingMode = fields.Char(u'主变压器接地方式')
    TransformerRatedVoltage = fields.Char(u'变压器额定电压')
    TransformerNPC = fields.Char(u'变压器中性点耐受电流')
    ZincOxideArrester = fields.Char(u'氧化锌避雷器')
    DischargingGap = fields.Char(u'放电间隙')
    CurrentTransformer = fields.Char(u'电流互感器')


# 4.1 110kV配电装置
class electrical_110kVSwitChgearType(models.Model):
    _name = 'auto_word_electrical.110kvswitchgeartype'
    _description = 'electrical_110kvswitchgeartype'
    _rec_name = 'TypeName'
    TypeID = fields.Integer(u'型号ID')
    TypeName = fields.Char(u'型号')
    RatedVoltage = fields.Integer(u'额定电压')
    RatedCurrent = fields.Integer(u'额定电流')
    RatedFrequency = fields.Integer(u'额定频率')
    RatedBreakingCurrent = fields.Integer(u'额定开断电流')
    RatedClosingCurrent = fields.Integer(u'额定关合电流')
    RatedPeakWCurrent = fields.Integer(u'额定峰值耐受电流')
    RatedShortTimeWCurrent = fields.Char(u'额定短时耐受电流')
    LineSpacing = fields.Char(u'出线间隔')
    PTSpacing = fields.Char(u'PT间隔')
    AccuracyClass = fields.Char(u'准确级')


# 4.2 110kV避雷器
class electrical_110kVArresterType(models.Model):
    _name = 'auto_word_electrical.110kvarrestertype'
    _description = 'electrical_110kvarrestertype'
    _rec_name = 'TypeName'
    TypeID = fields.Integer(u'型号ID')
    TypeName = fields.Char(u'型号')
    RatedVoltageArrester = fields.Integer(u'避雷器额定电压')
    OperatingVoltageArrester = fields.Integer(u'避雷器持续运行电压')
    DischargeCurrentArrester = fields.Integer(u'避雷器的标称放电电流')
    LightningResidualVoltage = fields.Integer(u'雷电冲击电流残压')


# 5.1 35kV风机进线柜
class electrical_35kVTICType(models.Model):
    _name = 'auto_word_electrical.35kvtictype'
    _description = 'electrical_35kv_turbine_inlet_cabinet_type'
    _rec_name = 'TypeName'
    TypeID = fields.Integer(u'型号ID')
    TypeName = fields.Char(u'型号')
    RatedVoltage = fields.Float(u'额定电压')
    RatedCurrent = fields.Float(u'额定电流')
    RatedBreakingCurrent = fields.Float(u'额定开断电流')
    DynamicCurrent = fields.Float(u'动稳定电流')
    RatedShortTimeWCurrent = fields.Char(u'额定短时耐受电流')
    CurrentTransformerRatio = fields.Char(u'电流互感器变比')
    CurrentTransformerAccuracyClass = fields.Char(u'电流互感器准确级')
    CurrentTransformerArrester = fields.Char(u'电流互感器避雷器')


# 5.2 35kV主变出线柜
class electrical_35kVMTOCType(models.Model):
    _name = 'auto_word_electrical.35kvmtovctype'
    _description = 'electrical_35kvmain_transformer_outlet_cabinet_type'
    _rec_name = 'TypeName'
    _inherit = ['auto_word_electrical.35kvtictype']


# 5.3 35kV站用变柜
class electrical_35kVSCType(models.Model):
    _name = 'auto_word_electrical.35kvsctype'
    _description = 'electrical_35kstation_cabinet_type'
    _rec_name = 'TypeName'
    _inherit = ['auto_word_electrical.35kvtictype']


# 5.4 35kV无功补偿装置柜
class electrical_35kVRPCDCType(models.Model):
    _name = 'auto_word_electrical.35kvrpcdctype'
    _description = 'electrical_35kReactive power compensation device cabinet_type'
    _rec_name = 'TypeName'
    _inherit = ['auto_word_electrical.35kvtictype']


# 5.5 35kV接地变柜
class electrical_35kVGCType(models.Model):
    _name = 'auto_word_electrical.35kvgctype'
    _description = 'electrical_35kGrounding_cabinet_type'
    _rec_name = 'TypeName'
    _inherit = ['auto_word_electrical.35kvtictype']


# 5.6 35kVPT柜
class electrical_35kVPTCType(models.Model):
    _name = 'auto_word_electrical.35kvptctype'
    _description = 'electrical_35kPT_cabinet_type'
    _rec_name = 'TypeName'
    _inherit = ['auto_word_electrical.35kvtictype']
    CurrentTransformer = fields.Char(u'电流互感器')
    AccuracyClass = fields.Char(u'准确级')
    HighVoltageFuse = fields.Char(u'高压熔断器')


# 6 小电阻成套接地装置
class electrical_SRGSType(models.Model):
    _name = 'auto_word_electrical.srgstype'
    _description = 'electrical_small resistance grounding set_type'
    _rec_name = 'TypeName'
    TypeID = fields.Integer(u'型号ID')
    TypeName = fields.Char(u'型号')
    RatedVoltage = fields.Integer(u'额定电压')
    RatedCapacity = fields.Integer(u'额定容量')
    EarthResistanceCurrent = fields.Float(u'入地阻性电流')
    ResistanceTolerance = fields.Float(u'电阻阻值')
    FlowTime = fields.Float(u'通流时间')


# 7 站用变压器
class electrical_STType(models.Model):
    _name = 'auto_word_electrical.sttype'
    _description = 'electrical_station transformer_type'
    _rec_name = 'TypeName'
    TypeID = fields.Integer(u'型号ID')
    TypeName = fields.Char(u'型号')
    Capacity = fields.Integer(u'容量')
    RatedVoltage = fields.Integer(u'额定电压')
    RatedVoltageTapRange = fields.Char(u'额定电压分接范围')
    ImpedanceVoltage = fields.Char(u'阻抗电压')
    JoinGroups = fields.Char(u'联接组别')


# 9.1 导体选择 GIS设备与主变压器间的连接线
class electrical_CCGISType(models.Model):
    _name = 'auto_word_electrical.ccgistype'
    _description = 'electrical_Conductor choice GIS_type'
    _rec_name = 'ConductorName'
    TypeID = fields.Integer(u'型号ID')
    ConductorName = fields.Char(u'导体材料')
    TypeName = fields.Char(u'型号')


# 9.2 导体选择 主变出线柜与主变压器低压侧的连接线
class electrical_CCMTLVType(models.Model):
    _name = 'auto_word_electrical.ccmtlvtype'
    _description = 'electrical_Conductor choice line between main transformer outlet cabinet and the low-voltage side_type'
    _rec_name = 'TypeName'
    TypeID = fields.Integer(u'型号ID')
    TypeName = fields.Char(u'型号')
    RatedVoltage = fields.Integer(u'额定电压')
    MaximumOperatingVoltage = fields.Float(u'最高运行电压')
    RatedCurrent = fields.Integer(u'额定电流')
    RatedThermalStabilityCurrent = fields.Float(u'额定热稳定电流')
    RatedDynamicCurrent = fields.Float(u'额定动稳定电流')
