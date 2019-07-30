# -*- coding: utf-8 -*-

from odoo import models, fields, api
import doc_6
import base64, os
from docxtpl import DocxTemplate
import pandas as pd
import numpy as np
from RoundUp import round_up


def generate_electrical_docx(Dict, path_images, model_name, outputfile):
    filename_box = [model_name, outputfile]
    read_path = os.path.join(path_images, '%s') % filename_box[0]
    save_path = os.path.join(path_images, '%s') % filename_box[1]
    tpl = DocxTemplate(read_path)
    tpl.render(Dict)
    tpl.save(save_path)


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
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    _name = 'auto_word_electrical.firstsec'
    _description = 'electrical input'
    _rec_name = 'project_id'
    project_id = fields.Many2one('auto_word.project', string='项目名', required=True)
    version_id = fields.Char(u'版本', required=True, default="1.0")
    report_attachment_id_input = fields.Many2many('ir.attachment', string=u'电气一次提资')
    attachment_number = fields.Integer(compute='_compute_attachment_number', string='Number of Attachments')

    boxvoltagetype = fields.Many2one('auto_word_electrical.boxvoltagetype', string='TypeID', required=True)
    TypeID_boxvoltagetype=0

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

            # if '电气一次' in t:
            #     xlsdata_first = base64.standard_b64decode(re.datas)
            #     name_first = t
            #     file_first = True
            #
            # elif '电气二次' in t:
            #     xlsdata_second = base64.standard_b64decode(re.datas)
            #     name_second = t
            #     file_second = True
        if file_exist == True:
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
                f.write(xlsdata)
                # if '电气一次' in re.name:
                #     f.write(xlsdata_first)
                # elif '电气二次' in re.name:
                #     f.write(xlsdata_second)
                f.close()
            else:
                print(Pathinput + " already existed.")
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

            sheet_name_array = ['01站用电负荷表', '02电气一次主要设备及材料表', '03电气二次设备主要材料清单', '04通信部分材料清单']
            for i in range(0, len(sheet_name_array)):
                if i == 0:
                    data = pd.read_excel(Pathinput, header=0, sheet_name=sheet_name_array[i],
                                         skip_footer=2)
                    col_name = data.columns.tolist()
                else:
                    data = pd.read_excel(Pathinput, header=0, sheet_name=sheet_name_array[i], )
                    # usecols=col_name_array[i])
                    col_name = data.columns.tolist()
                    if i==1:
                        if ~data['数量'].isnull().values.all() == True:
                            take_data=data[data['数量'].isnull().values == True]
                            drop_number=take_data[take_data.ix[:, 0].str.contains("-") == True].index
                        data=data.drop(drop_number)
                        modifier_data=data.ix[:, 0][data.ix[:, 0].str.contains("-") == True]
                        modifier_number_list=modifier_data.index
                        for j in range(0,modifier_data.shape[0]):
                            number = modifier_data.iloc[j].split("-")
                            if j ==0:
                                Judging=number[0]
                                number_add=1
                                string_number=Judging+"-"+str(number_add)
                                data.ix[modifier_number_list[j], 0]=string_number
                            else:
                                if number[0]==Judging:
                                   number_add=number_add+1
                                   string_number = Judging + "-" + str(number_add)
                                   data.ix[modifier_number_list[j], 0] = string_number
                                elif number[0]!=Judging:
                                   number_add =1
                                   string_number = number[0] + "-" + str(number_add)
                                   Judging=number[0]
                                   data.ix[modifier_number_list[j], 0] = string_number
                        #         print("88888888888")
                        #         print(i)
                        #         print(data.ix[modifier_number_list[i], 0])
                        #         print(string_number)
                        #
                        # print("jjjjjjjjjjjjjjjjjjjjjjjjjj")
                        print(data)
                        #
                print(i)
                data = data.replace(np.nan, '-', regex=True)
                col_name_array.append(col_name)
                tabel_number = str(chapter_number) + '_' + str(i)
                dict_content = get_dict_electrical_firstsec(tabel_number, col_name_array[i], data, sheet_name_array[i])

                dictMerged.update(dict_content)

            print(str(dictMerged['result_list6_1'][48]['cols'][1]))

            dict_6_res_word = {
                '站用电负荷表说明_1': str('1、综合楼空调机为单冷型，该负荷仅在夏季使用；'),
                '站用电负荷表说明_2': str('2、设备楼空调机为冷暖型。'),
                '热镀锌扁钢': str(dictMerged['result_list6_1'][47]['cols'][1]),
                '热镀锌角钢': str(dictMerged['result_list6_1'][48]['cols'][1]),


            }
            print(dictMerged)
            Dict6 = dict(dictMerged, **dict_6_res_word)
            generate_electrical_docx(Dict6, electrical_path, model_name, outputfile)
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
            [('res_model', '=', 'auto_word_electrical.firstsec'), ('res_id', 'in', self.ids)], ['res_id'],
            ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for expense in self:
            expense.attachment_number = attachment.get(expense.id, 0)


    def submit_electrical_firstsec(self):
        self.TypeID_boxvoltagetype=self.boxvoltagetype.TypeID
        dict6 = doc_6.generate_electrical_TypeID_dict(self.TypeID_boxvoltagetype,self.project_id.turbine_numbers_suggestion)

        print(dict6)
class electrical_BoxVoltageType(models.Model):
    _name = 'auto_word_electrical.boxvoltagetype'
    _description = 'electrical_boxvoltagetype'
    _rec_name = 'TypeName'
    TypeID = fields.Integer(u'型号ID')
    TypeName = fields.Char(u'型号')
    CapacityBoxVoltage = fields.Integer(u'容量')
    VoltageClasses = fields.Char(u'电压等级')
    WiringGroup = fields.Char(u'接线组别')
    CoolingType = fields.Char(u'冷却方式')
    ShortCircuitImpedance = fields.Char(u'短路阻抗')