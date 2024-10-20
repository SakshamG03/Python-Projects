import mysql.connector

db1 = None

def connect():
    global db1
    db1 = mysql.connector.connect(host="localhost",user="root",password="password")

connect()
c1=db1.cursor
c1.execute("create database shopping")
c1.execute("use shopping")
c1.execute("CREATE TABLE products (product_id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(100) NOT NULL,category VARCHAR(50),price DECIMAL(10, 2) NOT NULL,stock_quantity INT NOT NULL);")
c1.execute("CREATE TABLE customers (customer_id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(100) NOT NULL,email VARCHAR(100) NOT NULL);")
c1.execute("CREATE TABLE orders (order_id INT AUTO_INCREMENT PRIMARY KEY,customer_id INT NOT NULL,total_amount DECIMAL(10, 2) NOT NULL,order_date DATETIME DEFAULT NOW(),FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE);")
c1.execute("CREATE TABLE order_items (order_item_id INT AUTO_INCREMENT PRIMARY KEY,order_id INT NOT NULL,product_id INT NOT NULL,quantity INT NOT NULL,price DECIMAL(10, 2) NOT NULL,FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE);")
c1.execute("CREATE TABLE admin_users (admin_id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(50) NOT NULL,password VARCHAR(100) NOT NULL);")
c1.execute("INSERT INTO `shopping`.`admin_users` (`admin_id`, `username`, 'password') VALUES ('1', 'Rajat', '12');")