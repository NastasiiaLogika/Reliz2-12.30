from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget

from app import app
from data import *
from main_layout import*
from card_layout import *
#from edit_layout import txt_Question, txt_Answer, txt_Wrong1, txt_Wrong2, txt_Wrong3

# Константи
main_width, main_height = 1000, 450 # початкові розміри головного вікна
card_width, card_height = 600, 500 # початкові розміри вікна "картка"
time_unit = 1000 

# Глобальні змінні
questions_listmodel = QuestionListModel() # список запитань
#frm_edit = QuestionEdit(0, txt_Question, txt_Answer, txt_Wrong1, txt_Wrong2, txt_Wrong3) # запам'ятовуємо, що у формі редагування питання з чим пов'язано
radio_list = [rbtn_1, rbtn_2, rbtn_3, rbtn_4] 
frm_card = 0
timer = QTimer()
win_card = QWidget() 
win_main = QWidget() 

def testlist():
    frm = Question("Яка столиця бразилії?", 'бразиліа', 'Київ', 'Париж', 'оттава')
    questions_listmodel.form_list.append(frm)
    frm = Question("що розділяє нашу землю на південну та північеу пів кулю?", 'екватор', 'мередіан', 'океан', 'сша')
    questions_listmodel.form_list.append(frm)
    frm = Question("Що харектеризує для осеедку землетрусу?", 'утворення зсувів', 'виникнення цунамі', 'перетворення магми на лаву', 'розрив і зміщення земної кори')
    questions_listmodel.form_list.append(frm)
    frm = Question("Яке море не має берегів?", 'Сергасове', 'чорне', 'біле', 'червоне')
    questions_listmodel.form_list.append(frm)
    frm = Question("Країна яка не має столиці?", 'Швейцарія', 'Україна', 'англія', 'сша')
    questions_listmodel.form_list.append(frm)
    frm = Question("Що таке тітікака?", 'озеро', 'море', 'місто', 'країна')
    questions_listmodel.form_list.append(frm)
    frm = Question("У якій країні найбільше островів?", 'Щвеція', 'Англія', 'Китай', 'Бразилія')
    questions_listmodel.form_list.append(frm)


# Функції для проведення тесту
def set_card():
    ''' задає, який вигляд має вікно картки'''
    win_card.resize(card_width, card_height)
    win_card.move(300, 300)
    win_card.setWindowTitle('Memory Card')
    win_card.setLayout(layout_card)

def sleep_card():
    ''' картка ховається на час, зазначений у таймері'''
    win_card.hide()
    timer.setInterval(time_unit * box_Minutes.value() )
    timer.start()

def show_card():
    ''' показує вікно (за таймером), таймер зупиняється'''
    win_card.show()
    timer.stop()

def show_random():
    ''' показати випадкове запитання '''
    global frm_card
    frm_card = random_AnswerCheck(questions_listmodel, lb_Question, radio_list, lb_Correct, lb_Result)
    frm_card.show()
    show_question() 

def click_OK():
    ''' перевіряє запитання або завантажує нове запитання '''
    if btn_OK.text() != 'Наступне питання':
        frm_card.check()
        show_result()
    else:
        show_random()

def back_to_menu():
    ''' повернення з тесту у вікно редактора '''
    win_card.hide()
    win_main.showNormal()

# Функції для редагування питань
def set_main():
    ''' задає, який вигляд має основне вікно'''
    win_main.resize(main_width, main_height)
    win_main.move(100, 100)
    win_main.setWindowTitle('Список питань')
    win_main.setLayout(layout_main)

def edit_question(index):
    ''' завантажує у форму редагування запитання і відповіді, що відповідають переданому рядку '''
    if index.isValid():
        i = index.row()
        frm = questions_listmodel.form_list[i]
        #frm_edit.change(frm)
        #frm_edit.show()

def add_form():
    ''' додає нове запитання і пропонує його змінити '''
    questions_listmodel.insertRows() 
    last = questions_listmodel.rowCount(0) - 1  
    
    index = questions_listmodel.index(
        last)  
    list_questions.setCurrentIndex(index)
    edit_question(index) 


def del_form():
    ''' видаляє питання і перемикає фокус '''
    questions_listmodel.removeRows(list_questions.currentIndex().row())
    edit_question(list_questions.currentIndex())

def start_test():
    ''' на початку тесту форма зв'язується з випадковим питанням і показується '''
    show_random()
    win_card.show()
    win_main.showMinimized()

# Встановлення потрібних з`єднань
def connects():
    list_questions.setModel(questions_listmodel) 
    list_questions.clicked.connect(edit_question)
    btn_add.clicked.connect(add_form) 
    btn_delete.clicked.connect(del_form) 
    btn_start.clicked.connect(start_test) # натискання кнопки "почати тест"
    btn_OK.clicked.connect(click_OK) # натискання кнопки "OK" на формі тесту
    btn_Menu.clicked.connect(back_to_menu) # натискання кнопки "Меню" для повернення з форми тесту в редактор запитань
    timer.timeout.connect(show_card) # показуємо форму тесту після закінчення таймера
    btn_Sleep.clicked.connect(sleep_card) # натискання кнопки "спати" у картки-тесту

# Запуск програми
testlist()
set_card()
set_main()
connects()
win_main.show()
app.exec_()