import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import scrolledtext
import cx_Oracle
import csv
from tkinter import ttk
from openpyxl import Workbook
from tkinter import filedialog
class gui_tree:
    def __init__(self, master):
        self.master = master
        self.dbconn()
        self.create_menu()
        self.tree = None
    def dbconn(self):
        global conn
        global cur
        conn = cx_Oracle.connect(user="tree", password="1234", dsn="localhost:1521/xe")
        cur = conn.cursor()
    def create_menu(self):
        l0=Label(self.master,text="수종 검색 프로그램\n",font=(15))
        l1=Label(self.master,text="메뉴를 클릭하세요")
        self.var=IntVar()
        rb1=Radiobutton(self.master,text="별칭 찾기",variable=self.var,value=1,command=self.func_radiobutton)
        rb2=Radiobutton(self.master,text="유물 찾기",variable=self.var,value=2,command=self.func_radiobutton)
        rb3=Radiobutton(self.master,text="식별코드로 정명 조회",variable=self.var,value=3,command=self.func_radiobutton)
        rb4=Radiobutton(self.master,text="활엽수 식별코드 표",variable=self.var,value=4,command=self.func_radiobutton)
        rb5=Radiobutton(self.master,text="침엽수 식별코드 표",variable=self.var,value=5,command=self.func_radiobutton)
        rb6=Radiobutton(self.master,text="창 닫기",variable=self.var,value=6,command=self.func_radiobutton)
        l0.pack()
        l1.pack()
        rb1.pack()
        rb2.pack()
        rb3.pack()
        rb4.pack()
        rb5.pack()
        rb6.pack()
        w.mainloop()
    def func_quit(self):
        if messagebox.askokcancel("확인", "정말로 종료하시겠습니까?"):
            self.master.quit()
            self.master.destroy()
            conn.close()
    def destroy_new_window(self):
        global new_win
        new_win.destroy()
        text=Text(self.master)
        text.insert(INSERT," ")
        text.place(x=1,y=220)
    def export_to_excel(self):
        wb = Workbook()
        ws = wb.active
        headers = [self.tree.heading(col, "text") for col in self.tree["columns"]]
        ws.append(headers)
        for item in self.tree.get_children():
            values = [str(value) for value in self.tree.item(item, "values")]
            ws.append(values)
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            wb.save(file_path)
    def func_searchname(self):
        global new_win
        new_win=Tk()
        new_win.title('별칭 찾기')
        new_win.geometry("450x40+400+200")
        e1=Entry(new_win,width=20)
        combo1=Combobox(new_win,width=5)
        combo1['values']=("정명","이명","국명정명","국명이명","영문명","일본명","북한명")
        combo1.current(1)
        b0k=Button(new_win,text="찾기",command=lambda: self.find_name(combo1.get(),e1.get()))
        bCancel=Button(new_win,text="취소",command=self.destroy_new_window)
        combo1.grid(row=0,column=0,padx=5,pady=5)
        e1.grid(row=0,column=1,padx=5,pady=5)
        b0k.grid(row=0,column=2,padx=5,pady=5)
        bCancel.grid(row=0,column=3,padx=5,pady=5)
        new_win.mainloop()
        w.mainloop()
    def find_name(self,name_type,name):
        global cur
        if name_type=="정명":
            sql=f"select acceptname,decode(name_type,1,'이명',2,'국명정명',3,'영문명',4,'일본명',5,'북한명',name_type), other_names from other_names where acceptname like '%{name}%'"
        elif name_type=="이명":
            sql=f"select acceptname,decode(name_type,1,'이명',2,'국명정명',3,'영문명',4,'일본명',5,'북한명',name_type), other_names from other_names where name_type={1} and other_names like '%{name}%'"
        elif name_type=="국명정명":
            sql=f"select acceptname,decode(name_type,1,'이명',2,'국명정명',3,'영문명',4,'일본명',5,'북한명',name_type), other_names from other_names where name_type={2} and other_names like '%{name}%'"
        elif name_type=="영문명":
            sql=f"select acceptname,decode(name_type,1,'이명',2,'국명정명',3,'영문명',4,'일본명',5,'북한명',name_type), other_names from other_names where name_type={3} and other_names like '%{name}%'"
        elif name_type=="일본명":
            sql=f"select acceptname,decode(name_type,1,'이명',2,'국명정명',3,'영문명',4,'일본명',5,'북한명',name_type), other_names from other_names where name_type={4} and other_names like '%{name}%'"
        elif name_type=="북한명":
            sql=f"select acceptname,decode(name_type,1,'이명',2,'국명정명',3,'영문명',4,'일본명',5,'북한명',name_type), other_names from other_names where name_type={5} and other_names like '%{name}%'"
        rs=cur.execute(sql)
        data=cur.fetchall()
        w=Tk()
        w.geometry("1350x300")
        w.title('별칭')
        tree_frame = ttk.Frame(w, width=1350, height=300)
        tree_frame.pack(fill='both')
        self.tree = ttk.Treeview(tree_frame, columns=("1", "2"))
        self.tree.column("#0", width=500, minwidth=200, stretch=tk.NO)
        self.tree.column("1", width=200, minwidth=200, stretch=tk.NO)
        self.tree.column("2", width=900, minwidth=200, stretch=tk.NO)
        self.tree.heading("#0", text="정명")
        self.tree.heading("1", text="별칭유형")
        self.tree.heading("2", text="별칭")
        xscrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        xscrollbar.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=xscrollbar.set)
        yscrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        yscrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=yscrollbar.set)
        for i, row in enumerate(data):
            self.tree.insert(parent='', index='end', iid=i, text=row[0], values=(row[1], row[2]))
        self.tree.pack(fill="both")
        export_button = tk.Button(w, text="Export to Excel", command=self.export_to_excel)
        export_button.pack()
    def func_searcharch(self):
        global new_win
        new_win=Tk()
        new_win.title('유물 찾기')
        new_win.geometry("450x40+400+200")
        combo1=Combobox(new_win,width=5)
        combo1['values']=("acceptname","name","material","period","category1","category2","category3","category4","cultural_number","reference")
        combo1.current(1)
        e1=Entry(new_win,width=20)
        b0k=Button(new_win,text="찾기",command=lambda : self.find_arch(combo1.get(),e1.get()))
        bCancel=Button(new_win,text="취소",command=self.destroy_new_window)
        combo1.grid(row=0,column=0,padx=5,pady=5)
        e1.grid(row=0,column=1,padx=5,pady=5)
        b0k.grid(row=0,column=2,padx=5,pady=5)
        bCancel.grid(row=0,column=3,padx=5,pady=5)
        new_win.mainloop()
        w.mainloop()
    def find_arch(self,col,row):
        global cur
        sql=f"select acceptname,name,material,period,category,cultural_number,reference from e_museum where {col} like '%{row}%'"
        rs=cur.execute(sql)
        data=cur.fetchall()
        w=Tk()
        w.geometry("1100x300")
        w.title('유물')
        tree_frame = ttk.Frame(w)
        tree_frame.pack(fill='both')
        self.tree = ttk.Treeview(tree_frame, columns=("1", "2", "3", "4", "5", "6"))
        self.tree.column("#0", width=200, minwidth=200, stretch=tk.NO)
        self.tree.column("1", width=200, minwidth=200, stretch=tk.NO)
        self.tree.column("2", width=100, minwidth=200, stretch=tk.NO)
        self.tree.column("3", width=100, minwidth=200, stretch=tk.NO)
        self.tree.column("4", width=100, minwidth=200, stretch=tk.NO)
        self.tree.column("5", width=200, minwidth=200, stretch=tk.NO)
        self.tree.column("6", width=200, minwidth=200, stretch=tk.NO)
        self.tree.heading("#0", text="정명")
        self.tree.heading("1", text="유물명")
        self.tree.heading("2", text="재질")
        self.tree.heading("3", text="시대")
        self.tree.heading("4", text="분류")
        self.tree.heading("5", text="소장번호")
        self.tree.heading("6", text="소장기관")
        yscrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        yscrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=yscrollbar.set)
        for i, row in enumerate(data):
            self.tree.insert(parent='', index='end', iid=i, text=row[0], values=(row[1], row[2],row[3],row[4],row[5],row[6]))
        self.tree.pack()
        export_button = tk.Button(w, text="Export to Excel", command=self.export_to_excel)
        export_button.pack()
    def func_searchcode(self):
        global new_win
        new_win=Tk()
        new_win.title('식별코드로 정명 조회')
        new_win.geometry("380x170+400+200")
        combo1=Combobox(new_win,width=5)
        combo1['values']=("HW","SW")
        combo1.current(1)
        l1=Label(new_win,text='AND')
        l2=Label(new_win,text='OR')
        l3=Label(new_win,text='NOT IN')
        e1=Entry(new_win,width=35)
        e2=Entry(new_win,width=35)
        e3=Entry(new_win,width=35)
        b0k=Button(new_win,text="찾기",command=lambda : self.find_code(combo1.get(),e1.get(),e2.get(),e3.get()))
        bCancel=Button(new_win,text="취소",command=self.destroy_new_window)
        combo1.grid(row=0,column=0,padx=5,pady=5)
        l1.grid(row=1,column=0,padx=5,pady=5)
        e1.grid(row=1,column=1,padx=5,pady=5)
        b0k.grid(row=4,column=0,padx=5,pady=5)
        bCancel.grid(row=4,column=1,padx=5,pady=5)
        l2.grid(row=2,column=0,padx=5,pady=5)
        l3.grid(row=3,column=0,padx=5,pady=5)
        e2.grid(row=2,column=1,padx=5,pady=5)
        e3.grid(row=3,column=1,padx=5,pady=5)
        new_win.mainloop()
        w.mainloop()
    def find_code(self,TYPE,AND,OR,NOTIN):
        global cur
        w=Tk()
        w.geometry("1800x300")
        w.title('식별코드')
        x1=AND.split(" ")
        x2=NOTIN.split(" ")
        x3=OR.split(" ")
        massage = ""
        def fun_start(x,y):
            return f"SELECT id_acceptname,acceptname,code_reference FROM acceptname WHERE ID_acceptname IN (SELECT acceptname_ID FROM {y}_woodcode_has_acceptname WHERE {y}_woodcode_id = '{x}'"
        def fun_start2(x,y):
            return f"SELECT id_acceptname,acceptname,code_reference FROM acceptname WHERE wood_code !=' ' and wood_type='{y}' and ID_acceptname IN (SELECT acceptname_ID FROM {y}_woodcode_has_acceptname WHERE {y}_woodcode_id NOT IN '{x}'"
        def fun_and(x,y):
            return f"AND acceptname_ID IN (SELECT acceptname_ID FROM {y}_woodcode_has_acceptname WHERE {y}_woodcode_id = '{x}'"
        def fun_notin(x,y):
            return f"AND acceptname_ID NOT IN (SELECT acceptname_ID FROM {y}_woodcode_has_acceptname WHERE {y}_woodcode_id = '{x}'"
        def fun_notin2(x,y):
            return f"or acceptname_ID IN (SELECT acceptname_ID FROM {y}_woodcode_has_acceptname WHERE {y}_woodcode_id = '{x}'"
        def fun_or(x,y):
            return f"(select count(*) from {y}_woodcode_has_acceptname where acceptname_id=acceptname.ID_acceptname and {y}_woodcode_id={x})"
        if x1[0]=="":
            massage=fun_start2(9999,TYPE)
            if x2[0]=="":
                massage=massage+fun_notin(9999,TYPE)
            else:
                if len(x2)==1:
                    massage=massage+fun_notin(x2[0],TYPE)
                else:
                    massage=massage+fun_notin(x2[0],TYPE)
                    for var in x2[1:]:
                        massage+=fun_notin2(var,TYPE)
            massage=massage+ ")"*(len(x2)+1)
        else:
            if len(x1)==1:
                massage=fun_start(x1[0],TYPE)
            else:
                massage=fun_start(x1[0],TYPE)
                for var in x1[1:]:
                    massage+=fun_and(var,TYPE)
            if len(x2)==1:
                massage=massage+fun_notin(x2[0],TYPE)
            else:
                massage=massage+fun_notin(x2[0],TYPE)
                for var in x2[1:]:
                    massage+=fun_notin2(var,TYPE)
            massage =massage+ ")"*(len(x1)+len(x2))
        if x3[0] == "":
            pass
        else:
            if len(x3) == 1:
                massage = massage + f"ORDER BY {fun_or(x3[0], TYPE)} DESC"
            else:
                massage = massage + f"ORDER BY ({fun_or(x3[0], TYPE)}"
                for var in x3[1:]:
                    massage += "+" + fun_or(var, TYPE)
                massage = massage + ") DESC"
        cur.execute(massage)
        total = cur.fetchall()
        code_id=[]
        sub2=[]
        list1=[]
        for var in total:
            code_id.append(var[0])
        for var1 in code_id:
            if x1[0]=="" and x3[0]=="":
                massage2=f"select {TYPE}_woodcode_id,letters from {TYPE}_woodcode_has_acceptname where acceptname_id = '{var1}'"
                cur.execute(massage2)
                sub=cur.fetchall()
                for var2,var3 in sub:
                    if type(var3) == str:
                        sub2.append(str(var2)+var3)
                    else:
                        sub2.append(str(var2))
                list1.append(sub2)
                sub2=[]
            elif x3[0]=="":
                massage2=f"select {TYPE}_woodcode_id,letters from {TYPE}_woodcode_has_acceptname where acceptname_id = '{var1}' and {TYPE}_woodcode_id in ({','.join(x1)})"
                cur.execute(massage2)
                sub=cur.fetchall()
                for var2,var3 in sub:
                    if type(var3) == str:
                        sub2.append(str(var2)+var3)
                    else:
                        sub2.append(str(var2))
                list1.append(sub2)
                sub2=[]
            elif x1[0]=="":
                massage2=f"select {TYPE}_woodcode_id,letters from {TYPE}_woodcode_has_acceptname where acceptname_id = '{var1}' and {TYPE}_woodcode_id in ({','.join(x3)})"
                cur.execute(massage2)
                sub=cur.fetchall()
                for var2,var3 in sub:
                    if type(var3) == str:
                        sub2.append(str(var2)+var3)
                    else:
                        sub2.append(str(var2))
                list1.append(sub2)
                sub2=[]
            else:
                massage2=f"select {TYPE}_woodcode_id,letters from {TYPE}_woodcode_has_acceptname where acceptname_id = '{var1}' and {TYPE}_woodcode_id in ({','.join(x1+x3)})"
                cur.execute(massage2)
                sub=cur.fetchall()
                for var2,var3 in sub:
                    if type(var3) == str:
                        sub2.append(str(var2)+var3)
                    else:
                        sub2.append(str(var2))
                list1.append(sub2)
                sub2=[]
        list2=[]
        all_number=[]
        start_index = massage.find("(")
        end_index = massage.find("ORDER BY")
        massage3 = massage[start_index:end_index]
        code1 = f"SELECT {TYPE}_woodcode_id, MAX({TYPE}_woodcode_has_acceptname.letters) AS letters FROM {TYPE}_woodcode_has_acceptname WHERE acceptname_ID IN "
        code2 = f" GROUP BY {TYPE}_woodcode_id HAVING COUNT(DISTINCT acceptname_ID) = (SELECT COUNT(DISTINCT acceptname_ID) FROM {TYPE}_woodcode_has_acceptname WHERE acceptname_ID IN "
        if x3[0]=="":
            result = ', '.join([f"'{elem}'" for elem in (x1)])
        else:
            result = ', '.join([f"'{elem}'" for elem in (x1+x3)])
        code3= f" AND {TYPE}_woodcode_id NOT IN ({result})"
        if x3[0]=="":
            massage3_total = code1 + massage3+")"+code3+code2 + massage3 + ")" + ")"
        else:
            massage3_total = code1 + massage3 +code3+code2 + massage3 + ")"
        cur.execute(massage3_total)
        sub=cur.fetchall()
        if len(sub)==0:
            list2.append("없음")
            all_number.append("없음")
        else:
            for var in sub:
                all_number.append(str(var[0]))
                if type(var[1])==str:
                    list2.append(str(var[0])+var[1])
                else:
                    list2.append(str(var[0]))
        list3=[]
        for var2 in code_id:
            if all_number[0]=="없음":
                if x1[0]=="" and x3[0]=="":
                    massage2=f"select {TYPE}_woodcode_id,letters from {TYPE}_woodcode_has_acceptname where acceptname_id = '{var2}'"
                    cur.execute(massage2)
                    sub=cur.fetchall()
                    for var2,var3 in sub:
                        if type(var3) == str:
                            sub2.append(str(var2)+var3)
                        else:
                            sub2.append(str(var2))
                    list3.append(sub2)
                    sub2=[]
                elif x3[0]=="":
                    massage2=f"select {TYPE}_woodcode_id,letters from {TYPE}_woodcode_has_acceptname where acceptname_id = '{var2}' and {TYPE}_woodcode_id not in ({','.join(x1)})"
                    cur.execute(massage2)
                    sub=cur.fetchall()
                    for var2,var3 in sub:
                        if type(var3) == str:
                            sub2.append(str(var2)+var3)
                        else:
                            sub2.append(str(var2))
                    list3.append(sub2)
                    sub2=[]
                elif x1[0]=="":
                    massage2=f"select {TYPE}_woodcode_id,letters from {TYPE}_woodcode_has_acceptname where acceptname_id = '{var2}' and {TYPE}_woodcode_id not in ({','.join(x3)})"
                    cur.execute(massage2)
                    sub=cur.fetchall()
                    for var2,var3 in sub:
                        if type(var3) == str:
                            sub2.append(str(var2)+var3)
                        else:
                            sub2.append(str(var2))
                    list3.append(sub2)
                    sub2=[]
                else:
                    massage2=f"select {TYPE}_woodcode_id,letters from {TYPE}_woodcode_has_acceptname where acceptname_id = '{var2}' and {TYPE}_woodcode_id not in ({','.join(x1+x3)})"
                    cur.execute(massage2)
                    sub=cur.fetchall()
                    for var2,var3 in sub:
                        if type(var3) == str:
                            sub2.append(str(var2)+var3)
                        else:
                            sub2.append(str(var2))
                    list3.append(sub2)
                    sub2=[]
            else:
                if x1[0]=="" and x3[0]=="":
                    massage4=f"select {TYPE}_woodcode_id,letters from {TYPE}_woodcode_has_acceptname where acceptname_id = '{var2}' and {TYPE}_woodcode_id not in ({','.join(all_number)})"
                    cur.execute(massage4)
                    sub=cur.fetchall()
                    for var2,var3 in sub:
                        if type(var3) == str:
                            sub2.append(str(var2)+var3)
                        else:
                            sub2.append(str(var2))
                    list3.append(sub2)
                    sub2=[]
                elif x3[0]=="":
                    massage4=f"select {TYPE}_woodcode_id,letters from {TYPE}_woodcode_has_acceptname where acceptname_id = '{var2}' and {TYPE}_woodcode_id not in ({','.join(x1+all_number)})"
                    cur.execute(massage4)
                    sub=cur.fetchall()
                    for var2,var3 in sub:
                        if type(var3) == str:
                            sub2.append(str(var2)+var3)
                        else:
                            sub2.append(str(var2))
                    list3.append(sub2)
                    sub2=[]
                elif x1[0]=="":
                    massage4=f"select {TYPE}_woodcode_id,letters from {TYPE}_woodcode_has_acceptname where acceptname_id = '{var2}' and {TYPE}_woodcode_id not in ({','.join(x3+all_number)})"
                    cur.execute(massage4)
                    sub=cur.fetchall()
                    for var2,var3 in sub:
                        if type(var3) == str:
                            sub2.append(str(var2)+var3)
                        else:
                            sub2.append(str(var2))
                    list3.append(sub2)
                    sub2=[]
                else:
                    massage4=f"select {TYPE}_woodcode_id,letters from {TYPE}_woodcode_has_acceptname where acceptname_id = '{var2}' and {TYPE}_woodcode_id not in ({','.join(x1+x3+all_number)})"
                    cur.execute(massage4)
                    sub=cur.fetchall()
                    for var2,var3 in sub:
                        if type(var3) == str:
                            sub2.append(str(var2)+var3)
                        else:
                            sub2.append(str(var2))
                    list3.append(sub2)
                    sub2=[]
        tree_frame = ttk.Frame(w)
        tree_frame.pack(fill='both')
        self.tree = ttk.Treeview(tree_frame, columns=("1","2","3","4"))
        self.tree.column("#0", width=400, minwidth=200, stretch=tk.NO)
        self.tree.column("1", width=300, minwidth=200, stretch=tk.NO)
        self.tree.column("2", width=400, minwidth=200, stretch=tk.NO)
        self.tree.column("3", width=1000, minwidth=200, stretch=tk.NO)
        self.tree.column("4", width=1000, minwidth=200, stretch=tk.NO)
        self.tree.heading("#0", text="정명")
        self.tree.heading("1", text="검색코드")
        self.tree.heading("2", text="공통코드")
        self.tree.heading("3", text="나머지코드")
        self.tree.heading("4", text="참고문헌")
        xscrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        xscrollbar.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=xscrollbar.set)
        yscrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        yscrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=yscrollbar.set)
        if len(list3)==0:
            if list2[0]=="없음":
                for i, (row1,row2) in enumerate(zip(total,list1)):
                    self.tree.insert(parent='', index='end', iid=i, text=row1[1], values=((", ".join(row2)),("없음"),("없음",),(row1[2],)))
            else:
                for i, (row1,row2) in enumerate(zip(total,list1)):
                    self.tree.insert(parent='', index='end', iid=i, text=row1[1], values=(((", ".join(row2)),(", ".join(list2)),("없음",),(row1[2],))))
        else:
            if list2[0]=="없음":
                for i, (row1,row2,row3) in enumerate(zip(total,list1,list3)):
                    self.tree.insert(parent='', index='end', iid=i, text=row1[1], values=((", ".join(row2)),("없음"),(", ".join(row3)),(row1[2],)))
            else:
                for i, (row1,row2,row3) in enumerate(zip(total,list1,list3)):
                    self.tree.insert(parent='', index='end', iid=i, text=row1[1], values=((", ".join(row2)),(", ".join(list2)),(", ".join(row3)),(row1[2],)))
        self.tree.pack()
        export_button = tk.Button(w, text="Export to Excel", command=self.export_to_excel)
        export_button.pack()
    def func_hw_code(self):
        global new_win
        new_win=Tk()
        new_win.title('활엽수 식별 코드 표')
        tree_frame = ttk.Frame(new_win)
        tree_frame.pack(fill='both')
        self.tree = ttk.Treeview(tree_frame, columns=("1","2","3"))
        self.tree.column("#0", width=200, minwidth=200, stretch=tk.NO)
        self.tree.column("1", width=350, minwidth=200, stretch=tk.NO)
        self.tree.column("2", width=100, minwidth=100, stretch=tk.NO)
        self.tree.column("3", width=800, minwidth=200, stretch=tk.NO)
        self.tree.heading("#0", text="대분류")
        self.tree.heading("1", text="중분류")
        self.tree.heading("2", text="소분류")
        self.tree.heading("3", text="설명")
        xscrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        xscrollbar.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=xscrollbar.set)
        yscrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        yscrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=yscrollbar.set)
        temp = open("D:/작업할 거/프로젝트/활엽수.csv", encoding='utf-8')
        rdr = csv.reader(temp)
        data3 = []
        for var in rdr:
            data3.append(var)
        for i, row in enumerate(data3):
            self.tree.insert(parent='', index='end', iid=i, text=row[0], values=((row[1],),(row[2],),(row[3],)))
        self.tree.pack()
    def func_sw_code(self):
        global new_win
        new_win=Tk()
        new_win.title('침엽수 식별 코드 표')
        tree_frame = ttk.Frame(new_win)
        tree_frame.pack(fill='both')
        self.tree = ttk.Treeview(tree_frame, columns=("1","2","3"))
        self.tree.column("#0", width=200, minwidth=200, stretch=tk.NO)
        self.tree.column("1", width=700, minwidth=200, stretch=tk.NO)
        self.tree.column("2", width=100, minwidth=100, stretch=tk.NO)
        self.tree.column("3", width=700, minwidth=200, stretch=tk.NO)
        self.tree.heading("#0", text="대분류")
        self.tree.heading("1", text="중분류")
        self.tree.heading("2", text="소분류")
        self.tree.heading("3", text="설명")
        xscrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        xscrollbar.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=xscrollbar.set)
        yscrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        yscrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=yscrollbar.set)
        temp = open("D:/작업할 거/프로젝트/활엽수.csv", encoding='utf-8')
        rdr = csv.reader(temp)
        data3 = []
        for var in rdr:
            data3.append(var)
        for i, row in enumerate(data3):
            self.tree.insert(parent='', index='end', iid=i, text=row[0], values=((row[1],),(row[2],),(row[3],)))
        self.tree.pack()
    def func_radiobutton(self):
        global var
        if self.var.get()==1:
            self.func_searchname()
        elif self.var.get()==2:
            self.func_searcharch()
        elif self.var.get()==3:
            self.func_searchcode()
        elif self.var.get()==4:
            self.func_hw_code()
        elif self.var.get()==5:
            self.func_sw_code()
        elif self.var.get()==6:
            self.func_quit()
w = Tk()
w.title("수종 검색 프로그램 mk_5")
w.geometry("250x200+100+100")
a=gui_tree(w)
w.mainloop()