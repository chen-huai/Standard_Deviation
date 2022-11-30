# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

class Calculate_Operation():

    def location_corresponding(x_str, s_str):
        '''
        s 的第三位有效数字，以及对应 x 的相应的数字
        '''
        digit_location = s_str.find('.')
        if digit_location >= 3:
            # 如果小数点在字符串的第 4 位或大于第四位，也即数字至少在 100 以上
            # 此时第三位有效数字，肯定在小数点前。
            significant_num = s_str[2]
            # 有效位数于小数点的相对位置
            # 0 代表在小数点前， 3-1 是指从小数点前数起的位数
            # sig_loc 的第一位表示有效数字在小数点前，还是后
            # 第二位代表有效数字在小数点的“距离”
            str_len = len(s_str[:digit_location])
            sig_loc = (0, str_len - 3 - 1)

        elif s_str[0] == '0':
            # 若整数部分是0，则有效数字的位置在小数点后
            # 刨除整数和小数点部分
            s_without_int = s_str[digit_location:]
            # 若小数点后有 0，则不将 0 计入有效数字位
            if '.0' in s_without_int:
                digit_location += 1
                while '.00' in s_without_int:
                    # 若小数点后有多个0，也不计入
                    s_without_int = s_without_int.replace('.00', '.0')
                    digit_location += 1
            try:
                # 若位数不够，如 0.0，则有效数字为 0、
                significant_num = s_str[digit_location + 3]
            except:
                significant_num = '0'
            # 1 表示有效数字在小数点后
            sig_loc = (1, 3)

        elif digit_location == -1 and len(s_str) >= 3:
            # 若只有整数，没有小数部分，且整数部分大于 100，即有超过三位数
            # 则直接取第三位
            str_len = len(s_str)
            sig_loc = (0, str_len - 3)
            significant_num = s_str[2]
        elif digit_location == -1 and len(s_str) < 3:
            # 若小于 100，则有效数字为0
            significant_num = '0'
        else:
            # 若整数部分小于 2 位，且整数部分大于 0
            sig_loc = (1, 3 - digit_location)
            significant_num = s_str[sig_loc[1] + digit_location]

        # x 对应的数字
        x_digit_location = x_str.find('.')
        if sig_loc[0] == 0:
            if x_digit_location == -1 and len(x_str) >= 3:
                x_significant_num = x_str[2]
            elif x_digit_location == -1 and len(x_str) < 3:
                x_significant_num = '0'
            else:
                x_significant_num = x_str[x_digit_location - sig_loc[1]]
                print(sig_loc[1])
                print('前')
        else:
            try:
                x_significant_num = x_str[x_digit_location + sig_loc[1]]
            except:
                x_significant_num = '0'

        return x_significant_num, significant_num


    def coverage_critiria(x_list, s_list):
        '''
        收敛准则
        其中 s_list 是一个长度为 3 的 list, 包含当前迭代的 s* 和之前两个迭代的 s*
        其中 x_list 也一样

        难点在于：如何找出 s 的第三位有效数字，对应 x 的数位呢？
                这里的解决办法是：找出 s 三位有效数字，在小数点的位置，从而应用于 x 中
        '''

        s_numbers = []
        x_numbers = []
        for i in range(3):
            # 连续两位不变，故需要进行 3 此迭代。
            s = s_list[i]
            # s 的字符串
            s_str = str(s)

            x = x_list[i]
            # x 的字符串
            x_str = str(x)
            # 找出 s* 的第三位有效数字，和 x* 对应的数字。
            x_sig_num, s_sig_num = Calculate_Operation.location_corresponding(x_str, s_str)
            s_numbers.append(s_sig_num)
            x_numbers.append(x_sig_num)

        # 稳健标准差的第三位有效数字，连续两次不变，且稳健平均值的对应数字亦连续两次不变，则判断为收敛
        # 函数返回 True。否则返回 False
        s_equal_flag = (s_numbers[0] == s_numbers[1]) and (s_numbers[0] == s_numbers[2])
        x_equal_flag = (x_numbers[0] == x_numbers[1]) \
                       and (x_numbers[0] == x_numbers[2])

        if s_equal_flag and x_equal_flag:
            return True
        else:
            return False


    def perform_algorithm_A(x):
        '''
        x 是一个向量
        '''
        if type(x) is list:
            x = np.array(x)

        # 稳健平均和稳健标准差初始值
        x_star = np.median(x)
        x_diff = np.absolute(x - x_star)
        s_star = 1.483 * np.median(x_diff)

        # 上界和下界的初始值
        delta = 1.5 * s_star
        higher_bound = x_star + delta
        lower_bound = x_star - delta

        x_list = []
        s_list = []
        while True:
            x_tmp = np.copy(x)
            x_tmp[x_tmp > higher_bound] = higher_bound
            x_tmp[x_tmp < lower_bound] = lower_bound
            x_star = np.mean(x_tmp)
            s_star = 1.134 * np.std(x_tmp)

            x_list.append(x_star)
            s_list.append(s_star)

            if len(x_list) == 4:
                x_list.pop(0)
                s_list.pop(0)
                # 达到收敛条件
                if Calculate_Operation.coverage_critiria(x_list, s_list):
                    return x_tmp, x_list[2], s_list[2], higher_bound, lower_bound

            # 计算上下界
            delta = 1.5 * s_star
            higher_bound = x_star + delta
            lower_bound = x_star - delta


# if __name__ == '__main__':
#     x = [927, 952, 977, 995, 915, 962, 966, 950, 969, 949, 961, 940, 1002, 956, 960, 943]
#     x, x_star, s_star, higher_bound, lower_bound = perform_algorithm_A(x)
#     print('算法 A 收敛后，数据变为： ', x)
#     print('稳健平均值： ', x_star)
#     print('稳健标准差： ', s_star)

