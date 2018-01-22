from tkinter import *
import pymysql.cursors
import datetime
from admin import Admin
class Gui :
    def __init__(self):
        self.row = 6
        self.root = Tk()
        self.root.configure(background='white')
        self.now = datetime.datetime.now()
        self.centerWindow()
        self.guiMake()
        self.makeTables()
        self.root.mainloop()

    def login (self):
        self.row += 1
        self.username = self.e1.get()
        self.password = self.e2.get()
        if self.username.find(";") >= 0 or self.password.find(";") >= 0 or \
                self.username.find("drop") >= 0 or self.password.find("drop") >= 0:
            print("injection found")
            self.l11 = Label(text="injection found ;)", height=4, font=17, background='white').grid(row=self.row, column=0, sticky=W)
            return
        else:
            self.l11 = Label(text="                  ", height=4, font=17, background='white').grid(row=self.row, column=0,
                                                                                                   sticky=W)

        self.connection2 = pymysql.connect(host='localhost',
                                           user='root',
                                           password='Khalesuske76',
                                           db='onlineShopping',
                                           charset='utf8mb4',
                                           cursorclass=pymysql.cursors.DictCursor)
        try:
            with self.connection2.cursor() as cursor:
                # Read a single record
                sql = "SELECT `IDU` FROM `UserAccount` WHERE `IDU`=%s AND `password` = %s "
                cursor.execute(sql, (self.username, self.password))
                result = cursor.fetchone()
                try :
                    self.IDU= result['IDU']
                    print(self.IDU)
                    if self.IDU == 'admin' :
                        self.delete_root()
                        A = Admin(self.root)

                    # m = mainWindow.mainGui(self.username, self.password, self.access)

                except TypeError :
                    self.l11 = Label( text="wrong username and password !", height=4, font=17, background='white').grid(
                        row=self.row, column=0, sticky=W)

        finally:
            self.connection2.close()

    def login2(self):

        self.row += 1
        self.email = self.e3.get()
        if self.email.find(";") >= 0 or self.email.find("drop") >= 0:
            print("injection found")
            self.l11 = Label(text="injection found ;)", height=4, font=17, background='white').grid(row=self.row,
                                                                                                   column=0, sticky=W)
            return
        else:
            self.l11 = Label(text="                  ", height=4, font=17, background='white').grid(row=self.row,
                                                                                                   column=0,
                                                                                                   sticky=W)

        self.connection2 = pymysql.connect(host='localhost',
                                           user='root',
                                           password='Khalesuske76',
                                           db='onlineShopping',
                                           charset='utf8mb4',
                                           cursorclass=pymysql.cursors.DictCursor)
        try:
            with self.connection2.cursor() as cursor:
                # Read a single record
                sql = "SELECT `Email` FROM `Users` WHERE `Email`=%s "
                cursor.execute(sql, (self.email))
                result = cursor.fetchone()
                try:
                    self.Email = result['Email']
                    # TODO
                    # self.root.destroy()
                    # m = mainWindow.mainGui(self.username, self.password, self.access)
                    self.l11 = Label(text="                            ", height=4, font=17, background='white').grid(
                        row=self.row, column=0, sticky=W)

                except TypeError:
                    self.l11 = Label(text="wrong username and password !", height=4, font=17, background='white').grid(
                        row=self.row, column=0, sticky=W)

        finally:
            self.connection2.close()

    def login3(self):
        self.date = str(self.now.year) + "-" + str(self.now.month) + "-" + str(self.now.day)
        self.row += 1
        self.firstName = self.e4.get()
        self.lastName = self.e5.get()
        self.phone = self.e6.get()
        self.address = self.e7.get()
        self.username = self.e8.get()
        self.password = self.e9.get()
        self.Email = self.e10.get()
        if self.firstName == "" or self.lastName == "" or self.phone == "" or self.address == "" or self.username == ""\
                or self.password == "" or self.Email == "" :
            self.l11 = Label(text="please fill all of them", height=4, font=17, background='white').grid(row=self.row,
                                                                                                    column=0, sticky=W)
            return
        if self.firstName.find(";") >= 0 or self.firstName.lower().find("drop") >= 0 or self.firstName.lower().find("or") >= 0 or \
            self.lastName.find(";") >= 0 or self.lastName.lower().find("drop") >= 0 or self.lastName.lower().find("or") >= 0 or \
            self.phone.find(";") >= 0 or self.phone.lower().find("drop") >= 0 or self.phone.lower().find("or") >= 0 or \
            self.address.find(";") >= 0 or self.address.lower().find("drop") >= 0 or self.address.lower().find("or") >= 0 or \
            self.username.find(";") >= 0 or self.username.lower().find("drop") >= 0 or self.username.lower().find("or") >= 0 or \
            self.Email.find(";") >= 0 or self.Email.lower().find("drop") >= 0 or  self.Email.lower().find("or") >= 0 or\
            self.password.find(";") >= 0 or self.password.lower().find("drop") >= 0 or self.password.lower().find("or") >= 0:
            print("injection found")
            self.l11 = Label(text="injection found ;)", height=4, font=17, background='white').grid(row=self.row,
                                                                                                   column=0, sticky=W)
            return
        else:
            self.l11 = Label(text="                  ", height=4, font=17, background='white').grid(
                row=self.row, column=0, sticky=W)

        self.connection2 = pymysql.connect(host='localhost',
                                           user='root',
                                           password='Khalesuske76',
                                           db='onlineShopping',
                                           charset='utf8mb4',
                                           cursorclass=pymysql.cursors.DictCursor)
        try:
            with self.connection2.cursor() as cursor:
                sql = "insert into Users Values ('" + self.Email + "' , '" + self.firstName + "' , '" + self.lastName +  "' , 'account' )"
                cursor.execute(sql)
                result = cursor.fetchone()
                self.connection2.commit()

                sql = "insert into UserAccountPhone VALUES (%s , %s)"
                cursor.execute(sql, (self.phone , self.username))
                result = cursor.fetchone()
                self.connection2.commit()

                sql = "insert into UserAccountAddress VALUES (%s , %s)"
                cursor.execute(sql, (self.address, self.username))
                result = cursor.fetchone()
                self.connection2.commit()

                sql = "insert into UserAccount VALUES (%s , %s , 0 , %s , %s)"
                cursor.execute(sql, (self.username, self.Email , self.date, self.password))
                result = cursor.fetchone()
        finally:
            self.connection2.commit()
            self.connection2.close()

    def makeTables(self):
        path = "table.sql"
        f = open(path)
        text = f.readlines()
        counter = 0
        flag2 = False
        sql2 = ""
        for sql in text:
            if sql.find("CREATE") != -1 or sql.find("insert") != -1 or sql.find("drop") != -1 or\
                            sql.find("UPDATE") != -1 or sql.find("create") != -1 or sql.find("DELETE") != -1:
                if flag2:
                    sql3 = sql
                    sql = sql2
                    sql2 = sql3
                else:
                    flag2 = True
                    sql2 = sql
                    continue
            else:
                sql2 = sql2 + sql
                continue
            print("=========================")
            print(sql)
            print("=========================")
            self.connection = pymysql.connect(host='localhost',
                                              user='root',
                                              password='Khalesuske76',
                                              charset='utf8mb4',
                                              cursorclass=pymysql.cursors.DictCursor)
            if counter > 1:
                self.connection = pymysql.connect(host='localhost',
                                                  user='root',
                                                  password='Khalesuske76',
                                                  db='onlineShopping',
                                                  charset='utf8mb4',
                                                  cursorclass=pymysql.cursors.DictCursor)
            counter += 1
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    # print(sql)
            finally:
                self.connection.commit()
                self.connection.close()
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='Khalesuske76',
                                          db='onlineShopping',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql2)
                result = cursor.fetchone()
                print(sql2)
        except pymysql.err.InternalError as e:
            code, msg = e.args
            if code == 1644:
                print(msg)
        finally:
            self.connection.commit()
            self.connection.close()
        f.close()

    def centerWindow(self):

        self.root.withdraw()
        self.root.update_idletasks()  # Update "requested size" from geometry manager

        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2
        self.root.geometry("+%d+%d" % (x, y))
        self.root.deiconify()


    def guiMake(self):

        self.background_image = PhotoImage(file='Untitled Diagram (18).png')
        self.background_label = Label( image=self.background_image)
        self.background_label.grid(row=0, column=0, columnspan=6, rowspan=2, sticky=W+E+N+S )

        self.l1 = Label(text="username :" , height=2, font=17 , background='white')
        self.l1.grid(row = 3 , column = 0 , sticky = W)

        self.l2 = Label( text="password :" , height=2, font=17 , background='white')
        self.l2.grid(row = 4 , column = 0 , sticky = W)

        self.e1 = Entry( bd=2, width= 17, font=10)
        self.e1.grid(row = 3 , column = 1 , sticky = W)

        self.e2 = Entry( show="*" , bd=2, width= 17, font=10)
        self.e2.grid(row = 4 , column = 1, sticky = W)

        self.login_img = PhotoImage(file='Untitled Diagram (23).png' )
        self.b1 = Button(image = self.login_img, command = self.login )
        self.b1.grid(row = 5 , column = 1, sticky = W)

        self.l3 = Label(text="Email :", height=4, font=17, background='white')
        self.l3.grid(row=3, column=2, sticky=W)
        self.e3 = Entry(bd=3, width=17, font=10)
        self.e3.grid(row=3, column=3, sticky=W)

        self.login_img2 = PhotoImage(file='Untitled Diagram (23).png')
        self.b2 = Button(image=self.login_img2, command=self.login2)
        self.b2.grid(row=4, column=3, sticky=W)

        self.l4 = Label(text="First Name :", height=4, font=17, background='white')
        self.l4.grid(row=3, column=4, sticky=W)
        self.e4 = Entry(bd=3, width=17, font=10)
        self.e4.grid(row=3, column=5, sticky=W)

        self.l5 = Label(text="Last Name :", height=4, font=17, background='white')
        self.l5.grid(row=4, column=4, sticky=W)
        self.e5 = Entry(bd=3, width=17, font=10)
        self.e5.grid(row=4, column=5, sticky=W)

        self.l6 = Label(text="Phone :", height=4, font=17, background='white')
        self.l6.grid(row=5, column=4, sticky=W)
        self.e6 = Entry(bd=3, width=17, font=10)
        self.e6.grid(row=5, column=5, sticky=W)

        self.l7 = Label(text="Address :", height=4, font=17, background='white')
        self.l7.grid(row=6, column=4, sticky=W)
        self.e7 = Entry(bd=3, width=17, font=10)
        self.e7.grid(row=6, column=5, sticky=W)

        self.l8 = Label(text="Username :", height=4, font=17, background='white')
        self.l8.grid(row=7, column=4, sticky=W)
        self.e8 = Entry(bd=3, width=17, font=10)
        self.e8.grid(row=7, column=5, sticky=W)

        self.l9 = Label(text="Password :", height=4, font=17, background='white')
        self.l9.grid(row=8, column=4, sticky=W)
        self.e9 = Entry(show ="*" , bd=3, width=17, font=10)
        self.e9.grid(row=8, column=5, sticky=W)

        self.l10 = Label(text="Email :", height=4, font=17, background='white')
        self.l10.grid(row=9, column=4, sticky=W)
        self.e10 = Entry( bd=3, width=17, font=10)
        self.e10.grid(row=9, column=5, sticky=W)

        self.login_img3 = PhotoImage(file='Untitled Diagram (22).png')
        self.b3 = Button(image=self.login_img3, command=self.login3)
        self.b3.grid(row=10, column=5, sticky=W)

        self.l15 = Label(text=" ", height=1, font=17,  background='white')
        self.l15.grid(row=11, column=5, sticky=W)

    def delete_root (self):
        self.background_label.grid_forget()

        self.l1.grid_forget()
        self.l2.grid_forget()
        self.l3.grid_forget()
        self.l4.grid_forget()
        self.l5.grid_forget()
        self.l6.grid_forget()
        self.l7.grid_forget()
        self.l8.grid_forget()
        self.l9.grid_forget()
        self.l10.grid_forget()
        # self.l11.grid_forget()
        # self.l15.grid_forget()


        self.b1.grid_forget()
        self.b2.grid_forget()
        self.b3.grid_forget()

        self.e1.grid_forget()
        self.e2.grid_forget()
        self.e3.grid_forget()
        self.e4.grid_forget()
        self.e5.grid_forget()
        self.e6.grid_forget()
        self.e7.grid_forget()
        self.e8.grid_forget()
        self.e9.grid_forget()
        self.e10.grid_forget()

g = Gui()
