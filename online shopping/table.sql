drop database if exists onlineShopping;
create database onlineShopping;
drop table if exists Employee;
drop table if exists UserAccount;
drop table if exists Users;
drop table if exists Basket;
drop table if exists Supporter;
drop table if exists Supporterlog;
drop table if exists Company;
drop table if exists Connector;
drop table if exists Driver;
drop table if exists DriverLog;
drop table if exists Products;
drop table if exists Home;
drop table if exists UserAccountPhone;
drop table if exists UserAccountAddress;
drop table if exists DeletedUsers;
drop table if exists User_Basket;
drop table if exists CompanyPhone;
drop table if exists CompanyAdress;
drop table if exists ConnectorPhone;
drop table if exists DriverAdress;
drop table if exists DriverPhone;
drop table if exists Prizes;
drop table if exists Specify;
drop table if exists Deliver;
drop table if exists Pay;
drop table if exists Conversation;
drop table if exists Comments;
drop table if exists Confirm;
drop table if exists Basket_Product;
drop table if exists Sport;
drop table if exists DeletedCompany;
drop procedure if exists hesab;
drop procedure if exists avgStar;
create table Employee(IDU varchar(30) references UserAccount on update cascade,companyName text references Company,Pnumber int,Confirmation VARCHAR (10),CHECK (Confirmation in (’yes’, ’no’)) , PRIMARY KEY (IDU));
create table UserAccount(IDU varchar(30) primary key,Email text references Users,credit int DEFAULT 0 , uDATE date , password text );
create table UserAccountPhone(UPhonenumber numeric (11,0),IDU varchar(30) references UserAccount on update cascade,PRIMARY KEY (UPhonenumber, IDU)  );
create table UserAccountAddress(UAddress varchar(100),IDU varchar(30) references UserAccount on update cascade ,PRIMARY KEY (UAddress, IDU) );
create table Users(Email varchar(30) primary key , UfirstName text,UlastName text , kind varchar (10) , check (kind in (’guest’, ’account’)));
create table DeletedUsers(IDU varchar(30) primary key ,Email varchar(30) not null references Users);
create table Basket_Product(IDB int, IDP int, timeAD timestamp , kind VARCHAR (10), PRIMARY KEY (IDB , IDP,timeAD), CHECK (kind in(’add’, ’delete’)));
create table Basket(IDB int primary key ,state char ,deliveryTime timestamp , totalCost int DEFAULT 0);
create table User_Basket(IDB int references Basket , Email varchar(30) references Users  on delete no action ,PRIMARY KEY (IDB, Email));
create table Supporter(IDS int primary key , SfirstName text ,SlastName text,onlinestatus char);
create table SupporterLog(IDS int ,onlinestatus char,times TIMESTAMP DEFAULT NOW(),PRIMARY KEY (IDs,times));
create table Company(coRegisterationNumber int primary key , companyName text);
create table CompanyPhone(cPhonenumber numeric (11,0),coRegisterationNumber  int references Company on delete cascade ,PRIMARY KEY (cPhonenumber,coRegisterationNumber ));
create table CompanyAdress(cAddress varchar(100),coRegisterationNumber int references Company on delete cascade,PRIMARY KEY (cAddress,coRegisterationNumber ));
create table Connector(IDC int primary key , CfirstName text ,ClastName text ,introducedate timestamp );
create table ConnectorPhone(CPhonenumber numeric (11,0),IDC int references Connector on delete cascade ,PRIMARY KEY (CPhonenumber, IDC)  );
create table Driver(numberIdentification int primary key , DfirstName text ,DlastName text, plaque varchar(11) ,machine varchar(11) ,Dstate varchar(10) , CHECK (Dstate in (’ready’, ’notReady’)));
create table DriverLog(numberIdentification int ,plaque varchar(11) ,machine varchar(11) ,Dstate varchar(10),times TIMESTAMP DEFAULT NOW() ,PRIMARY KEY (numberIdentification  ,plaque ,machine,Dstate,times ));
create table DriverPhone(DPhonenumber numeric (11,0),numberIdentification  int references Driver  ,PRIMARY KEY (DPhonenumber,numberIdentification ));
create table DriverAdress(DAddress varchar(100),numberIdentification int references Driver ,PRIMARY KEY (DAddress,numberIdentification ));
create table Products(IDP int PRIMARY KEY  ,Pname text ,producer text,cost int ,discount int,numberExist int,kind varchar (10), check (kind in (’Sports’, ’Home’, ’Digital’)));
create table Home(IDP int PRIMARY KEY , Dates date);
create table Sport(IDP int PRIMARY KEY , color text);
create table Confirm( IDU varchar(30) references Employee on update cascade  ,IDC int references Connector on delete cascade,PRIMARY KEY (IDC,IDU));
create table Comments(IDU varchar(30) references UserAccount on update cascade  ,IDP int references Products on delete no action,commText text , star int,commtime timestamp,PRIMARY KEY (IDP,IDU,commtime));
create table Conversation(Email varchar(30)  references Users on delete cascade ,IDS int references Supporter on delete cascade  ,Convtime timestamp , title text,PRIMARY KEY (Email,IDs,convtime) ,check (title in (’shekayat’, ’dirKard’, ’pasokhgooi’,’darkhastHazine’)));
create table Pay(IDB int  references Basket on delete restrict,Email varchar(30)  references Users,dest text,Ptime time,Pdate date,Pkind text,PRIMARY KEY (IDB,Email),check (Pkind in ('etebar', 'internety', 'sherkat')));
create table Deliver(numberIdentification int  references Driver on delete no action, IDB int  references Basket,PRIMARY KEY (IDB,numberIdentification));
create table Specify(IDC int references Connector,coRegisterationNumber int references Company,PRIMARY KEY (IDC,coRegisterationNumber) );
create table Prizes ( IDU varchar(30) REFERENCES UserAccount on update cascade,time timestamp,primary key(IDU,time) );
create table DeletedCompany(coRegisterationNumber int primary key , companyName text);
CREATE TRIGGER deletedAccounts After delete ON UserAccount
       FOR EACH ROW
   INSERT INTO  DeletedUsers(IDU  , email)
   VALUES
   ( old.IDU ,old.email);
