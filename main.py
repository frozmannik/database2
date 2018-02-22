import mysql.connector
from mysql.connector import cursor
from mysql.connector.constants import ClientFlag
import datetime
import os



client_cert = os.path.abspath(os.path.join('keys', 'client-cert.pem'))
client_key = os.path.abspath(os.path.join('keys', 'client-key.pem'))
server_ca = os.path.abspath(os.path.join('keys', 'server-ca.pem'))
db = mysql.connector.connect(user='root', password='12123434Qq',  # database connection (dont touch this line)
                              host='35.198.97.12',
                              database='test',
                              client_flags =[ClientFlag.SSL],
                              ssl_ca=server_ca,
                              ssl_cert = client_cert,
                              ssl_key = client_key
                             )

cursor = db.cursor() #cursor to work with db

# manually add item
def add_item(name,description,categoryID,itemPrice,URL):  # string,string,int,float
    try:
        sqlstmt = "INSERT INTO items (`itemName`, `itemDescription`, `categoryID`, `itemPrice`, `OutOFStock`) VALUES ('" + str(name)+"', '" + str(description) + "', '" + str(categoryID) + "', '" +str(itemPrice) + "', '0');"
        cursor.execute(sqlstmt)
        print "Item added successfully"

    except mysql.connector.Error as err :
        print"Something went wrong: {}".format(err)
        print "Item wasn't added"


def del_item(id):  # delete items hopefully we wont use it
    try:
        sqlstmt = "DELETE FROM `test`.`items` WHERE `itemID`='{}';".format(id)
        cursor.execute(sqlstmt)
        db.commit()
        print "Item removed successfully"

    except mysql.connector.Error as err :
        print "Something went wrong: {}".format(err)
        print "Item wasn't removed"


def show_items():  # just tool to see items (no idea why would like to use it but let it be here )
    sqlstmt = "SELECT * FROM items"  # mysql statment to execute
    cursor.execute(sqlstmt)  # execution of statement
    result = cursor.fetchall()  # fetch result of executing
    for x in result:  # just for printing result
        print "id: " + str(x[0])
        print "itemName: " + str(x[1])
        print "idemDesription : " + str(x[2])
        print "categoryID : " + str(x[3])
        print "itemPrice : " + str(x[4])
        print "URL : " + str(x[5])
        print  "new value ####################"

def out_of_stock(id): # set item out of stock
    try:
        sqlstmt = "UPDATE `test`.`items` SET `outOfStock` = '1' WHERE `itemID` = '{}';".format(id)
        print sqlstmt
        cursor.execute(sqlstmt)
        db.commit()
        print "Item was set as out of stock"

    except mysql.connector.Error as err:
        print "Something went wrong: {}".format(err)
        print "Can not put item out of stock"

def release_item(id):  # set item out of stock
    try:
        sqlstmt = "UPDATE `test`.`items` SET `outOfStock` = '0' WHERE `itemID` = '{}';".format(id)
        cursor.execute(sqlstmt)
        db.commit()
        print "Item was set as available"

    except mysql.connector.Error as err:
        print "Something went wrong: {}".format(err)
        print "Can not release item"


def make_an_order(basket,orderID): #orderID could be replaced by some internal counter( THEN we will use this counter as
    try:
        price = 0
        for item in basket:
            sqlstmt = "SELECT `itemPrice` FROM `items` WHERE `itemID` = {} ".format(item)
            cursor.execute(sqlstmt)
            result = cursor.fetchall()
            price = price +(result[0][0])
        print "final price is {}".format(price)
        print "current time is {}".format(datetime.datetime.now())

        # create an order in `order` table
        time = datetime.datetime.now()
        sqlstmt = " INSERT INTO `test`.`orders` (`orderTime`, `orderPrice`) VALUES ('{}', '{}');".format(time,price)
        cursor.execute(sqlstmt)
        db.commit()

        sqlstmt = "SELECT MAX(`orderID`) FROM `orders`;"
        cursor.execute(sqlstmt)
        result = cursor.fetchall()
        print result[0][0]
        # get a result[0][0] as order id and put it in `utility table` with itemID

        for item in basket:
            sqlstmt ="INSERT INTO `test`.`utility_table` (`itemID`, `orderID`) VALUES ('{}', '{}');".format(item,result[0][0])
            cursor.execute(sqlstmt)
            db.commit()

    except mysql.connector.Error as err:
        print "Something went wrong: {}".format(err)
    except IndexError as err1:
        print "Something went wrong: {}".format(err1)
        print "Item doesn't exist"




basket = [1,2,3,100]

make_an_order(basket,21)



#add_item('TESTTEST','TESTTTTTTTTT','99','12', 'URL')
#add_item('test2','test2','99','12', 'URL')
#del_item(21)
#show_items()



db.close()  # close your connection to db (DONT TOUCH THIS LINE)