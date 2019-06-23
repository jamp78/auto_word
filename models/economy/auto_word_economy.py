# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
import sys, win32ui, os
from docxtpl import DocxTemplate, InlineImage

sys.path.append(r'H:\GOdoo12_community\myaddons\auto_word\models\wind')
import doc_5
import pandas as pd
import numpy as np

sys.path.append(r'H:\GOdoo12_community\myaddons\auto_word\models\source')
from RoundUp import round_up, Get_Average, Get_Sum


def get_dict_economy(index, col_name, data, sheet_name_array):
    result_dict, context = {}, {}
    result_list = []

    result_labels_name = 'result_labels' + str(index)
    result_list_name = 'result_list' + str(index)
    context[result_labels_name] = col_name
    data_np = np.array(data)
    print(data_np.shape[0], sheet_name_array)
    for i in range(0, data_np.shape[0]):
        key = str(data_np[i, 0])

        value = data_np[i, 1:].tolist()
        for j in range(0, len(value)):
            if type(value[j]).__name__ == 'float':
                value[j] = round_up(value[j], 3)
        value = [str(i) for i in value]

        result_dict = {'number': key, 'cols': value}
        result_list.append(result_dict)
    context[result_list_name] = result_list

    # key = str(data_np[i, 0]) + "_" + sheet_name
    # value = data_np[i, 1:].tolist()
    # value = [str(i) for i in value]
    # Dict_e[key] = value
    return context


def get_dict_economy_head(col_name, sheet_name):
    Dict_h = {}
    data_np = np.array(col_name)
    key = str(data_np[0]) + "_" + sheet_name
    value = data_np[1:].tolist()
    value = [str(i) for i in value]
    Dict_h[key] = value
    return Dict_h


def generate_economy_docx(Dict, path_images, model_name, outputfile):
    filename_box = [model_name, outputfile]
    read_path = os.path.join(path_images, '%s') % filename_box[0]
    save_path = os.path.join(path_images, '%s') % filename_box[1]
    tpl = DocxTemplate(read_path)
    tpl.render(Dict)
    tpl.save(save_path)