CREATE TRIGGER up_support After UPDATE ON Supporter
       FOR EACH ROW
   INSERT INTO  SupporterLog(IDS ,onlinestatus,times)
   VALUES
   ( new.IDS,new.onlinestatus,SYSDate());
CREATE TRIGGER up_driver After UPDATE ON Driver
       FOR EACH ROW
   INSERT INTO  DriverLog(numberIdentification ,plaque,machine,Dstate,times )
   VALUES
   ( new.numberIdentification ,new.plaque,new.machine,new.Dstate,SYSDate());
CREATE PROCEDURE hesab( IN IDBs INT )
BEGIN
DECLARE total INT DEFAULT 0 ;
DECLARE deletedItems INT DEFAULT 0 ;
SELECT sum(cost) into total
FROM  Products  join Basket_Product using (IDP)
WHERE  IDB=IDBs and Basket_Product.kind='add' ;
SELECT sum(cost) into deletedItems
FROM  Products  join Basket_Product using (IDP)
WHERE  IDB=IDBs and Basket_Product.kind='delete' ;
update Basket SET totalCost=(total-deletedItems)*(1.09) WHERE  IDB=IDBs;
END ;
CREATE TRIGGER delcompany After delete on Company
       FOR EACH ROW
   INSERT INTO  DeletedCompany(coRegisterationNumber, companyName )
   VALUES
   ( old.coRegisterationNumber,old.companyName);
CREATE TRIGGER CostPlusMaliat After insert ON Basket_Product
       FOR EACH ROW
		call hesab(new.IDB);
CREATE TRIGGER incCredit BEFORE UPDATE ON UserAccount
     FOR EACH ROW
     BEGIN
         IF NEW.credit>1000 THEN
            SET NEW.credit = old.credit+new.credit+10;
            INSERT INTO Prizes ( IDU ,time)
   VALUES
   ( new.IDU,SYSDate());
        ELSEIF NEW.credit < 1000 THEN
             SET NEW.credit =  old.credit+new.credit;
         END IF;
