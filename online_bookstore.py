import uuid
from datetime import datetime

class Book:
    def __init__(self,isbn,title,author,subject,price,stock):
        self.isbn=isbn
        self.title=title
        self.author=author
        self.subject=subject
        self.price=price
        self.stock=stock
    

    def is_available(self,quantity):
        return self.stock>0
    
    def reduce_stock(self,quatity=1):
        if self.stock>=quatity:
            self.stock-=quatity
            return True
        return False
    
    def restock(self,quatity):
        self.stock+=quatity

class Patron:
    def __init__(self,patron_id,name,email):
        self.patron_id=patron_id
        self.name=name
        self.email=email
        self.orders=[]

    def add_order(self,order):
        self.orders.append(order)
    
    def view_order(self):
        for order in self.orders:
            print(f"Order ID {order.order_id}, Status : {order.status},Total: {order.calculate_total()} type {order} time {order.order_time} patron {order.patron.patron_id} itmes {order.items[0]}")


class Order:
    def __init__(self,patron):
        self.order_id=str(uuid.uuid4())
        self.patron=patron
        self.items=[]
        self.status="Pending"
        self.order_time=datetime.now()
    
    def add_book(self,book,quantity=1):
        if book.is_available(quantity) and book.reduce_stock(quantity):
            self.items.append((book,quantity))
        else:
            print(f"book {book.titlt} is out of stock")
    
    def calculate_total(self):
        return sum(book.price * quantity for book, quantity in self.items)
    
    def complete_order(self):
        self.status="Completed"
    
    def view_order(self):
        for book,quantity in self.items:
            print(f"{book.title} (x{quantity} - ${book.price * quantity})")
        print(f"total price: ${self.calculate_total()}")

class Bookstore:
    def __init__(self):
        self.books_by_isbn={}
        self.books_by_title={}
        self.books_by_author={}
        self.books_by_subject={}
        self.patrons={}
    
    def add_book(self,book):
        self.books_by_isbn[book.isbn]=book
        if book.title not in self.books_by_title:
            self.books_by_title[book.title]=[]
        self.books_by_title[book.title].append(book)

        if book.author not in self.books_by_author:
            self.books_by_author[book.author]=[]
        self.books_by_author[book.author].append(book)

        if book.subject not in self.books_by_subject:
            self.books_by_subject[book.subject]=[]
        self.books_by_subject[book.subject].append(book)    

    def search_by_title(self,title):
        return self.books_by_title.get(title,[])


    def search_by_author(self,author):
        return self.books_by_author.get(author,[])
    
    def search_by_subject(self,subject):
        return self.books_by_subject.get(subject,[])
    

    def add_patron(self,patron):
        self.patrons[patron.patron_id]=patron


    def get_patron(self,patron_id):
        return self.patron.get(patron_id,None)



bookstore=Bookstore()

book1=Book("1234","Book One","Author One","Suspense",10.99,5)
book2=Book("5678","Book Two","Author Two","Romance",15.50,3)


bookstore.add_book(book1)
bookstore.add_book(book2)

patron1=Patron("P001","Komal","komal@gmail.com")
patron2=Patron("P002","sonal","sonal@gmail.com")

bookstore.add_patron(patron1)
bookstore.add_patron(patron2)

found_books=bookstore.search_by_title("Book One")
for book in found_books:
    print(f"found book {book.title} by author {book.author}")


order=Order(patron1)
order.add_book(book1,2)
order.add_book(book2,1)

order.complete_order()

patron1.add_order(order)

patron1.view_order()

order.view_order()