# -*- coding: utf-8 -*-

from odoo import models, fields, api
import doc_6
import base64, os
from docxtpl import DocxTemplate
import pandas as pd
import numpy as np
from RoundUp import round_up


def get_dict_electrical_firstsec(index, col_name, data, sheet_name_array):
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
    _name = 'auto_word_electrical.firstsec'
    _description = 'electrical input'
    _rec_name = 'project_id'
    project_id = fields.Many2one('auto_word.project', string='项目名', required=True)
    version_id = fields.Char(u'版本', required=True, default="1.0")
    report_attachment_id_input = fields.Many2many('ir.attachment', string=u'电气一次提资')
    attachment_number = fields.Integer(compute='_compute_attachment_number', string='Number of Attachments')

    def electrical_firstsec_generate(self):
        dictMerged, Dict, dict_content, dict_head = {}, {}, {}, {}
        col_name_array = []
        file_first = False
        file_second = False
        for re in self.report_attachment_id_input:
            t = re.name
            chapter_number = 6
            if '电气一次' in t:
                xlsdata_first = base64.standard_b64decode(re.datas)
                name_first = t
                file_first = True

            elif '电气二次' in t:
                xlsdata_second = base64.standard_b64decode(re.datas)
                name_second = t
                file_second = True
        if file_first == True:
            electrical_path = self.env['auto_word.project'].path_images_chapter_6
            suffix_in = ".xls"
            suffix_out = ".docx"
            inputfile = name_first + suffix_in
            outputfile = 'result_chapter' + str(chapter_number) + suffix_out
            model_name = 'cr' + str(chapter_number) + suffix_out
            Pathinput = os.path.join(electrical_path, '%s') % inputfile
            Pathoutput = os.path.join(electrical_path, '%s') % outputfile
            if not os.path.exists(Pathinput):
                f = open(Pathinput, 'wb+')
                if '电气一次' in re.name:
                    f.write(xlsdata_first)
                elif '电气二次' in re.name:
                    f.write(xlsdata_second)
                f.close()
            else:
                print(Pathinput + " already existed.")
                os.remove(Pathinput)
                f = open(Pathinput, 'wb+')
                if '电气一次' in re.name:
                    f.write(xlsdata_first)
                elif '电气二次' in re.name:
                    f.write(xlsdata_second)
                f.close()

            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)

            sheet_name_array = ['01站用电负荷表', '02电气一次主要设备及材料表']
            for i in range(0, len(sheet_name_array)):
                if i == 0:
                    data = pd.read_excel(Pathinput, header=0, sheet_name=sheet_name_array[i],
                                         skip_footer=2)
                    col_name = data.columns.tolist()
                else:
                    data = pd.read_excel(Pathinput, header=0, sheet_name=sheet_name_array[i], )
                    # usecols=col_name_array[i])
                    col_name = data.columns.tolist()

                data = data.replace(np.nan, '-', regex=True)
                col_name_array.append(col_name)
                tabel_number = str(chapter_number) + '_' + str(i)
                dict_content = get_dict_electrical_firstsec(tabel_number, col_name, data, sheet_name_array[i])

                dictMerged.update(dict_content)

            print(dictMerged)
        return

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
            [('res_model', '=', 'auto_word_electrical.firstsec'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for expense in self:
            expense.attachment_number = attachment.get(expense.id, 0)