END;
CREATE PROCEDURE payEmployee (IN  IDBA int , IN mail varchar(30))
BEGIN
DECLARE emp INT DEFAULT 0 ;
  SELECT COUNT(*) into emp
  FROM Employee , UserAccount
  WHERE Employee.IDU = UserAccount.IDU and UserAccount.Email = mail ;
  update Basket SET totalCost =( totalCost * 0.9 )  WHERE  IDB=IDBA and totalCost <= 500 and emp >= 1;
  update Basket SET totalCost =(totalCost - 50 ) WHERE  IDB=IDBA and totalCost > 500 and emp >= 1;
END;
CREATE TRIGGER empdiscount BEFORE insert on Pay
  FOR EACH ROW
  call payEmployee(new.IDB , new.Email)
UPDATE UserAccount SET credit =1001
WHERE IDu='samii';
CREATE PROCEDURE avgStar( in IDps int , out  stars int )
BEGIN
 SELECT sum(star)/count(distinct IDU) into stars
 FROM  Comments
 WHERE  IDp=IDps ;
END ;
 CREATE TRIGGER numberExists BEFORE insert ON Basket_Product
     FOR EACH ROW
     BEGIN
         IF NEW.kind='add' THEN
   update Products set numberExist=numberExist-1 where IDP=new.IDP;
        ELSEIF NEW.kind='delete' THEN
   update Products set numberExist=numberExist+1 where IDP=new.IDP;
         END IF;
