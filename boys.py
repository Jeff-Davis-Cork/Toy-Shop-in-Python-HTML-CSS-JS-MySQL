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

#form_data = FieldStorage()
#username=''
#password=''

result = """
   <p>You do not have permission to access this page.</p>
   <ul>
       <li><a href="register.py">Register</a></li>
       <li><a href="login.py">Login</a></li>
   </ul>"""

print('Content-Type: text/html')
print()


result2 = "<p>If you would like to shop, Login!</p>"
   
try:
    cookie = SimpleCookie()
    http_cookie_header = environ.get('HTTP_COOKIE')
    if http_cookie_header:
        cookie.load(http_cookie_header)
        if 'toy' in cookie:
            sid = cookie['toy'].value
            session_store = open('sess_' + sid, writeback=False)
            if session_store.get('authenticated'):
                result2 = """
                    <p>
                        <b>Welcome Back, %s. Enjoy Shopping!</b>
                    </p>""" % session_store.get('username')
            session_store.close()
except IOError:
    result2 = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

try:
    connection = db.connect(# put login here)
    cursor = connection.cursor(db.cursors.DictCursor)
    cursor.execute("SELECT photo,toy_name,price,age_min,stock,id_num FROM toys WHERE toy_cat='Boys' ORDER BY id_num")
    result = """<table border='1'>
                <tr><th colspan="6">Boys Toys</th></tr>
                <tr><th>Picture</th><th>Toy Name</th><th>Buy It!</th><th>Price</th><th>Ages</th><th>Stock Available</th></tr>"""
    for row in cursor.fetchall():
        result += """<tr>
                        <td><img src="%s" alt='' border=1 ></img></td>
                        <td>%s</td>
                        <td><a href="add_to_cart.py?id_num=%s">Buy It!</a></td>
                        <td>&#8364<span>%.2f</span></td>
                        <td>%s</td>
                        
                        <td>%s</td>
                        
                    </tr>""" % (row['photo'],row['toy_name'], row['id_num'],row['price'], row['age_min'], row['stock'])
    result += '</table>'
    cursor.close()  
    connection.close()
except db.Error:
    result = '<p>DBDBSorry! We are experiencing problems at the moment. Please call back later.</p>'

    
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
				Boys Toys Page: <br></br> The Toy Basket: Used Toy Shop
			</h1>

		</header>
		<aside>
			<img id="slideshow" src="ball.jpg" />
		</aside>
		<main>
		<section style="overflow-x:auto;">
			%s
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
""" % (result2,result))
