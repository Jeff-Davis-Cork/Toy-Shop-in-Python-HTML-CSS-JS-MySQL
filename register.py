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

form_data = FieldStorage()

username=''
fname = ''
lname = ''
full_address = ''
phone = ''
email = ''
result = ''
loggedIn=False
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
    if session_store.get('authenticated'):
        result2 = """<p id='larger'>No Need to Register - You are Logged In!</p>
                <p>Click on the links to continue shopping and add to your basket!</i></p>
                <p><a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/boys.py" id='larger' >Continue to Shop for <b>Boys Toys</b></a></p>
                <p><a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/girls.py" id='larger' >Continue to Shop for <b>Girls Toys</b></a></p>
                <p><a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/show_cart.py" id='larger' ><b>See Your Basket</b></a></p>
                <p><a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/checkout.py" id='larger' ><b>or... Check Out</b></a></p>
"""
        loggedIn=True
    else:
        result2 = "<p><b>Please enter in your details to Sign Up!</b></p>"
except (IOError):
    result2 = "<p>Sorry! We can't confirm you are logged in or not. Please call back later.</p>"
    
if len(form_data) != 0:
    username = escape(form_data.getfirst('username', '').strip())
    password1 = escape(form_data.getfirst('password1', '').strip())
    password2 = escape(form_data.getfirst('password2', '').strip())
    fname = escape(form_data.getfirst('fname', '').strip())
    lname = escape(form_data.getfirst('lname', '').strip())
    full_address = escape(form_data.getfirst('full_address', '').strip())
    phone = escape(form_data.getfirst('phone', '').strip())
    email = escape(form_data.getfirst('email', '').strip())
    if not username or not password1 or not password2 or not fname or not lname or not full_address or not phone or not email:
        result = '<p>Sorry! - you must fill out all the boxes</p>'
    elif password1 !=  password2 :
        result = '<p>Sorry! - your passwords much match up. Please try again.</p>'
    elif '@' not in email:
        result = '<p>Sorry! - Please enter in a valid email address. Please try again.</p>'
    else:
        try:
            connection = db.connect(# login here)
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("SELECT * FROM customers WHERE username = %s" , (username))
            if cursor.rowcount > 0 :
                result = '<p>Sorry! - that user name was already taken. Please choose a different one.</p>'
            else:
                sha256_password = sha256(password1.encode()).hexdigest()
                cursor.execute("""INSERT INTO customers (username, password, fname, lname, email, phone, full_address) 
                                  VALUES (%s, %s, %s, %s, %s, %s, %s)""", (username, sha256_password, fname, lname, email, phone, full_address))
                connection.commit()
                cursor.close()  
                connection.close()
                cookie = SimpleCookie()
                toy = sha256(repr(time()).encode()).hexdigest()
                cookie['toy'] = toy
                session_store = open('sess_' + toy, writeback=True)
                session_store['authenticated'] = True
                session_store['username'] = username
                session_store.close()
                loggedIn=True
                result = """
                   <p id="larger"><b>Congratulations!</b></p>
                   <p>You are now signed up to <i>The Toy Basket !</i></p>
                   <p id="larger">
                      <a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/boys.py">Shop for Boys Toys</a>
                   </p>
                   <p id="larger">
                      <a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/girls.py">Shop for Girls Toys</a>
                   </p>"""
                result2=''
                print(cookie)
        except (db.Error, IOError):
            result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

print('Content-Type: text/html')
print()

if not loggedIn:
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
				Registration Page: <br></br> The Toy Basket: Used Toy Shop
			</h1>

		</header>
		<aside>
			<img id="slideshow" src="ball.jpg" />
		</aside>
		<main>
			<section id="form">
			<p>
			%s
			%s
			</p>
			    <form action="register.py" method="post">
                                <label for="username">User name: </label>
                                <input type="text" name="username" id="username" value="%s" />
                                <br></br>
                                <label for="password1">Password: </label>
                                <input type="password" name="password1" id="password1" />
                                <br></br>
                                <label for="passwords2">Re-enter password: </label>
                                <input type="password" name="password2" id="password2" />
                                <br></br>
                                <label for="fname">Your First Name: </label>
                                <input type="text" name="fname" id="fname" value="%s" />
                                <br></br>
                                <label for="lname">Your Last Name: </label>
                                <input type="text" name="lname" id="lname" value="%s" />
                                <br></br>
                                <label for="full_address">Your Full Address: </label>
                                <input type="text" name="full_address" id="full_address" value="%s" />
                                <br></br>
                                <label for="email">Your Email: </label>
                                <input type="text" name="email" id="email" value="%s" />
                                <br></br>
                                <label for="phone">Phone Number: </label>
                                <input type="text" name="phone" id="phone" value="%s" />
                                <br></br>
                                <input type="submit" value="Sign Up!" />
                                <br></br>
                            </form>
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
""" % (result2,result,username,fname,lname,full_address,email,phone))
else:
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
				Registration Page: <br></br> The Toy Basket: Used Toy Shop
			</h1>

		</header>
		<aside>
			<img id="slideshow" src="ball.jpg" />
		</aside>
		<main>
			<section>
			<p>
			%s
			%s
			</p>
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

