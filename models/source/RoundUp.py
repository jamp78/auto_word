def round_dict(dic):
    for key in dic:
        if type(dic[key]).__name__ != 'int':
            dic[key] = round_up(dic[key], 2)

    return dic


def round_up(value, dec_digits=2):
    result = str(value).strip()
    if result != '':
        zero_count = dec_digits
        index_dec = result.find('.')
        if index_dec > 0:
            zero_count = len(result[index_dec + 1:])
            if zero_count > dec_digits:
                if int(result[index_dec + dec_digits + 1]) > 4:
                    result = str(value + pow(10, dec_digits * -1))
                    # 存在进位的可能，小数点会移位
                    index_dec = result.find('.')
                result = result[:index_dec + dec_digits + 1]
                zero_count = 0
            else:
                zero_count = dec_digits - zero_count
        else:
            result += '.'
        for i in range(zero_count):
            result += '0'
    return float(result)

def round_up3(value, dec_digits=3):
    result = str(value).strip()
    if result != '':
        zero_count = dec_digits
        index_dec = result.find('.')
        if index_dec > 0:
            zero_count = len(result[index_dec + 1:])
            if zero_count > dec_digits:
                if int(result[index_dec + dec_digits + 1]) > 4:
                    result = str(value + pow(10, dec_digits * -1))
                    # 存在进位的可能，小数点会移位
                    index_dec = result.find('.')
                result = result[:index_dec + dec_digits + 1]
                zero_count = 0
            else:
                zero_count = dec_digits - zero_count
        else:
            result += '.'
        for i in range(zero_count):
            result += '0'
    return float(result)


def round_dict_numbers(dic, tur_num,keep_num):
    for key_o in list(dic.keys()):
        # if type(dic[key_o]).__name__ != 'int':
        if 'numbers' not in key_o:
            if type(dic[key_o]).__name__ != 'int':
                dic[key_o] = round_up(dic[key_o], 2)
                key = key_o + '_numbers'
                dic[key] = round_up(dic[key_o] * tur_num, keep_num)
            else:
                key = key_o + '_numbers'
                dic[key] = dic[key_o] * tur_num
    return dic



# print(round_up(2.55, dec_digits=1))
#
# result = str(2.55).strip()
# index_dec = result.find('.')
# a = result[index_dec + 1:]
# print(result, index_dec, a)
# 最大数
def Get_Max(list):
    return max(list)


# 最小数
def Get_Min(list):
    return min(list)


# 极差
def Get_Range(list):
    return max(list) - min(list)


# 中位数
def get_median(data):
    data = sorted(data)
    size = len(data)
    if size % 2 == 0:
        # 判断列表长度为偶数
        median = (data[size // 2] + data[size // 2 - 1]) / 2
    if size % 2 == 1:
        # 判断列表长度为奇数
        median = data[(size - 1) // 2]
    return median



# 获取平均数
def Get_Average(list):
    sum = 0
    for item in list:
        sum += item
    return sum / len(list)

# 获取综合数
def Get_Sum(list):
    sum = 0
    for item in list:
        sum += item
    return sum