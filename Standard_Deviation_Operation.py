# # -*- coding: utf-8 -*-

import sys
import bin.chicon  # 引用图标
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Standard_Deviation_Ui import *
from Calculate_Operation import *

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.actionExit.triggered.connect(MyMainWindow.close)
        self.actionHelp.triggered.connect(self.show_version)
        self.actionAuthor.triggered.connect(self.show_author_message)
        self.pushButton_2.clicked.connect(self.calculate)
        self.pushButton.clicked.connect(self.lineEdit.clear)
        self.pushButton.clicked.connect(self.textBrowser.clear)
        # self.checkBox_9.toggled.connect(lambda: self.pdfNameRule('Invoice No'))

    # 暂时用不上
    def getConfig(self):
        # 初始化，获取或生成配置文件
        global configFileUrl
        global desktopUrl
        global now
        global last_time
        global today
        global oneWeekday
        global fileUrl

        date = datetime.datetime.now() + datetime.timedelta(days=1)
        now = int(time.strftime('%Y'))
        last_time = now - 1
        today = time.strftime('%Y.%m.%d')
        oneWeekday = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y.%m.%d')
        desktopUrl = os.path.join(os.path.expanduser("~"), 'Desktop')
        configFileUrl = '%s/config' % desktopUrl
        configFile = os.path.exists('%s/config_sap.csv' % configFileUrl)
        # print(desktopUrl,configFileUrl,configFile)
        if not configFile:  # 判断是否存在文件夹如果不存在则创建为文件夹
            reply = QMessageBox.question(self, '信息', '确认是否要创建配置文件', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                if not os.path.exists(configFileUrl):
                    os.makedirs(configFileUrl)
                MyMainWindow.createConfigContent(self)
                MyMainWindow.getConfigContent(self)
                self.textBrowser.append("创建并导入配置成功")
            else:
                exit()
        else:
            MyMainWindow.getConfigContent(self)

    def getConfigContent(self):
        # 配置文件
        csvFile = pd.read_csv('%s/config_sap.csv' % configFileUrl, names=['A', 'B', 'C'])
        global configContent
        global username
        global role
        configContent = {}
        username = list(csvFile['A'])
        number = list(csvFile['B'])
        role = list(csvFile['C'])
        for i in range(len(username)):
            configContent['%s' % username[i]] = number[i]
        # a = len(configContent)
        # if (int(configContent['config_num']) != len(configContent)) or (len(configContent) != 40):
        # 	reply = QMessageBox.question(self, '信息', 'config文件配置缺少一些参数，是否重新创建并获取新的config文件', QMessageBox.Yes | QMessageBox.No,
        # 								 QMessageBox.Yes)
        # 	if reply == QMessageBox.Yes:
        # 		MyMainWindow.createConfigContent(self)
        # 		MyMainWindow.getConfigContent(self)
        try:
            self.textBrowser_2.append("配置获取成功")
        except AttributeError:
            QMessageBox.information(self, "提示信息", "已获取配置文件内容", QMessageBox.Yes)
        else:
            pass

    def createConfigContent(self):
        global monthAbbrev
        months = "JanFebMarAprMayJunJulAugSepOctNovDec"
        n = time.strftime('%m')
        pos = (int(n) - 1) * 3
        monthAbbrev = months[pos:pos + 3]

        configContent = [
            # ['SAP登入信息', '内容', '备注'],
            # ['订单类型', 'DR', '根据Site自定义'],
            # ['销售组织', '0486', '根据Site自定义'],
            # ['分销渠道', '01', '根据Site自定义'],
            # ['销售办事处', '>601', '根据Site自定义'],
            # ['销售组', '240', '根据Site自定义'],、
            ['特殊开票', '内容', '备注'],
            ['SAP_Date_URL', 'N:\\XM Softlines\\6. Personel\\5. Personal\\Supporting Team\\收样\\3.Sap\\ODM Data - XM',
             '文件数据路径'],
            ['Invoice_File_URL',
             'N:\\XM Softlines\\6. Personel\\5. Personal\\Supporting Team\\收样\\3.Sap\\ODM Data - XM\\2.特殊开票',
             '特殊开票文件路径'],
            ['Invoice_File_Name', '开票特殊要求2022.xlsx', '特殊开票文件名称'],
            ['SAP登入信息', '内容', '备注'],
            ['Login_msg', 'DR-0486-01->601-240', '订单类型-销售组织-分销渠道-销售办事处-销售组'],
            ['Hourly Rate', '金额', '备注'],
            ["Hourly Rate(PC)", 315, '每年更新'],
            ['Hourly Rate(Lab)', 342, '每年更新'],
            ['成本中心', '编号', '备注'],
            ['CS_Selected', 1, '是否默认被选中,1选中，0未选中'],
            ['PHY_Selected', 1, '是否默认被选中,1选中，0未选中'],
            ['CHM_Selected', 1, '是否默认被选中,1选中，0未选中'],
            ['CS_Cost_Center', '48601240', 'CS成本中心'],
            ['CHM_Cost_Center', '48601293', 'CHM成本中心'],
            ['PHY_Cost_Center', '48601294', 'PHY成本中心'],
            ['计划成本', '数值', '备注'],
            ['Plan_Costc_Parameter', 0.9, '实际的90%'],
            ['Significant_Digits', 0, '保留几位有效数值'],
            ['SAP操作', '内容', '备注'],
            ['NVA01_Selected', 1, '是否默认被选中,1选中，0未选中'],
            ['NVA02_Selected', 1, '是否默认被选中,1选中，0未选中'],
            ['NVF01_Selected', 0, '是否默认被选中,1选中，0未选中'],
            ['NVF03_Selected', 0, '是否默认被选中,1选中，0未选中'],
            ['DataB_Selected', 1, '是否默认被选中,1选中，0未选中'],
            ['Plan_Cost_Selected', 25, '每月超过几号自动选中（不包含）'],
            ['Save_Selected', 1, '是否默认被选中,1选中，0未选中'],
            ['管理操作', '内容', '备注'],
            ['Invoice_No_Selected', 1, '是否默认被选中,1选中，0未选中'],
            ['Invoice_Start_Num', 4, 'Invoice的起始数字'],
            ['Invoice_Num', 9, 'Invoice的总位数'],
            ['Company_Name_Selected', 1, '是否默认被选中,1选中，0未选中'],
            ['Order_No_Selected', 0, '是否默认被选中,1选中，0未选中'],
            ['Order_Start_Num', 7, 'Order的起始数字'],
            ['Order_Num', 9, 'Order的总位数'],
            ['Project_No_Selected', 0, '是否默认被选中,1选中，0未选中'],
            ['PDF_Name', 'Invoice No + Company Name', 'PDF文件名称默认规则'],
            ['PDF_Files_Import_URL', desktopUrl, 'PDF文件导入路径'],
            ['PDF_Files_Export_URL', 'N:\\XM Softlines\\1. Project\\3. Finance\\02. WIP', 'PDF文件导出路径'],
            ['名称', '编号', '角色'],
            ['chen, frank', '6375108', 'CS'],
            ['chen, frank', '6375108', 'Sales'],
        ]
        config = np.array(configContent)
        df = pd.DataFrame(config)
        df.to_csv('%s/config_sap.csv' % configFileUrl, index=0, header=0, encoding='utf_8_sig')
        self.textBrowser_2.append("配置文件创建成功")
        QMessageBox.information(self, "提示信息",
                                "默认配置文件已经创建好，\n如需修改请在用户桌面查找config文件夹中config_sap.csv，\n将相应的文件内容替换成用户需求即可，修改后记得重新导入配置文件。",
                                QMessageBox.Yes)

    def show_author_message(self):
        # 关于作者
        QMessageBox.about(self, "关于",
                          "人生苦短，码上行乐。\n\n\n        ----Frank Chen")

    def show_version(self):
        # 关于作者
        QMessageBox.about(self, "版本",
                          "V 22.01.01\n\n\n 2022-11-30")

    def get_gui_data(self):
        gui_data = {}
        gui_data['Input data'] = self.lineEdit.text().strip()
        return gui_data
    
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
            x_sig_num, s_sig_num = MyMainWindow.location_corresponding(x_str, s_str)
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
                if MyMainWindow.coverage_critiria(x_list, s_list):
                    return x_tmp, x_list[2], s_list[2], higher_bound, lower_bound

            # 计算上下界
            delta = 1.5 * s_star
            higher_bound = x_star + delta
            lower_bound = x_star - delta

    def calculate(self):
        try:
            gui_data = MyMainWindow.get_gui_data(self)
            # 转换列表中的元素为float
            x = list(map(float, gui_data['Input data'].split(" ")))
            x, x_star, s_star, higher_bound, lower_bound = Calculate_Operation.perform_algorithm_A(x)
            self.textBrowser.append('输入数据：%s' % gui_data['Input data'])
            self.textBrowser.append('算法 A 收敛后，数据变为：%s' % x)
            self.textBrowser.append('稳健平均值：%s' % x_star)
            self.textBrowser.append('稳健标准差：%s' % s_star)
            self.textBrowser.append('------------------------------')
        except Exception as msg:
            self.textBrowser.append('报错信息：%s' % msg)
            self.textBrowser.append('------------------------------')






if __name__ == "__main__":
    import sys
    import os
    import time
    import pandas as pd
    import numpy as np
    import datetime

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())