class auto_word_economy(models.Model):
    _name = 'auto_word.economy'
    _description = 'economy res'
    _rec_name = 'content_id'
    # 项目参数
    project_id = fields.Many2one('auto_word.project', string=u'项目名', required=True)
    content_id = fields.Selection([("风能", u"风能"), ("电气", u"电气"), ("土建", u"土建"),
                                   ("经评", u"经评"), ("其他", u"其他")], string=u"章节分类", required=True)
    version_id = fields.Char(u'版本', required=True, default="1.0")
    report_attachment_id = fields.Many2one('ir.attachment', string=u'可研报告经评章节')
    report_attachment_id3 = fields.Many2many('ir.attachment', string=u'经济性评价结果')
    attachment_number = fields.Integer(compute='_compute_attachment_number', string='Number of Attachments')
    xls_list = []

    def economy_generate(self):
        chapter_number = 0
        for re in self:
            xlsdata = base64.standard_b64decode(re.report_attachment_id3.datas)
            t = re.report_attachment_id3.name
            if '概算' in t:
                chapter_number = 12
            elif '经济评价' in t:
                chapter_number = 13
            economy_path = r'H:\GOdoo12_community\myaddons\auto_word\models\economy\chapter_'+str(chapter_number)

            print('33333333333333')
            print(economy_path)

            suffix_in = ".xls"
            suffix_out = ".docx"
            inputfile = t + suffix_in
            outputfile = 'result_chapter' + str(chapter_number) + suffix_out
            model_name = 'cr' + str(chapter_number) + suffix_out
            Pathinput = os.path.join(economy_path, '%s') % inputfile
            Pathoutput = os.path.join(economy_path, '%s') % outputfile
            if not os.path.exists(Pathinput):
                f = open(Pathinput, 'wb+')
                f.write(xlsdata)
                f.close()
            else:
                print(Pathinput + " already existed.")
                os.remove(Pathinput)
                f = open(Pathinput, 'wb+')
                f.write(xlsdata)
                f.close()
            self.xls_list.append(t)

            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)
            dictMerged, Dict, dict_content, dict_head = {}, {}, {}, {}
            if chapter_number == 12:
                col_name_2 = ['序号', '项目名称', '设备购置费(万元)', '建安工程费(万元)', '其他费用(万元)', '合计(万元)', '占总投资比例(%)']
                col_name_3 = ['序号', '项目名称', '单位', '数量', '单价(元)', '合计(万元)']
                col_name_4 = ['序号', '名称及规格', '单位', '数量', '设备费（单价）', '安装费（单价）', '设备费（合计）', '安装费（合计）']
                col_name_5 = ['序号', '工程或费用名称', '单位', '数量', '单价(元)', '合计(万元)']
                col_name_6 = ['序号', '工程或费用名称', '单位', '数量', '单价(万元)', '合计(万元)']
                col_name_7 = ['序号', '工程名称', '工程投资', '第1年', '第2年']
                col_name_8 = ['编号', '工程名称', '单位', '单价', '人工费', '材料费', '机械使用费', '装置性材料费',
                              '措施费', '间接费', '利润', '税金']
                col_name_9 = ['编号', '工程名称', '单位', '单价', '人工费', '材料费', '机械使用费', '中间单价',
                              '措施费', '间接费', '利润', '税金']
                col_name_10 = ['序号', '钢筋(t)', '水泥(t)', '桩(m)', '钢材(t)', '电缆(km)']
                col_name_11 = ['编号', '名称及规格', '台时费', '折旧费', '修理费', '安装拆卸费', '人工费', '动力燃料费',
                               '其他费用']
                col_name_12 = ['编号', '名称及规格', '单位', '预算价格', '原价依据', '原价(元)', '运杂费(元)', '采购及保管费(元)']
                col_name_13 = ['编号', '混凝土强度 水泥标号 级配', '水泥(kg)', '掺和料(kg)', '砂(m³)', '石子(m³)', '外加剂(kg)',
                               '水(m³)', '单价(元)']

                col_name_array = [col_name_2, col_name_3, col_name_4, col_name_5, col_name_6, col_name_7,
                                  col_name_8, col_name_9, col_name_10, col_name_11, col_name_12, col_name_13]
                sheet_name_array = ['工程总概算表', '施工辅助工程概算表', '设备及安装工程概算表', '建筑工程概算表',
                                    '其他费用概算表', '分年度投资表', '安装工程单价汇总表', '建筑工程单价汇总表',
                                    '主要材料用量汇总表', '施工机械台时费汇总表', '主要材料预算价格计算表',
                                    '混凝土材料单价计算表']
                for i in range(0, len(sheet_name_array)):
                    # print(sheet_name_array[i], i)
                    if i == 2 or i == 5 or i == 9 or i == 10 or i == 11:
                        data = pd.read_excel(Pathinput, header=2, sheet_name=sheet_name_array[i],
                                             usecols=col_name_array[i])

                    elif i == 6 or i == 7:
                        data = pd.read_excel(Pathinput, header=3, sheet_name=sheet_name_array[i],
                                             usecols=col_name_array[i])
                    else:
                        data = pd.read_excel(Pathinput, header=1, sheet_name=sheet_name_array[i],
                                             usecols=col_name_array[i])
                    data = data.replace(np.nan, '-', regex=True)
                    # if i == 2:
                    #     print(data)
                    dict_content = get_dict_economy(i, col_name_array[i], data, sheet_name_array[i])
                    # Dict_head = get_dict_economy_head(col_name_array[i], sheet_name_array[i])
                    # Dict = dict(Dict_content, **Dict_head)
                    dictMerged.update(dict_content)
                # print(dictMerged)

            generate_economy_docx(dictMerged, economy_path, model_name, outputfile)

            # ###########################

            reportfile_name = open(file=Pathoutput, mode='rb')
            byte = reportfile_name.read()
            reportfile_name.close()
            print('file lenth=', len(byte))
            base64.standard_b64encode(byte)
            if (str(self.report_attachment_id) == 'ir.attachment()'):
                Attachments = self.env['ir.attachment']
                print('开始创建新纪录')
                New = Attachments.create({
                    'name': self.project_id.project_name + '可研报告经评章节chapter' + str(chapter_number) + '下载页',
                    'datas_fname': self.project_id.project_name + '可研报告经评章节chapter' + str(chapter_number) + '.docx',
                    'datas': base64.standard_b64encode(byte),
                    'display_name': self.project_id.project_name + '可研报告经评章节',
                    'create_date': fields.date.today(),
                    'public': True,  # 此处需设置为true 否则attachments.read  读不到
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
    def action_get_attachment_economy_view(self):
        """附件上传动作视图"""
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('base', 'action_attachment')
        res['domain'] = [('res_model', '=', 'auto_word.economy'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'auto_word.economy', 'default_res_id': self.id}
        return res

    @api.multi
    def _compute_attachment_number(self):
        """附件上传"""
        attachment_data = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'auto_word.economy'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for expense in self:
            expense.attachment_number = attachment.get(expense.id, 0)
