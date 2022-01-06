import sys
from math import pi, sqrt
from GUI import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

class App(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_1_1.clicked.connect(self.start)
        self.ui.pushButton_2_1.clicked.connect(self.start)
        self.ui.pushButton_3_1.clicked.connect(self.start)
        self.ui.pushButton_4_1.clicked.connect(self.start)
        self.ui.pushButton_5_1.clicked.connect(self.start)
        self.ui.pushButton_6_1.clicked.connect(self.start)
        self.ui.pushButton_7_1.clicked.connect(self.start)
        self.ui.pushButton_8_1.clicked.connect(self.start)
        self.ui.pushButton_9_1.clicked.connect(self.start)
        self.ui.pushButton_9_2.clicked.connect(self.clear)

        self.ui.textEdit_9_1.setReadOnly(True)
        
        self.ui.comboBox_1_2.currentTextChanged.connect(self.__handler_locker_1)
        self.ui.comboBox_2_3.currentTextChanged.connect(self.__handler_locker_2)
        self.ui.comboBox_3_2.currentTextChanged.connect(self.__handler_locker_3)
        self.ui.comboBox_4_1.currentTextChanged.connect(self.__handler_locker_4)

        self.base_line_edit = [self.ui.lineEdit_1_2, self.ui.lineEdit_1_3, 
            self.ui.lineEdit_1_4, self.ui.lineEdit_1_5, self.ui.lineEdit_1_6,
            self.ui.lineEdit_2_1, self.ui.lineEdit_2_2, self.ui.lineEdit_2_3, 
            self.ui.lineEdit_2_4, self.ui.lineEdit_3_1, self.ui.lineEdit_3_2, 
            self.ui.lineEdit_4_1, self.ui.lineEdit_4_2, self.ui.lineEdit_4_3, 
            self.ui.lineEdit_4_4, self.ui.lineEdit_4_5, self.ui.lineEdit_4_6,
            self.ui.lineEdit_6_1, self.ui.lineEdit_7_1, self.ui.lineEdit_8_1, self.ui.lineEdit_9_1]

        """ Костыль, но необходимый """
        # =============================================================================================================================================
        self.base_block = [self.ui.label_6, self.ui.label_7, self.ui.label_10, self.ui.lineEdit_1_4, self.ui.lineEdit_1_5, self.ui.lineEdit_1_6, 
            self.ui.label_21, self.ui.label_22, self.ui.lineEdit_3_1, self.ui.lineEdit_3_2, self.ui.label_29, self.ui.lineEdit_4_3, self.ui.label_25, 
            self.ui.lineEdit_4_5, self.ui.label_27, self.ui.lineEdit_4_6] 

        for i in self.base_block:
            i.setEnabled(False)
        # =============================================================================================================================================

        self.strength_report = Strength_report()
        self.constructive_calculation = Constructive_calculation()
        self.stability_calculation = Stability_calculation()
        self.torsion_calculation = Torsion_calculation()
        self.determination_of_durability = Determination_of_durability()
        self.choice_of_the_workpice = Choice_of_the_workpice()
        self.calculation_allowances = Calculation_allowances()
        self.processing_details = Processing_details()
        self.route_map = Route_map()

        self.strength_report.mysignal.connect(self.__handler_signal)
        self.constructive_calculation.mysignal.connect(self.__handler_signal)
        self.stability_calculation.mysignal.connect(self.__handler_signal)
        self.torsion_calculation.mysignal.connect(self.__handler_signal)
        self.determination_of_durability.mysignal.connect(self.__handler_signal)
        self.choice_of_the_workpice.mysignal.connect(self.__handler_signal)
        self.calculation_allowances.mysignal.connect(self.__handler_signal)
        self.processing_details.mysignal.connect(self.__handler_signal)
        self.route_map.mysignal.connect(self.__handler_signal)

    def clear(self) -> None:
        self.ui.textEdit_9_1.clear()

    def start(self, button) -> None:
        calculation_type = self.ui.tabWidget.tabText(self.ui.tabWidget.currentIndex())
        answer = 0
        if calculation_type == 'Прочностный отчет':
            F = self.ui.lineEdit_1_1.text()
            material = self.ui.comboBox1_1.currentText()
            cross_section = self.ui.comboBox_1_2.currentText()

            D_o, d_o = self.ui.lineEdit_1_2.text(), self.ui.lineEdit_1_3.text()
            a, b = self.ui.lineEdit_1_4.text(), self.ui.lineEdit_1_5.text()
            d = self.ui.lineEdit_1_6.text()

            self.strength_report.init_args(F=F, material=material, cross_section=cross_section, D_o=D_o, d_o=d_o, a=a, b=b, d=d)
            answer = self.strength_report.calculation()

        elif calculation_type == 'Конструкторский расчёт':
            z2, z1 = self.ui.lineEdit_2_2.text(), self.ui.lineEdit_2_3.text()
            M = self.ui.lineEdit_2_4.text()
            hrc = self.ui.lineEdit_2_1.text()

            type_of_wheels = self.ui.comboBox_2_1.currentText()
            wheel_arrangement = self.ui.comboBox_2_2.currentText()
            heat_treatment_method = self.ui.comboBox_2_3.currentText()

            self.constructive_calculation.init_args(z2=z2, z1=z1, M=M, hrc=hrc, wheel_arrangement=wheel_arrangement, heat_treatment_method=heat_treatment_method, type_of_wheels=type_of_wheels)
            answer = self.constructive_calculation.calculation()

        elif calculation_type == 'Расчёты на устойчивость':
            material = self.ui.comboBox_3_1.currentText()
            cross_section = self.ui.comboBox_3_2.currentText()
            h = self.ui.lineEdit_3_1.text()
            d = self.ui.lineEdit_3_2.text()

            self.stability_calculation.init_args(material=material, cross_section=cross_section, h=h, d=d)
            answer = self.stability_calculation.calculation()

        elif calculation_type == 'Расчёты на кручение':
            material = self.ui.comboBox_4_2.currentText()
            cross_section = self.ui.comboBox_4_1.currentText()
            d_s, k_m = self.ui.lineEdit_4_1.text(), self.ui.lineEdit_4_2.text()
            D_o, d_o = self.ui.lineEdit_4_3.text(), self.ui.lineEdit_4_4.text()
            width, depth = self.ui.lineEdit_4_5.text(), self.ui.lineEdit_4_6.text()
            self.torsion_calculation.init_args(material=material, cross_section=cross_section, d_s=d_s, k_m=k_m, D_o=D_o, d_o=d_o, width=width, depth=depth)
            answer = self.torsion_calculation.calculation()

        elif calculation_type == 'Определение долговечности':
            type_bearing = self.ui.comboBox_5_1.currentText()
            n, Frad = self.ui.lineEdit_5_1.text(), self.ui.lineEdit_5_2.text()
            kb_value, kt_value = self.ui.comboBox_5_2.currentText(), self.ui.comboBox_5_3.currentText()

            self.determination_of_durability.init_args(type_bearing=type_bearing, n=n, Frad=Frad, kb_value=kb_value, kt_value=kt_value)
            answer = self.determination_of_durability.calculation()

        elif calculation_type == 'Выбор заготовки':
            material = self.ui.comboBox_6_1.currentText()
            massa = self.ui.lineEdit_6_1.text()

            self.choice_of_the_workpice.init_args(material=material, massa=massa)
            answer = self.choice_of_the_workpice.calculation()

        elif calculation_type == 'Расчет припусков':
            the_surface = self.ui.comboBox_7_1.currentText()
            Ra = self.ui.lineEdit_7_1.text()

            self.calculation_allowances.init_args(the_surface=the_surface, Ra=Ra)

            answer = self.calculation_allowances.calculation()

        elif calculation_type == 'Обработка детали':
            the_surface = self.ui.comboBox_8_1.currentText()
            Ra = self.ui.lineEdit_8_1.text()

            self.processing_details.init_args(the_surface=the_surface, Ra=Ra)

            answer = self.processing_details.calculation()

        elif calculation_type == 'Маршрутная карта':   
            operation = self.ui.comboBox_9_1.currentText()
            time = self.ui.lineEdit_9_1.text()

            self.route_map.init_args(operation=operation, time=time)

            answer_tuple = self.route_map.calculation()

            self.ui.textEdit_9_1.append(f'{answer_tuple[0]} | Вреия выполнения: {answer_tuple[1]} минут')

        if answer != 0:
            QtWidgets.QMessageBox.information(self, calculation_type, answer)

    def __handler_locker_1(self, value: str) -> None:
        self.__clear(self.base_line_edit)
        if value == 'Трубовое сечение':
            self.__locker([self.ui.label_8, self.ui.label_9, 
                self.ui.lineEdit_1_2, self.ui.lineEdit_1_3], True) 
            self.__locker([self.ui.label_6, self.ui.label_7, self.ui.label_10, 
                self.ui.lineEdit_1_4, self.ui.lineEdit_1_5, self.ui.lineEdit_1_6], False)
        elif value == 'Прямоугольное сечение':
            self.__locker([self.ui.label_6, self.ui.label_7, 
                self.ui.lineEdit_1_4, self.ui.lineEdit_1_5], True) 
            self.__locker([self.ui.label_8, self.ui.label_9, self.ui.label_10, 
                self.ui.lineEdit_1_2, self.ui.lineEdit_1_3, self.ui.lineEdit_1_6], False) 
        elif value == 'Круговое сечение':
            self.__locker([self.ui.label_10, self.ui.lineEdit_1_6], True)
            self.__locker([self.ui.label_6, self.ui.label_7, self.ui.label_8, self.ui.label_9, 
                self.ui.lineEdit_1_2, self.ui.lineEdit_1_3, self.ui.lineEdit_1_4, self.ui.lineEdit_1_5], False)

    def __handler_locker_2(self, value: str) -> None:
        self.__clear(self.ui.lineEdit_2_1)
        if value == 'Закалка ТВЧ':
            self.__locker([self.ui.label_17, self.ui.lineEdit_2_1], True)
        elif value == 'Цементация':
            self.__locker([self.ui.label_17, self.ui.lineEdit_2_1], True)
        elif value == 'Улучшения':
            self.__locker([self.ui.label_17, self.ui.lineEdit_2_1], False)

    def __handler_locker_3(self, value: str) -> None:
        self.__clear(self.base_line_edit)
        if value == 'Прямоугольник':
            self.__locker([self.ui.label_21, self.ui.label_22, self.ui.lineEdit_3_1, self.ui.lineEdit_3_2], False)
        elif value == 'Круг':
            self.__locker([self.ui.label_22, self.ui.lineEdit_3_2], True)
            self.__locker([self.ui.label_21, self.ui.lineEdit_3_1], False)
        elif value == 'Швеллер № 10':
            self.__locker([self.ui.label_21, self.ui.label_22, self.ui.lineEdit_3_1, self.ui.lineEdit_3_2], True)

    def __handler_locker_4(self, value: str) -> None:
        self.__clear(self.base_line_edit)
        if value == 'Круговое':
            self.__locker([self.ui.label_28, self.ui.lineEdit_4_4], True)
            self.__locker([self.ui.label_29, self.ui.lineEdit_4_3, self.ui.label_25, self.ui.lineEdit_4_5, self.ui.label_27, self.ui.lineEdit_4_6], False)
        elif value == 'Трубчатое':
            self.__locker([self.ui.label_29, self.ui.lineEdit_4_3, self.ui.label_28, self.ui.lineEdit_4_4], True)
            self.__locker([self.ui.label_27, self.ui.lineEdit_4_5, self.ui.label_25, self.ui.lineEdit_4_6], False)
        elif value == 'Шпоночное':
            self.__locker([self.ui.label_27, self.ui.lineEdit_4_5, self.ui.label_25, self.ui.lineEdit_4_6], True)
            self.__locker([self.ui.label_29, self.ui.lineEdit_4_3, self.ui.label_28, self.ui.lineEdit_4_4], False)

    def __clear(self, base: list) -> None:
        if isinstance(base, list):
            if base:
                for i in base:
                    i.clear()
        else:
            base.clear()

    def __locker(self, base: list, states: bool) -> None:
        if isinstance(base, list):
            if base:
                for i in base:
                    i.setEnabled(states)
        else:
            base.setEnabled(states)

    def __handler_signal(self, value):
        if value[0] == 'Error':
            QtWidgets.QMessageBox.warning(self, value[0], value[1])


class Base_class(QtCore.QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table_of_materials = {
            'Сталь': {
                'strength': 160,
                'mat': 120,
                'G': 1.5 * 10 ** 6,
                'E': 2.1 * 10 ** 6
            },
            'Алюминий':{
                'strength': 60,
                'mat': 40,
                'G': 1.1 * 10 ** 6,
                'E': 1.5 * 10 ** 6
            },
            'Латунь': {
                'strength': 160,
                'mat': 60,
                'G': 1.2 * 10 ** 6,
                'E': 1.7 * 10 ** 6
            },
            'Чугун': {
                'strength': 240,
                'mat': '',
                'G': '',
                'E': ''
            },
        }

    @staticmethod
    def _checking_values(value: str):
        return float(value.replace(',', '.')) if value != '' else None


class Strength_report(Base_class):
    mysignal = QtCore.pyqtSignal(list)

    def init_args(self, F, material, cross_section, D_o, d_o, a, b, d) -> None:
        self.F = self._checking_values(F)
        self.cross_section = cross_section
        self.D_o = self._checking_values(D_o)
        self.d_o = self._checking_values(d_o)
        self.a = self._checking_values(a)
        self.b = self._checking_values(b)
        self.d = self._checking_values(d)
        self.material_strength = self.table_of_materials[material]['strength']

    def calculation(self) -> str:
        try:
            if self.cross_section == 'Трубовое сечение':
                self.A = pi / 4 * (self.D_o ** 2 - self.d_o ** 2) 
            elif self.cross_section == 'Прямоугольное сечение':
                self.A = self.a * self.b
            else:
                self.A = (pi * self.d ** 2) / 4
            sigma = 160
            k = self.F / self.A
            K = sigma / k
            if self.F / self.A <= self.material_strength:
                answer = f'Материал выдержит.\nНапряжение {round(k, 4)}\nЗапас прочности {round(K, 4)}'  
            else:
                answer = 'Материал не выдержит.'
            return answer
        except Exception as _ex:
            self.mysignal.emit(['Error', str(_ex)])
            return 0


class Constructive_calculation(Base_class):
    mysignal = QtCore.pyqtSignal(list)

    def init_args(self, z2, z1, M, hrc, wheel_arrangement, heat_treatment_method, type_of_wheels) -> None:
        self.z2 = self._checking_values(z2)
        self.z1 = self._checking_values(z1)
        self.M = self._checking_values(M)
        self.hrc = self._checking_values(hrc)
        self.wheel_arrangement = wheel_arrangement
        self.heat_treatment_method = heat_treatment_method
        self.type_of_wheels = type_of_wheels
        self.khb, self.ka  = 0, 0

    def calculation(self) -> str:
        try:
            U = self.z2 / self.z1

            if self.type_of_wheels == 'Прямозубчатая':
                self.ka = 49.5
            elif self.type_of_wheels == 'Кривазубчатая':
                self.ka = 43

            if self.wheel_arrangement == 'Симетрично':
                self.khb = 1.05
            elif self.wheel_arrangement == 'Несеметрично':
                self.khb = 1.2
            elif self.wheel_arrangement == 'Консоль':
                self.khb = 1.3

            if self.heat_treatment_method == 'Закалка ТВЧ':
                Vn = 18 * self.hrc + 70
            elif self.heat_treatment_method == 'Улучшения':
                Vn = 2 * 300 + 150
            elif self.heat_treatment_method == 'Цементация':
                Vn = 23 * self.hrc

            aw1 = sqrt((self.M * self.khb) / (U ** 2 * Vn * 0.2))
            aw2 = str(round(self.ka * (U + 1) * aw1, 4))
            return aw2
        except Exception as _ex:
            self.mysignal.emit(['Error', str(_ex)])
            return 0


class Stability_calculation(Base_class):
    mysignal = QtCore.pyqtSignal(list)

    def init_args(self, material, cross_section, h, d) -> None:
        self.cross_section = cross_section
        self.J = 0 
        self.Fkp, self.R2 = 0, 0
        self.U, self.L = 0.7, 3000
        self.G = 20 * 10 ** 4
        self.h = self._checking_values(h)
        self.d = self._checking_values(d)
        self.E = self.table_of_materials[material]['E']

        
    def calculation(self) -> str:
        try: 
            if self.cross_section == 'Прямоугольник':
                self.J = 1480
            elif self.cross_section == 'Круг':
                self.J = 0.1 * self.d ** 4
            else:
                self.J = (self.h * self.d ** 3) / 12

            self.Fkp = (pi * self.E * self.J) / (self.U * self.L) ** 2
            self.R2 = -(self.G * 0.5) / (2 * 0.86)
            if self.R2 <= self.Fkp:
                answer = f'Мост будет устойчив, т.к\nR2 <= Fkp\n{round(self.R2, 4)} <= {round(self.Fkp, 4)}'
            else:
                answer = f'Мост будет не устойчив, т.к\nR2 > Fkp\n{round(self.R2, 4)} > {round(self.Fkp, 4)}'
            return answer
        except Exception as _ex:
            self.mysignal.emit(['Error', str(_ex)])
            return 0


class Torsion_calculation(Base_class):
    mysignal = QtCore.pyqtSignal(list)
    def init_args(self, material, cross_section, d_s, k_m, D_o, d_o, width, depth) -> None:
        self.cross_section = cross_section
        self.d_s = self._checking_values(d_s)
        self.k_m = self._checking_values(k_m)
        self.D_o = self._checking_values(D_o)
        self.d_o = self._checking_values(d_o)
        self.width = self._checking_values(width)
        self.depth = self._checking_values(depth)
        self.Jp, self.Wp = 0, 0

        dict_info = self.table_of_materials[material]
        self.mat, self.G = dict_info['mat'], dict_info['G']

    
    def calculation(self) -> str:
        try:
            if self.cross_section == 'Круговое':
                self.Jp = 0.1 * self.d_o ** 4
                self.Wp = 0.2 * self.d_o ** 3
            elif self.cross_section == 'Трубчатое':
                self.Jp = 0.1 * self.D_o ** 4 - 0.1 * self.d_o ** 4
                self.Wp = 0.2 * self.D_o ** 3 - 0.2 * self.d_o ** 3
            else:
                self.Jp = 0.1 * self.d_o ** 4 * (self.width * self.depth) / 12
                self.Wp = 0.2 * self.d_o ** 3 - (self.width * self.depth) / 6

            answ1 = (self.k_m / self.Wp) ** (1 / 3)
            answ2 = (self.k_m * self.d_s) / (self.G * self.Jp)

            if answ1 <= self.mat:
                answer = f'Изделие выдержит данный момент\n{round(answ1, 4)}\n{answ2}'
            else:
                answer = f'Изделие не выдержит данный момент\n{round(answ1, 4)}\n{answ2}'
            return answer
        except Exception as _ex:
            self.mysignal.emit(['Error', str(_ex)])
            return 0


class Determination_of_durability(Base_class):
    mysignal = QtCore.pyqtSignal(list)
    def init_args(self, type_bearing, n, Frad, kb_value, kt_value) -> None:
        table_bearings = {
            '204': 12.7,
            '205': 14,
            '206': 19.5,
            '207': 25.5,
            '208': 32
        }
        table_of_coefficients = {
            'Kb': {
                'Спокойная': 3,
                'Легкие толчки': 2.5,
                'Значительные толчки': 1.2,
                'Сильные удары': 1
            },
            'Kt':{
                '125 Градусов': 1.5,
                '200 Градусов': 1.25,
                '300 Градусов': 1.05
            }
        }
        self.C = table_bearings[type_bearing]
        self.n = self._checking_values(n)
        self.Frad = self._checking_values(Frad)
        self.Kb = table_of_coefficients['Kb'][kb_value]
        self.Kt = table_of_coefficients['Kt'][kt_value]

    def calculation(self) -> str:
        try:
            Fekv = self.Frad * self.Kb * self.Kt
            Lh = (10 ** 6 / (60 * self.n)) * ((self.C / Fekv) ** 3) * 1000000
            answer = f'Эквивалентная нагрузка на подшипник - {Fekv}\nДолговечность подшипника - {round(Lh, 4)} часов'
            return answer
        except Exception as _ex:
            self.mysignal.emit(['Error', str(_ex)])
            return 0


class Choice_of_the_workpice(Base_class):
    mysignal = QtCore.pyqtSignal(list)
    def init_args(self, material, massa) -> None:
        self.material = material
        self.massa = self._checking_values(massa)
        self.types_of_manufacturing = {
            'Сталь': {
                3000: 'Литье в кокиль',
                5000: 'Литье в землю',
                30: 'Литье в выпловляемую модель, ковка или штамповка',
                50: 'Литье в центробежности',
                10: 'Прокатка'
            },
            'Чугун': {
                3000: 'Литье в кокиль',
                5000: 'Литье в землю',
                30: 'Литье в выпловляемую модель, ковка или штамповка',
                50: 'Литье в центробежности'
            },
            'Латунь': {
                3000: 'Литье в кокиль',
                5000: 'Литье в землю',
                30: 'Литье в выпловляемую модель',
                50: 'Литье в центробежности'
            },
            'Бронза': {
                3000: 'Литье в кокиль',
                5000: 'Литье в землю',
                30: 'Литье в выпловляемую модель',
                50: 'Литье в центробежности',
            }
        }

    def calculation(self) -> str:
        try:
            answer = self.types_of_manufacturing[self.material].get(self.massa, 'Выбрать заготовку невозможно')
            return answer
        except Exception as _ex:
            self.mysignal.emit(['Error', str(_ex)])
            return 0


class Calculation_allowances(Base_class):
    mysignal = QtCore.pyqtSignal(list)
    def init_args(self, the_surface, Ra) -> None:
        self.the_surface = self._checking_values(the_surface)
        self.Ra = self._checking_values(Ra)
        self.__answer = 'Подходящей операции нет'
        

    def calculation(self) -> str:
        try:
            if self.the_surface == 1 and self.Ra == 15:
                self.__answer = f'Подходящая операция для поверхности {int(self.the_surface)}\nэто Фрезировка\nПрипуски = 1.5 мм'
            elif self.the_surface == 2 and 5 <= self.Ra <= 10:
                self.__answer = f'Подходящая операция для поверхности {int(self.the_surface)}\nэто Сверление\nПрипуски = 1.5 мм'
            elif (self.the_surface == 3 or self.the_surface == 5) and 20 <= self.Ra <= 40:
                self.__answer = f'Подходящая операция для поверхности {int(self.the_surface)}\nэто Точение\nПрипуски = 1.5 мм'
            elif self.the_surface == 4 and 0.25 < self.Ra <= 1:
                self.__answer = f'Подходящая операция для поверхности {int(self.the_surface)}\nэто Точение, Шлифовка и Полировка\nПрипуски = 4.5 мм'
            elif self.the_surface == 6 and 1 <= self.Ra <= 2:
                self.__answer = f'Подходящая операция для поверхности {int(self.the_surface)}\nэто Точение и Шлифовка\nПрипуски = 3 мм'

            return self.__answer
        except Exception as _ex:
            self.mysignal.emit(['Error', str(_ex)])
            return 0


class Processing_details(Base_class):
    mysignal = QtCore.pyqtSignal(list)
    def init_args(self, the_surface, Ra) -> None:
        self.the_surface = self._checking_values(the_surface)
        self.Ra = self._checking_values(Ra)
        self.__answer = 'Подходящей операции нет'
        self.table = {
            1: 'Вид станка - Фрезерный\nИнструмент - Фреза\nРежим резанья - l = 1500, S = 2 мм/с',
            2: 'Вид станка - Сверлильный\nИнструмент - Сверло\nРежим резанья - l = 2000, S = 1 мм/с',
            3: 'Вид станка - Токарный\nИнструмент - Резец\nРежим резанья - l = 1000, S = 1 мм/с',
            4: 'Вид станка - Токарный, Шлифовальный, Полировальный\nИнструмент - Резец, Шлифовальный круг, Полировальный круг и паста\
                \nРежим резанья:\n(l = 1000, S = 1 мм/с)\n(l = 500, S = 0.5 мм/с)\n(l = 100, S = 0.1 мм/с)',
            5: 'Вид станка - Токарный, Шлифовальный\nИнструмент - Резец, Шлифовальный круг\
                \nРежим резанья:\n(l = 1000, S = 1 мм/с)\n(l = 500, S = 0.5 мм/с)',
        }

    def calculation(self) -> str:
        try:
            if self.the_surface == 1 and self.Ra == 15:
                self.__answer = self.table[1]
            elif self.the_surface == 2 and 5 <= self.Ra <= 10:
                self.__answer = self.table[2]
            elif (self.the_surface == 3 or self.the_surface == 5) and 20 <= self.Ra <= 40:
                self.__answer = self.table[3]
            elif self.the_surface == 4 and 0.25 < self.Ra <= 1:
                self.__answer = self.table[4]
            elif self.the_surface == 6 and 1 <= self.Ra <= 2:
                self.__answer = self.table[5]

            return self.__answer
        except Exception as _ex:
            self.mysignal.emit(['Error', str(_ex)])
            return 0


class Route_map(Base_class):
    mysignal = QtCore.pyqtSignal(list)
    def init_args(self, operation, time) -> None:
        self.operation = operation
        self.time = self._checking_values(time)
        self.time_one_operation = 5
    def calculation(self) -> str:
        try:
            self.answer = (self.operation, self.time * self.time_one_operation)
            return self.answer
        except Exception as _ex:
            self.mysignal.emit(['Error', str(_ex)])
            return 0


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Window = App()
    Window.show()
    sys.exit(app.exec_())