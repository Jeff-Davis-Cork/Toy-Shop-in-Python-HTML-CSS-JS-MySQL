#!/usr/local/bin/python3

from cgitb import enable 
enable()

from os import environ
from cgi import FieldStorage, escape
from hashlib import sha256            # Secure Hash Algorithm is a cryptographic hash function designed by the United States National Security Agency and is a U.S. Federal Information Processing Standard 
from time import time
from shelve import open                # A “shelf” is a persistent, dictionary-like object. The difference with “dbm” databases is that the values (not the keys!) in a shelf can be essentially arbitrary Python objects
from http.cookies import SimpleCookie   

result = ''

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

    # Get the id of the item being added to the cart
    form_data = FieldStorage()
    id_num = form_data.getfirst('id_num')
    # If this item is not in the cart already, then quantity is 1; otherwise, increment the quantity.
    qty = session_store.get(id_num)
    if not qty:
        qty = 1
    else:
        qty +=1
    session_store[id_num] = qty
    session_store.close()

    print(cookie)
    result = """<p>Item successfully added to your basket.</p>
                <p>Click on the links to continue shopping and add to your basket!</i></p>
                <p><a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/boys.py" id='larger' >Continue to Shop for <b>Boys Toys</b></a></p>
                <p><a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/girls.py" id='larger' >Continue to Shop for <b>Girls Toys</b></a></p>
                <p><a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/show_cart.py" id='larger' ><b>See Your Basket</b></a></p>
                <p><a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/checkout.py" id='larger' ><b>or... Check Out</b></a></p>
                """

except IOError:
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
				Add To Basket Page: <br></br> The Toy Basket: Used Toy Shop
			</h1>

		</header>
		<aside>
			<img id="slideshow" src="ball.jpg" />
		</aside>
		<main>
		<section>
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