END;
insert into Users VALUES ('shahrzad@gmail.com' , 'shahrzad', 'shirazi', 'account');
insert into Users VALUES ('sara@gmail.com' , 'sara', 'shirazi', 'account');
insert into Users VALUES ('sarass@gmail.com' , 'saras', 'shirazi', 'account');
insert into Users VALUES ('s@gmail.com' , 's', 'shirazi', 'account');
insert into UserAccount VALUES ('shahrzad' , 'shahrzad@gmail.com' , 0 , '2017-12-23' , '1234');
insert into UserAccount VALUES ('sara' , 'sara@gmail.com' , 0 , '2017-12-23' , '1234');
insert into UserAccount VALUES ('sarass' , 'sarass@gmail.com' , 0 , '2017-12-23' , '1234');
insert into Employee VALUES ('shahrzad' , 'asanpardakht', 1 , 'yes');
insert into Employee VALUES ('sara' , 'asanpardakht', 1 , 'yes');
insert into Employee VALUES ('sarass' , 'asanpardakhtss', 1 , 'yes');
insert into Employee VALUES ('s' , 'golrang', 1 , 'yes');
insert into Employee VALUES ('saras' , 'golrang', 1 , 'yes');
insert into DeletedUsers VALUES ('monireh' , 'monireh@gmail.com' );
insert into Users VALUES ('mahtab.farrokh@gmail.com', 'mahtab' , 'farrokh' , 'account');
insert into UserAccount VALUES ('admin'  ,'mahtab.farrokh@gmail.com' , 1000000 ,'2017-12-23', '1234' );
insert into UserAccountPhone VALUES (999999999 , 'admin');
insert into UserAccountAddress VALUES ('enghelab' , 'admin');
insert into Products VALUES (1 ,'pen' , 'panter', 1000 , 0 , 100 , 'Digital');
insert into Products VALUES (2 ,'bag' , 'xxx', 50000 , 0 , 10 , 'Sports');
insert into Products VALUES (3 ,'desk' , 'yyy', 44000 , 10 , 10 , 'home');
insert into Sport VALUES (2, 'blue');
insert into Driver VALUES (11111111, 'ali', 'gholi', '12345', 'neysan', 'ready');
insert into DriverPhone VALUES (88888888 , 11111111 );
insert into DriverPhone VALUES (55555555 , 11111111 );
insert into DriverAdress VALUES ('azadi..' , 11111111);
insert into DriverAdress VALUES ('mirdamad..' , 11111111);
insert into User_Basket VALUES(999,'shahrzad@gmail.com');
insert into Deliver VALUES( 1277, 12334);
insert into Comments value( 'shahrzad' ,3,'' , 3,'2038-01-19 03:14:27');
insert into Comments value( 'monireh' ,3,'' , 5,'2038-01-19 03:14:43');
insert into Sport value(3,'red');
insert into Pay value(12334,'shahrzad@gmail.com','meidal salehi','03:14:43','2038-01-19 ','etebar');
insert into Conversation value ('shahrzad@gmail.com',1,'2038-01-19 03:14:43','shekayet');
insert into Conversation value ('sarass@gmail.com',1,'2038-01-19 03:14:43','shekayet');
insert into Supporter value (1,'ali','ailyar','o');
insert into Conversation value ('sarass@gmail.com',1,'2038-01-19 03:17:43','dirKard');
insert into  Connector value(333 , 'reza' ,'rezapoor','2013-01-19 03:17:43' );
insert into  Connector value(331, 'razi' ,'rezapoor','2014-01-19 04:17:43' );
insert into  Connector value(322, 'vahid' ,'rezaii','2034-01-19 04:17:43' );
insert into Pay value(3,'mahtab.farrokh@gmail.com','hafez','07:17:43','2055-05-19','etebar');
insert into Pay value(4,'shahrzad.com','hafez','06:17:43','2054-05-19','etebar');
insert into Pay value(10,'shahrzad.com','hafez','06:17:43','2004-05-19','etebar');
insert into Pay value(6,'shahrzadsd.com','hafezs','06:17:43','2014-05-19','etebar');
insert into  Basket value (3,'d' ,'2013-06-19 04:17:43' , 4400);
insert into  Basket value (4,'d' ,'2027-06-13 04:17:42' , 4430);
insert into  Basket value (6,'d' ,'2016-06-12 04:17:42' , 1400);
insert into  Basket value (10,'d' ,'2008-06-12 04:17:42' , 100);
insert into  Basket value (33,'d' ,'2008-06-12 04:17:42' , 100);
insert into  Basket value (32,'d' ,'2008-06-12 04:17:42' , 100);
insert into  Basket value (8,'d' ,'2008-06-12 04:17:42' , 100);
insert into User_Basket value(33,'samii@gmail.com' );
insert into User_Basket value(32,'s@gmail.com' );
insert into User_Basket value(3,'mahtab.farrokh@gmail.com' );
insert into User_Basket value(10,'shahrzad.com' );
insert into User_Basket value(6,'shahrzad.sdcom' );
insert into User_Basket value(4,'shahrzad.com' );
insert into User_Basket value(8,'shahrzad@gmail.com' );
insert into  Deliver value(133, 10);
insert into  Deliver value(133, 3);
insert into  Deliver value(14, 6);
insert into UserAccount VALUES ('sam' , 'sam@gmail.com' , 0 , '2013-12-23' , '1234');
insert into Pay value(333,'sam@gmail.com','hafezs','06:17:43','2014-05-19','etebar');
insert into Pay value(8,'shahrzad@gmail.com','hafezs','06:17:43','2014-05-19','etebar');
insert into  Basket value (333,'d' ,'2008-06-12 04:17:42' , 100);
insert into User_Basket value(333,'sam@gmail.com');
insert into  Deliver value(133, 333);
insert into  Basket value (331,'d' ,'2022-06-12 04:17:42' , 100);
insert into User_Basket value(331,'sam@gmail.com');
insert into  Deliver value(123, 331);
insert into UserAccount VALUES ('samii' , 'samii@gmail.com' , 0 , '2017-12-23' , '1234');
insert into Pay value(338,'samii@gmail.com','hafezs','06:17:43','2018-05-19','etebar');
insert into Pay value(445,'samii@gmail.com','hafezs','04:17:43','2018-05-19','sherkat');
insert into Pay value(431,'s@gmail.com','hafezs','05:17:43','2018-05-12','sherkat');
insert into Basket value (338,'d' ,'2013-06-12 04:17:42' , 100);
insert into User_Basket value(338,'sam@gmail.com');
insert into Deliver value(123, 338);
insert into Company value (5555566 ,'golrang');
insert into Basket value (10009,'d' ,'2013-06-12 04:17:42' , 0);
insert into Basket_Product value (10009,1,'2013-06-12 04:17:42', 'add');
insert into Basket_Product value (10009,2,'2013-06-12 04:17:44', 'add');
insert into Basket_Product value (33,2,'2013-06-12 04:17:44', 'add');
insert into Basket_Product value (33,2,'2013-06-12 04:17:55', 'delete');
UPDATE Supporter  SET onlinestatus ='v'
WHERE ids=1;
DELETE FROM useraccount WHERE IDU='sam';