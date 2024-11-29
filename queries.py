# pylint:disable=C0111,C0103

import sqlite3

conn = sqlite3.connect('data/ecommerce.sqlite')
a = conn.cursor()

def detailed_orders(db):
    '''return a list of all orders (order_id, customer.contact_name,
    employee.firstname) ordered by order_id'''
    query = """SELECT OrderID, c.ContactName, e.FirstName
    FROM Orders o
    JOIN Employees e ON e.EmployeeID = o.EmployeeID
    JOIN Customers c ON c.CustomerID = o.CustomerID
    ORDER BY OrderID
    """
    db.execute(query)
    detailed_orders_list = db.fetchall()
    return detailed_orders_list

def spent_per_customer(db):
    '''return the total amount spent per customer ordered by ascending total
    amount (to 2 decimal places)
    Exemple :
        Jean   |   100
        Marc   |   110
        Simon  |   432
        ...
    '''
    query = """
    SELECT ContactName cn , SUM(UnitPrice * Quantity) sum
    FROM Customers c
    JOIN Orders o ON o.CustomerID = c.CustomerID
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    GROUP BY cn
    ORDER BY ROUND(sum, 2)
    """
    db.execute(query)
    spent_per_customer_list = db.fetchall()
    return spent_per_customer_list

def best_employee(db):
    query = """SELECT FirstName, LastName, SUM(UnitPrice * Quantity) sum
    FROM Employees e
    JOIN Orders o ON o.EmployeeID = e.EmployeeID
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    GROUP BY e.EmployeeID
    ORDER BY sum DESC
    """
    db.execute(query)
    best_employee_list = db.fetchone()
    return best_employee_list


def orders_per_customer(db):
    '''Return a list of tuples where each tuple contains the contactName
    of the customer and the number of orders they made (contactName,
    number_of_orders). Order the list by ascending number of orders'''
    query = """SELECT ContactName cn, COUNT(OrderID) count
    FROM Customers c
    LEFT JOIN Orders o ON o.CustomerID = c.CustomerID
    GROUP BY cn
    ORDER BY count
    """
    db.execute(query)
    orders_per_customer_list = db.fetchall()
    return orders_per_customer_list
