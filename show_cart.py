#!/usr/local/bin/python3

from cgitb import enable 
enable()

from os import environ
from cgi import FieldStorage, escape
from hashlib import sha256            # Secure Hash Algorithm is a cryptographic hash function designed by the United States National Security Agency and is a U.S. Federal Information Processing Standard 
from time import time
from shelve import open                # A “shelf” is a persistent, dictionary-like object. The difference with “dbm” databases is that the values (not the keys!) in a shelf can be essentially arbitrary Python objects
from http.cookies import SimpleCookie   
import pymysql as db

result = ''
empty=True
try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if not http_cookie_header:
        toy = sha256(repr(time()).encode()).hexdigest()
        cookie['toy'] = toy
    else:
        cookie.load(http_cookie_header)
        if 'toy' not in cookie:
            toy = sha256(repr(time()).encode()).hexdigest()
            cookie['toy'] = toy
        else:
            toy = cookie['toy'].value
            
    session_store = open('sess_' + toy, writeback=True)

    for id_num in session_store: # checking to see if need to show table
        if id_num != 'username' and id_num !='authenticated':
            if session_store.get(id_num)!=0:
                empty=False

    if not session_store.get('authenticated'):
        result = '<p id="larger"><a href="login.py">Please Log In to see a shopping basket !<a></p>'
    elif empty:
        result = '<p>No items in shopping cart. <em>Keep Shopping !</em></p>'
    else:
        connection = db.connect(# login here)
        cursor = connection.cursor(db.cursors.DictCursor)
        result = """<table border=1>
                    <tr><th colspan="4">Your Cart</th></tr>
                    <tr><th>Photo</th><th>Toy</th><th>Quantity</th><th>Remove from Cart</th></tr>"""
        for id_num in session_store:
            if id_num != 'username' and id_num !='authenticated':
                cursor.execute("SELECT toy_name, photo FROM toys WHERE id_num = %s", (id_num))
                row = cursor.fetchone()
                if session_store.get(id_num)!=0:
                    result += '<tr><td><img class="smImage" src="%s" alt='' border=1 ></img></td><td>%s</td><td>%s</td><td><a href="remove_from_cart.py?id_num=%s">Remove One</a></td></tr>' % (row['photo'],row['toy_name'], session_store.get(id_num),id_num)
        result += """</table>
<p><a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/checkout.py" id='larger' ><b>All done? - Check Out</b></a></p>
"""
        cursor.close()  
        connection.close()
 
    session_store.close()
    print(cookie)
except (db.Error, IOError):
    result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'
    
print('Content-Type: text/html')
print()

    
print("""
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>The Toy Basket: Used Toy Shop !</title>
		<link rel="shortcut icon" href="toys.png" type="image/png">
		<link rel="icon" href="toys.png" type="image/png">
		<link href="styles.css" rel="stylesheet">
		<script src="slideshow.js"></script>
		<meta name="viewport" content="initial-scale=1.0, width=device-width" />
    </head>
	<body>
		<nav>			
			    <ul>
				<li>
					<a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/index.html" >The Shop:</a>
				</li>
				<li>
					<a href="login.py">Login</a>
				</li>
				<li>
					<a href="register.py">Register!</a>
				</li>
				<li>
					<a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/show_cart.py" >Shopping Basket</a>
				</li>
				<li>
					<a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/boys.py" >Boys Toys</a>
				</li>
				<li>
					<a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/girls.py" >Girls Toys</a>
				</li>
				<li>
					<a href="logout.py">Logout</a>
				</li>
			</ul>
		</nav>
    	<header>
			<h1>
				Your Basket <br></br> The Toy Basket: Used Toy Shop
			</h1>

		</header>
		<aside>
			<img id="slideshow" src="ball.jpg" />
		</aside>
		<main>
		<section style="overflow-x:auto;">
		%s
		</section>
		</main>
		<footer>
			<p> 
				<small>
					&copy; Jeff Davis, Student, Department of Computer Science, University College Cork. All rights reserved.
				</small>
			</p> 
			<p>
				<small>
					Contact information: 116221322 at umail dot ucc dot ie
				</small>
			</p>
			<p>
				<small>
					<a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/disclaimer.html">Legal disclaimer</a>
				</small>
			</p> 
		</footer>
	</body>
</html>
""" % (result))
