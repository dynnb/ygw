from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Scrollbar, Checkbutton, Label, Button
from tkinter import ttk

import pymongo
import os
from PIL import Image, ImageTk

class YGW(Tk):
    """docstring for YGW"""
    def __init__(self):
        super().__init__()
        # 窗口设置
        self._set_window()
        # 连接数据库
        self._connect_db()
        # 初始化窗口数据
        self.result_list = list(self.collection.find())
        self.card = self.result_list[0]
        card_img_path = "data/card_icon/{}.jpg"
        img = Image.open(card_img_path.format(self.card['name_nw']))  # 打开图片
        self.photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
        # 主体窗口设计
        self._create_search_window()
        self._create_result_window()
        self._create_card_info_window()

    def _set_window(self):
        self.title("查询器")
        #设置窗口大小
        self.width = 825
        self.height = 700
        #获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        screenwidth = self.winfo_screenwidth() 
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (self.width, self.height, (screenwidth-self.width)/2, (screenheight-self.height)/2)
        self.geometry(alignstr)

    def _connect_db(self):
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client['crawl_db']
        self.collection = self.db['OCG_cards']

    def _search(self):
        query_list = []

        #关键字
        keywords = self.__keywords.get()
        if len(keywords):
            query_list.append({"$or":[{'desc_nw':{'$regex': keywords}},{'name':{'$regex': keywords}}]})

        #稀有度
        rare = self.__rare.get()
        if rare != "全部卡片":
            pass

        #等级
        level_range = self.__level.get()
        if len(level_range):
            query_list.append({"$and":[{'level':{'$gte': level_range.split('-')[0]}},{'level':{'$lte': level_range.split('-')[-1]}}]})

        #刻度
        degree_range = self.__degree.get()
        if len(degree_range):
            query_list.append({"$and":[{'level':{'$gte': degree_range.split('-')[0]}},{'level':{'$lte': degree_range.split('-')[-1]}}]})

         #攻击
        attack_range = self.__attack.get()
        if len(attack_range):
            query_list.append({"$and":[{'atk':{'$gte': attack_range.split('-')[0]}},{'atk':{'$lte': attack_range.split('-')[-1]}}]})

        #防御
        defence_range = self.__defence.get()
        if len(defence_range):
            query_list.append({"$and":[{'def':{'$gte': defence_range.split('-')[0]}},{'def':{'$lte': defence_range.split('-')[-1]}}]})

        #link值
        link_range = self.__link.get()
        if len(link_range):
            query_list.append({"$and":[{'link':{'$gte': link_range.split('-')[0]}},{'link':{'$lte': link_range.split('-')[-1]}}]})

        #属性
        attribute = self.__attribute.get()
        if attribute != "无":
            query_list.append({'attribute': attribute})


        #种族
        race = self.__race.get()
        if race != "无":
            query_list.append({'race': race})

        #魔法或陷阱类型

        card_type2 = self.__card_type2.get()
        if card_type2 != "无":
            query_list.append({'type_st':{'$regex': card_type2}})

        #其他
        other_keywords = self.__other_keywords.get()
        if other_keywords != "无":
            query_list.append({"$or":[{'type_st':{'$regex': other_keywords}},{'desc':{'$regex': other_keywords}}]})

        # #排序方式
        # sort_way = self.__sort_way.get()

        if len(query_list):
            self.result_list = list(self.collection.find({"$and": query_list}))
        else:
            self.result_list = list(self.collection.find())
        # print(query_list)
        print("查询到 {} 条数据".format(len(list(self.result_list))))
        self.after_select()
    def show_card_info(self, event):
        self.index = self.listbox.curselection()[0]
        self.set_card_img()
        self.show_card_info_window.destroy()
        self._create_card_info_window()

    def set_card_img(self):
        self.card = self.result_list[self.index]
        print("你选择了{}".format(self.card['name_nw']))
        card_img_path = "data/card_icon/{}.jpg"
        img = Image.open(card_img_path.format(self.card['name_nw']))  # 打开图片
        self.photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开

        self.show_card_img.configure(image = self.photo)
        self.show_card_img.image = self.photo # keep a reference!


    def after_select(self):
        self.result_window.destroy()
        self._create_result_window()
        self.index = 0
        self.set_card_img()

    def just_card_type(self, event):
        self.__keywords.set('')
        # self.__rare.set("全部卡片")
        self.__level.set('')
        self.__degree.set('')
        self.__attack.set('')
        self.__defence.set('')
        self.__link.set('')
        self.__attribute.set('无')
        self.__card_type2.set('无')
        self.__race.set('无')
        self.__other_keywords.set('无')
        self.__card_type2.set('无')
        
        card_type = self.__card_type.get()
        if card_type == "全部卡片":
            print("选择了全部类型")
            self.result_list = list(self.collection.find())
            self.after_select()
            self.monster_window.grid(row=3, column=0, rowspan=4, columnspan=7, pady=5, sticky=S+N+W+E)
            self.attr_window.grid(row=7, column=0, columnspan=7, pady=5, sticky=S+N+W+E)
            self.type_window.grid(row=8, column=0, columnspan=7, pady=5, sticky=S+N+W+E)
            self.race_window.grid(row=9, column=0, columnspan=7, pady=5, sticky=S+N+W+E)
            self.other_window.grid(row=10, column=0, columnspan=7, pady=5, sticky=S+N+W+E)
            # self.sort_way_window.grid(row=12, column=0, columnspan=7, pady=5, sticky=S+N+W+E)

        elif card_type == "怪兽":
            print("选择了怪兽")
            query = {"$or":[{'type_st':{'$regex': "怪兽"}},{'name':{'$regex': "怪兽"}}]}
            self.result_list = list(self.collection.find(query))
            self.after_select()
            self.monster_window.grid(row=3, column=0, rowspan=4, columnspan=7, pady=5, sticky=S+N+W+E)
            self.attr_window.grid(row=7, column=0, columnspan=7, pady=5, sticky=S+N+W+E)
            self.type_window.grid_forget()
            self.race_window.grid(row=9, column=0, columnspan=7, pady=5, sticky=S+N+W+E)
            self.other_window.grid(row=10, column=0, columnspan=7, pady=5, sticky=S+N+W+E)
            # self.sort_way_window.grid(row=12, column=0, columnspan=7, pady=5, sticky=S+N+W+E)

        else:
            print("选择了魔法或陷阱")
            query = {"$or":[{'type_st':{'$regex': card_type}},{'name':{'$regex': card_type}}]}
            self.result_list = list(self.collection.find(query))
            self.after_select()
            self.monster_window.grid_forget()
            self.attr_window.grid_forget()
            self.type_window.grid(row=8, column=0, columnspan=7, pady=5, sticky=S+N+W+E)
            self.race_window.grid_forget()
            self.other_window.grid_forget()
            # self.sort_way_window.grid_forget()

    def _create_card_info_window(self):
        self.show_card_info_window = LabelFrame(self.result_window, width=400, height=390,bg='darkgray')
        self.show_card_info_window.grid(row=1, column=0,columnspan=2, padx=5, pady=5)

        self.name_cn_key = Label(self.show_card_info_window,text = "中文名", background="gray",width=10)
        self.name_cn_key.grid(row=0, column=0, sticky=W+E)
        self.name_cn_value = Label(self.show_card_info_window, text=self.card['name_nw'],width=30)
        self.name_cn_value.grid(row=0, column=1, columnspan=5, sticky=W+E)

        self.name_ja_key = Label(self.show_card_info_window,text = "日文名", background="gray",width=10)
        self.name_ja_key.grid(row=1, column=0, sticky=W+E)
        self.name_ja_value = Label(self.show_card_info_window, text=self.card['name_ja'],width=30)
        self.name_ja_value.grid(row=1, column=1, columnspan=5, sticky=W+E)

        self.name_en_key = Label(self.show_card_info_window,text = "英文名", background="gray",width=10)
        self.name_en_key.grid(row=2, column=0, sticky=W+E)
        self.name_en_value = Label(self.show_card_info_window, text=self.card['name_en'],width=30)
        self.name_en_value.grid(row=2, column=1, columnspan=5, sticky=W+E)

        self.type_key = Label(self.show_card_info_window,text = "卡片种类", background="gray",width=10)
        self.type_key.grid(row=3, column=0, sticky=W+E)
        self.type_value = Label(self.show_card_info_window, text=self.card['type_st'],width=30)
        self.type_value.grid(row=3, column=1, columnspan=5, sticky=W+E)

        self.password_key = Label(self.show_card_info_window,text = "卡片密码", background="gray",width=10)
        self.password_key.grid(row=4, column=0, sticky=W+E)
        self.password_value = Label(self.show_card_info_window, text=self.card['password'],width=30)
        self.password_value.grid(row=4, column=1, columnspan=5, sticky=W+E)

        self.rare_key = Label(self.show_card_info_window,text = "稀有度", background="gray",width=10)
        self.rare_key.grid(row=5, column=0, sticky=W+E)
        self.rare_value = Label(self.show_card_info_window, text=self.card['rare'],width=30)
        self.rare_value.grid(row=5, column=1, columnspan=5, sticky=W+E)

    def _create_search_window(self):
        self.search_window = LabelFrame(self, width= 400, height=700)
        self.search_window.grid(row=0, column=0, padx=5, pady=5, sticky=S+N+W+E)


        #关键字查询
        self.__keywords = StringVar()
        keywords_label = Label(self.search_window, text='关键字', width=10)
        keywords_label.grid(row=0, column=0, columnspan=2, padx=5, pady=40)

        entry1 = Entry(self.search_window, textvariable=self.__keywords, width=40)
        entry1.grid(row=0, column=1, columnspan=7, padx=60, pady=40)

        #******************************卡片类型
        card_types_label = Label(self.search_window, text='卡种')
        card_types_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.__card_type=StringVar()#窗体自带的文本，新建一个值
        card_type_comboxlist=ttk.Combobox(self.search_window, state="readonly", textvariable=self.__card_type) #初始化  
        card_type_comboxlist["values"]=("全部卡片","怪兽","魔法","陷阱")  
        card_type_comboxlist.current(0)  #选择第一个  
        card_type_comboxlist.bind("<<ComboboxSelected>>",self.just_card_type)  #绑定事件,(下拉列表框被选中时，绑定go()函数)  
        card_type_comboxlist.grid(row=1, column=1, columnspan=7, padx=5, pady=5)


        #*****************************卡片稀有度
        rare_types_label = Label(self.search_window, text='稀有度')
        rare_types_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.__rare=StringVar()#窗体自带的文本，新建一个值
        self.rare_comboxlist=ttk.Combobox(self.search_window, state="readonly", textvariable=self.__rare) #初始化  
        self.rare_comboxlist["values"]=("全部卡片","OCG独有","TCG独有","OT通用")  
        self.rare_comboxlist.current(0)  #选择第一个  
        # rare_comboxlist.bind("<<ComboboxSelected>>",self.just_card_type)  #绑定事件,(下拉列表框被选中时，绑定go()函数)  
        self.rare_comboxlist.grid(row=2, column=1, columnspan=7, padx=5, pady=5)

        #****************************monster
        self.monster_window = LabelFrame(self.search_window)
        self.monster_window.grid(row=3, column=0, rowspan=4, columnspan=7, pady=5, sticky=S+N+W+E)
        #星阶
        level_label = Label(self.monster_window, text='星阶', width=10)
        level_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.__level = StringVar()
        self.entry2 = Entry(self.monster_window, textvariable=self.__level, width=40)
        self.entry2.grid(row=0, column=1, columnspan=7, padx=60, pady=5)

        #刻度
        degree_label = Label(self.monster_window, text='刻度', width=10)
        degree_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.__degree = StringVar()
        entry3 = Entry(self.monster_window, textvariable=self.__degree, width=40)
        entry3.grid(row=1, column=1, columnspan=7, padx=60, pady=5)

        #攻击力
        attack_label = Label(self.monster_window, text='攻击力', width=10)
        attack_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.__attack = StringVar()
        entry4 = Entry(self.monster_window, textvariable=self.__attack, width=40)
        entry4.grid(row=2, column=1, columnspan=7, padx=60, pady=5)

        #防御力
        defence_label = Label(self.monster_window, text='防御力', width=10)
        defence_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.__defence = StringVar()
        entry5 = Entry(self.monster_window, textvariable=self.__defence, width=40)
        entry5.grid(row=3, column=1, columnspan=7, padx=60, pady=5)

        #link值
        link_label = Label(self.monster_window, text='link值', width=10)
        link_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        self.__link = StringVar()
        entry6 = Entry(self.monster_window, textvariable=self.__link, width=40)
        entry6.grid(row=4, column=1, columnspan=7, padx=60, pady=5)

        #属性
        self.attr_window = LabelFrame(self.search_window, width= 390, height=50)
        self.attr_window.grid(row=7, column=0, columnspan=7, pady=5, sticky=S+N+W+E)
        
        attribute_label = Label(self.attr_window, text='属性', width=10)
        attribute_label.grid(row=7,column=0, columnspan=2, padx=5, pady=5)

        self.attribute_list=["无","光","地","暗","水","炎","神","风"] 
        #定义变量
        self.__attribute = StringVar()
        self.__attribute.set("无")
        #计数器
        counter1=0 
        #循环创建选项
        for i in self.attribute_list: 
            #创建单选框并居中
        #     checkbutton=Radiobutton(root,text=i,variable=variable,value=counter) 
            checkbutton = Radiobutton(self.attr_window, text=i, variable=self.__attribute, value=self.attribute_list[counter1], indicatoron=False)
            #计数器自加
            counter1 += 1 
            checkbutton.grid(row=7, column=counter1+1, padx=10, pady=5)



        #类型
        self.type_window = LabelFrame(self.search_window, width= 390, height=50)
        self.type_window.grid(row=8, column=0, columnspan=7, pady=5, sticky=S+N+W+E)

        self.card_type_label = Label(self.type_window, text='类型', width=10)
        self.card_type_label.grid(row=8,column=0, columnspan=2, padx=5, pady=5)

        self.card_type_list=["无" ,"装备","场地","速攻","仪式","永续","反击","通常"]

        #定义变量
        self.__card_type2=StringVar()
        self.__card_type2.set("无")
        #计数器
        counter2=0 
        #循环创建选项
        for i in self.card_type_list: 
            #创建单选框并居中

            self.check_card_type_button = Radiobutton(self.type_window, text=i, variable=self.__card_type2, value=self.card_type_list[counter2], indicatoron=False)
            #计数器自加
            counter2 += 1 
            self.check_card_type_button.grid(row=8, column=counter2+1, padx=4, pady=5)

        #种族
        self.race_window = LabelFrame(self.search_window, width= 390, height=50)
        self.race_window.grid(row=9, column=0, columnspan=7, pady=5, sticky=S+N+W+E)

        race_label = Label(self.race_window, text='种族', width=10)
        race_label.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        self.race_list=["无",'水','兽','兽战士','创造神','恐龙','幻神兽','龙','天使','恶魔','鱼','昆虫','机械','植物','念动力','炎','爬虫类','岩石','海龙','魔法师','雷','战士','鸟兽','不死','幻龙','电子界']
        #定义变量
        self.__race=StringVar()
        self.__race.set("无")
        #计数器
        counter3 = 0 
        #循环创建选项
        for i in self.race_list: 

            #创建单选框并居中
        #     checkbutton=Radiobutton(root,text=i,variable=variable,value=counter) 
            checkbutton = Radiobutton(self.race_window, text=i, variable=self.__race, value=self.race_list[counter3], indicatoron=False)
            #计数器自加
            counter3 += 1 
            checkbutton.grid(row=9+counter3//7, column=1+counter3%7, padx=3, pady=5)

        #其他
        self.other_window = LabelFrame(self.search_window, width= 390, height=50)
        self.other_window.grid(row=10, column=0, columnspan=7, pady=5, sticky=S+N+W+E)

        other_label = Label(self.other_window, text='其他', width=10)
        other_label.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

        self.other_list=["无",'通常','效果','仪式','融合','同调','XYZ','卡通','同盟','灵魂','调整','二重','灵摆','反转','特殊召唤','连接']
        #定义变量
        self.__other_keywords = StringVar()
        self.__other_keywords.set("无")
        #计数器
        counter4 = 0 
        #循环创建选项
        for i in self.other_list: 

            #创建单选框并居中
        #     checkbutton=Radiobutton(root,text=i,variable=variable,value=counter) 
            checkbutton = Radiobutton(self.other_window, text=i, variable=self.__other_keywords, value=self.other_list[counter4], indicatoron=False)
            #计数器自加
            counter4 += 1 
            checkbutton.grid(row=10+counter4//7, column=1+counter4%7, padx=3, pady=5)

        #***************************卡片排序
        # self.sort_way_window = LabelFrame(self.search_window)
        # self.sort_way_window.grid(row=12, column=0, columnspan=7, pady=5, sticky=S+N+W+E)

        # sort_way_label = Label(self.sort_way_window, text='排序')
        # sort_way_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # self.__sort_way=StringVar()#窗体自带的文本，新建一个值
        # sortway_comboxlist=ttk.Combobox(self.sort_way_window, state="readonly", textvariable=self.__sort_way) #初始化  
        # sortway_comboxlist["values"]=("卡片排序","等级从高到低","等级从低到高", "攻击力从大到小", "攻击力从小到大", "防御力从大到小", "防御力从小到大")  
        # sortway_comboxlist.current(0)  #选择第一个  
        # # sortway_comboxlist.bind("<<ComboboxSelected>>",self.just_card_type)  #绑定事件,(下拉列表框被选中时，绑定go()函数)  
        # sortway_comboxlist.grid(row=0, column=2, columnspan=7, padx=80, pady=5)


        #***************************搜索按钮
        search_button = Button(self.search_window, text="搜索", command=self._search)
        search_button.grid(row=13, column=1, columnspan=7, padx=5, pady=15)



    def _create_result_window(self):
        self.result_window = LabelFrame(self, width= 520, height=700, bg="red")
        self.result_window.grid(row=0, column=1, padx=5, pady=5, sticky=S+N+W+E)
        self.top_left_window = LabelFrame(self.result_window, width=210,height=240, bg='black')
        self.top_left_window.grid(row=0, column=0, sticky=S+N+W)


        #创建滑块
        scrollbar = Scrollbar(self.top_left_window)
        scrollbar.grid(row=0, column=1, sticky=W+E+S+N)
        
        self.listbox = Listbox(self.top_left_window, width=22, height=19, selectmode=BROWSE, yscrollcommand=scrollbar.set,bg='gray')
        self.listbox.grid(row=0,column=0, sticky=W+S+N)
        self.listbox.bind("<<ListboxSelect>>", self.show_card_info)
        # print(self.result_list[0])
        for result in self.result_list:
            self.listbox.insert(END,result['name'])

        scrollbar.config(command=self.listbox.yview)

        self.show_card_img = Label(self.result_window, width=230, image=self.photo, background="yellow")
        self.show_card_img.grid(row=0, column=1, sticky=S+N+E)
if __name__ == "__main__":
    app = YGW()
    app.mainloop()


        