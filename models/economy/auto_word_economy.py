# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
import sys, win32ui, os
from docxtpl import DocxTemplate, InlineImage

sys.path.append(r'D:\GOdoo12_community\myaddons\auto_word\models\wind')
import doc_5
import pandas as pd
import numpy as np


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
        economy_images = r"D:\GOdoo12_community\myaddons\auto_word\models\economy\chapter_12"

        xlsdata = base64.standard_b64decode(self.report_attachment_id3.datas)
        t = self.report_attachment_id3.name
        suffix_in = ".xls"
        suffix_out = ".docx"
        inputfile = t + suffix_in
        outputfile = 'result_chapter12' + suffix_out
        Pathinput = os.path.join(economy_images, '%s') % inputfile
        Pathoutput = os.path.join(economy_images, '%s') % outputfile
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
        col_name_2 = ['项目名称', '设备购置费(万元)', '建安工程费(万元)', '其他费用(万元)', '合计(万元)', '占总投资比例(%)']
        col_name_3 = ['项目名称', '单位', '数量', '单价(元)', '合计(万元)']

        data_2 = pd.read_excel(Pathinput,
                               header=1, sheet_name='工程总概算表', usecols=col_name_2)
        data_3 = pd.read_excel(Pathinput,
                               header=1, sheet_name='施工辅助工程概算表', usecols=col_name_3)

        # data_4 = pd.read_excel(Pathinput,
        #                        header=1, sheet_name='设备及安装工程概算表', usecols=col_name)
        # data_5 = pd.read_excel(Pathinput,
        #                        header=1, sheet_name='建筑工程概算表', usecols=col_name)
        # data_6 = pd.read_excel(Pathinput,
        #                        header=1, sheet_name='其他费用概算表', usecols=col_name)
        # data_7 = pd.read_excel(Pathinput,
        #                        header=1, sheet_name='分年度投资表', usecols=col_name)
        # data_8 = pd.read_excel(Pathinput,
        #                        header=1, sheet_name='安装工程单价汇总表', usecols=col_name)
        # data_9 = pd.read_excel(Pathinput,
        #                        header=1, sheet_name='建筑工程单价汇总表', usecols=col_name)
        # data_10 = pd.read_excel(Pathinput,
        #                         header=1, sheet_name='主要材料用量汇总表', usecols=col_name)
        # data_11 = pd.read_excel(Pathinput,
        #                         header=1, sheet_name='施工机械台时费汇总表', usecols=col_name)
        # data_12 = pd.read_excel(Pathinput,
        #                         header=1, sheet_name='主要材料预算价格计算表', usecols=col_name)
        # data_13 = pd.read_excel(Pathinput,
        #                         header=1, sheet_name='混凝土材料单价计算表', usecols=col_name)
        # data_14 = pd.read_excel(Pathinput,
        #                         header=1, sheet_name='材料运输费用计算表', usecols=col_name)
        # data_15 = pd.read_excel(Pathinput,
        #                         header=1, sheet_name='设备运输费率计算表', usecols=col_name)
        # data_16 = pd.read_excel(Pathinput,
        #                         header=1, sheet_name='电价计算表', usecols=col_name)
        # data_17 = pd.read_excel(Pathinput,
        #                         header=1, sheet_name='水价计算表', usecols=col_name)
        # data_18 = pd.read_excel(Pathinput,
        #                         header=1, sheet_name='电价计算表', usecols=col_name)
        # data_19 = pd.read_excel(Pathinput,
        #                         header=1, sheet_name='风价计算表', usecols=col_name)
        # data_20 = pd.read_excel(Pathinput,
        #                         header=1, sheet_name='主要工程量汇总表', usecols=col_name)
        def get_dict_economy(data, col_name):
            Dict_e = {}
            data_np = np.array(data)
            print(data_np.shape)
            for i in range(0, 1):
                key = data_np[i,0]
                value = data_np[i, 1:].tolist()
                value = [str(i) for i in value]
                Dict_e[key] = value
            print(Dict_e)
            print("OK!!!!!")
            return Dict_e

        def generate_economy_docx(Dict, path_images):
            filename_box = ['11', 'result_chapter12']
            read_path = os.path.join(path_images, '%s.docx') % filename_box[0]
            save_path = os.path.join(path_images, '%s.docx') % filename_box[1]
            tpl = DocxTemplate(read_path)
            print(Dict)
            tpl.render(Dict)
            tpl.save(save_path)

        Dict_e = get_dict_economy(data_2, col_name_2)
        # for i in range(0, len(data_2.index)):
        #     key = data_2['项目名称'][i]
        #     value = [data_2['设备购置费(万元)'][i], data_2['建安工程费(万元)'][i], data_2['其他费用(万元)'][i],
        #              data_2['合计(万元)'][i], data_2['占总投资比例(%)'][i]]
        #     Dict_e[key] = value
        # print(Dict_e)
        # print("OK!!!!!")

        generate_economy_docx(Dict_e, economy_images)


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
                'name': self.project_id.project_name + '可研报告风电章节下载页',
                'datas_fname': self.project_id.project_name + '可研报告风电章节.docx',
                'datas': base64.standard_b64encode(byte),
                'display_name': self.project_id.project_name + '可研报告风电章节',
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
