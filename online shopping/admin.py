from tkinter import *
import pymysql.cursors
import datetime
from tkinter.scrolledtext import ScrolledText
class Admin :

    def __init__(self , root):
        self.q = []
        self.now = datetime.datetime.now()
        # self.makeQueryList()
        self.root = root
        # self.root = Tk()
        self.root.configure(background='white')

        self.guiMake()
        self.root.mainloop()

    def queryList(self, number, name):
        self.date = str(self.now.year) + "-" + str(self.now.month) + "-" + str(self.now.day)

        if number == 1:
            return "select sum(cost) as totalCost, Products.kind as kind , count(IDB) as number " +\
                    "from (Products  join  Basket_Product using( IDP)) natural join Basket " +\
                    "where state='d'and Basket_Product.kind= 'add' " +\
                    "group by Products.kind ; "

        elif number == 2:
            return "SELECT  UfirstName,UlastName,uDATE " +\
                   "FROM UserAccount  natural join Users ;"

        elif number == 3:
            return "SELECT * " +\
                   "FROM ( Users join  UserAccount  using (email)) join Employee using (IDU) " +\
                   "where  companyName " + name + " ;"

        elif number == 4:
            return "SELECT numberIdentification,IDB,IDU as userID,Pdate as TimeOfPurchase,dest as destination,deliveryTime " +\
                   "FROM Deliver natural join  User_Basket  natural join UserAccount join Pay using (IDB) join Basket using (IDB) " +\
                   "where numberIdentification = " + name + " ;"

        elif number == 5:
            return "SELECT  *" +\
                   "FROM DeletedUsers natural join users ;"

        elif number == 6:
            return "SELECT  idp,avg(star) as stars " +\
                   "FROM  Sport natural join Comments " +\
                   "group by idp ;"

        elif number == 7:
            return "SELECT distinct  IDC  , CfirstName ,ClastName " +\
                   "FROM  Connector " +\
                   "where introducedate >= " + self.date + " ;"

        elif number == 8:
            return "SELECT  IDB as TrackingCode,Ptime as payTime ,Pdate as payDate,UfirstName as firstName ,UlastName as lastName  ,IDU as ID " +\
                   "FROM Pay  natural join Users natural  join UserAccount " +\
                   "where Pkind = 'etebar' ;"

        elif number == 9:
            return "SELECT * " +\
                   "FROM Conversation natural join  Supporter ;"

        elif number == 10:
            return "SELECT  IDP as productID,Pname as productName, discount,cost-discount*cost/100 as newCost,kind " +\
                   "FROm Products " +\
                   " where discount>0 ;"

        elif number == 11:
            return "SELECT  IDS , times " +\
                   "FROM  SupporterLog " +\
                   "where onlinestatus='o'; "

        elif number == 12:
            return "SELECT  sum(totalcost) " +\
                    "FROM Pay natural join Basket " +\
                    "where DATE_SUB(Pay.Pdate, INTERVAL -2 MONTH) < " + self.date + " ;"

        elif number == 13:
            return "select sum(Basket.totalCost)/0.3 " +\
                   "from Pay , Basket " +\
                   "where Pay.IDB = Basket.IDB and " +\
                   "DATE_SUB(Pay.Pdate, INTERVAL -1 MONTH) < " + self.date + " ;"

        elif number == 14:
            return "select IDU , sum(numbers) * 10 " +\
                   "from Prizes " +\
                   "group by IDU ;  "

        elif number == 15:
            return "select Users.UfirstName , Users.UlastName , Users.kind " +\
                   "from Users , Products , User_Basket , Basket , Pay , Basket_Product " +\
                   "where Pay.Email = Users.Email and Pay.IDB = User_Basket.IDB and " +\
                   "Pay.IDB = Basket.IDB and User_Basket.Email = Pay.Email and " +\
                   "Basket_Product.IDB = Pay.IDB and Basket_Product.IDP = " + name + " ; "

        elif number == 16:
            return "select IDP , Pname , numberExist " +\
                   "from Products " +\
                   "where kind = 'Home' ; "

        elif number == 17:
            return "select sum(Basket.totalCost) " +\
                   "from Users , Pay , Basket , Employee , UserAccount " +\
                   "where DATE_SUB(Pay.Pdate, INTERVAL -1 MONTH) <  " + self.date +\
                   " and Pay.IDB = Basket.IDB and Employee.IDU = UserAccount.IDU and UserAccount.Email = Users.Email and " +\
                   "Users.Email = Pay.Email ;"

        elif number == 18:
            return ["call avgStar (" + name + ",@stars);", "select @stars ; "]

        elif number == 19:
            return "select sum(totalcost) as totalcost " +\
                    "from Employee , UserAccount , Users ,User_Basket , Basket , Pay " +\
                    "where Employee.companyName = '" + name + "' and Employee.IDU = UserAccount.IDU and UserAccount.Email = Users.Email and " +\
                    "User_Basket.Email = Users.Email and User_Basket.IDB = Basket.IDB  and  Basket.IDB = Pay.IDB ; "
        elif number == 20:
            return "update UserAccount set IDU = '" + name[0] + "' where Email = '" + name[1] + "' ;"

        elif number == 21:
            return "select create_time " +\
                    "FROM INFORMATION_SCHEMA.TABLES " +\
                    "WHERE table_schema = 'onlineShopping' " +\
                    "AND table_name = '" + name + "' ;"

        elif number == 22:
            return "SELECT UPDATE_TIME " +\
                    "FROM   information_schema.tables " +\
                    "WHERE  TABLE_SCHEMA = 'onlineShopping' "\
                    "AND TABLE_NAME = '"+ name + "';"

        elif number == 23:
            return "select * " +\
                    "from changeIDU ;"

    def print_Query_Result (self , table):

        self.scrolltext.insert(INSERT, "\n\t")
        x = table[0]
        for i in x:
            s = i + "\t|\t"
            if i == x[len(x)-1]:
                s = i + "\n\t"
            self.scrolltext.insert(INSERT, s)
        for i in x:
            for w in i:
                self.scrolltext.insert(INSERT, "---")
        self.scrolltext.insert(INSERT, "\n\t")
        for row in table[1:]:
            for e in row:
                if not e == row[len(row) - 1]:
                    self.scrolltext.insert(INSERT, str(e) + "\t|\t")
                else:
                    self.scrolltext.insert(INSERT, str(e) + "\n\t")

        self.scrolltext.insert(INSERT, "\n\t")

    def runQuery (self):
        res = self.e20.get()
        r = res.split(" ")
        self.now = datetime.datetime.now()
        name = ""
        number = 0
        if len(r) == 0:
            return
        elif len(r) == 1:
            number = int(r[0])
        elif len(r) == 3:
            number = int(r[0])
            name = r[2]
        elif len(r) == 4:
            number = int(r[0])
            name = [r[2], r[3]]
        sql = self.queryList(number, name)
        print(sql)
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='Khalesuske76',
                                          db='onlineShopping',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)
        try:
            with self.connection.cursor() as cursor:
                if number == 18 :
                    cursor.execute(sql[0])
                    result = cursor.fetchone()
                    cursor.execute(sql[1])
                    result = cursor.fetchone()
                else:
                    cursor.execute(str(sql))
                    result = cursor.fetchone()
                table = []
                x = []
                if result is None:
                    self.scrolltext.clipboard_clear()
                    if number != 20 :
                        self.scrolltext.insert(INSERT, "\n Empty table")
                    else:
                        self.scrolltext.insert(INSERT, "\n Your User ID Changed :)")
                else:
                    for attribute in result.keys():
                        x.append(attribute)
                    table.append(x)
                    while result is not None:
                        x = []
                        for attribute in table[0]:
                            x.append(result.get(attribute))
                        table.append(x)
                        result = cursor.fetchone()
                    print(table)
                    self.print_Query_Result(table)
        except pymysql.err.InternalError as e:
            code, msg = e.args
            if code == 1644:
                self.scrolltext.clipboard_clear()
                self.scrolltext.insert(INSERT, "\n " + msg)
        finally:
            self.connection.commit()
            self.connection.close()

    def guiMake(self):
        self.l20 = Label(text="Hey Admin ;)", height=2, font=17, background='white' , fg = '#058194')
        self.l20.grid(row=0, column=0, sticky=W)

        self.l21 = Label(text="What Query do you want ? (number - condition)", height=2, font=17, background='white' ,fg = '#058194')
        self.l21.grid(row=1, column=0, sticky=W)

        self.l22 = Label(text="1) number & cost of each product kind", height=2, font=17, background='white' , fg = '#034752')
        self.l22.grid(row=2, column=0, sticky=W)

        self.l23 = Label(text="2) name of Registered Users with date", height=2, font=17, background='white' , fg = '#034752' )
        self.l23.grid(row=3, column=0, sticky=W)

        self.l24 = Label(text="3) informations of useres in specific company", height=2, font=17, background='white', fg = '#034752')
        self.l24.grid(row=4, column=0, sticky=W)

        self.l25 = Label(text="4) informations of Driver in last month", height=2, font=17, background='white', fg = '#034752')
        self.l25.grid(row=5, column=0, sticky=W)

        self.l26 = Label(text="5) list of deleted users", height=2, font=17, background='white', fg = '#034752')
        self.l26.grid(row=6, column=0, sticky=W)

        self.l27 = Label(text="6) rate of all sport products", height=2, font=17, background='white', fg = '#034752')
        self.l27.grid(row=7, column=0, sticky=W)

        self.l28 = Label(text="7) list of connectors in last month", height=2, font=17, background='white', fg = '#034752')
        self.l28.grid(row=8, column=0, sticky=W)

        self.l29 = Label(text="8) information of users that paid with credit cart", height=2, font=17, background='white', fg = '#034752')
        self.l29.grid(row=9, column=0, sticky=W)

        self.l36 = Label(text="9) information about all conversations and Supporters", height=2, font=17, background='white', fg = '#034752')
        self.l36.grid(row=10, column=0, sticky=W)

        self.l30 = Label(text="10) information about all discount and products", height=2, font=17, background='white', fg = '#034752')
        self.l30.grid(row=2, column=1, sticky=W)

        self.l31 = Label(text="11) all times of supporter that was online", height=2, font=17, background='white', fg = '#034752')
        self.l31.grid(row=3, column=1, sticky=W)

        self.l32 = Label(text="12) income of shop in 2 last month", height=2, font=17, background='white', fg = '#034752')
        self.l32.grid(row=4, column=1, sticky=W)

        self.l33 = Label(text="13) sum of tax that users paid", height=2, font=17, background='white', fg = '#034752')
        self.l33.grid(row=5, column=1, sticky=W)

        self.l34 = Label(text="14) information about prizes", height=2, font=17, background='white', fg = '#034752')
        self.l34.grid(row=6, column=1, sticky=W)

        self.l35 = Label(text="15) informations about users that bought specific product", height=2, font=17, background='white', fg = '#034752')
        self.l35.grid(row=7, column=1, sticky=W)

        self.l36 = Label(text="16) informations about Home products", height=2, font=17, background='white', fg = '#034752')
        self.l36.grid(row=8, column=1, sticky=W)

        self.l37 = Label(text="17) sum of all products that users of companys bought", height=2, font=17, background='white', fg = '#034752')
        self.l37.grid(row=9, column=1, sticky=W)

        self.l38 = Label(text="18) get the average star of a product", height=2, font=17,
                         background='white', fg='#034752')
        self.l38.grid(row=10, column=1, sticky=W)

        self.l39 = Label(text="19) get the sum of all Employees cost in one company", height=2, font=17,
                         background='white', fg='#034752')
        self.l39.grid(row=2, column=2, sticky=W)

        self.l40 = Label(text="20) change the user ID (new ID & Email)", height=2, font=17,
                         background='white', fg='#034752')
        self.l40.grid(row=3, column=2, sticky=W)

        self.l41 = Label(text="21) Get the time of Creation all Tables", height=2, font=17,
                         background='white', fg='#034752')
        self.l41.grid(row=4, column=2, sticky=W)

        self.l42 = Label(text="22) get last time tables updated", height=2, font=17,
                         background='white', fg='#034752')
        self.l42.grid(row=5, column=2, sticky=W)

        self.l43 = Label(text="23) log of user ID changed", height=2, font=17,
                         background='white', fg='#034752')
        self.l43.grid(row=6, column=2, sticky=W)


        self.e20 = Entry(bd=3, width=17, font=10)
        self.e20.grid(row= 1, column=1, sticky=W)

        self.login_img3 = PhotoImage(file='Untitled Diagram (19).png')
        self.b3 = Button(image=self.login_img3, command=self.runQuery)
        self.b3.grid(row=1, column=1, sticky=E)

        self.scrolltext = ScrolledText(font=10, width=140, height=20)
        self.scrolltext.grid(row=11, column=0,columnspan=4, rowspan=3 , sticky=W)

# r = ""
# a = Admin(r)

