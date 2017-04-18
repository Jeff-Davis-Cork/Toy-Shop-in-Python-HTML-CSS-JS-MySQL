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
password=''
result = ''
result2=''

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
        result2 = """
                <p id='larger'>No Need to Log In - Welcome Back !</p>
                <p>Click on the links to continue shopping and add to your basket!</i></p>
                <p><a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/boys.py" id='larger' >Continue to Shop for <b>Boys Toys</b></a></p>
                <p><a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/girls.py" id='larger' >Continue to Shop for <b>Girls Toys</b></a></p>
                <p><a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/show_cart.py" id='larger' ><b>See Your Basket</b></a></p>
                <p><a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/checkout.py" id='larger' ><b>or... Check Out</b></a></p>"""
        loggedIn=True
except (IOError):
    result2 = "<p>Sorry! We can't confirm you are logged in or not. Please call back later.</p>"
    
if len(form_data) != 0:
    username = escape(form_data.getfirst('username', '').strip())
    password = escape(form_data.getfirst('password', '').strip())
    if not username or not password:
        result = '<p>Sorry! - you must put in a user name and password</p>'
    else:
        sha256_password = sha256(password.encode()).hexdigest()
        try:
            connection = db.connect(# login here)
            cursor = connection.cursor(db.cursors.DictCursor)
            cursor.execute("SELECT * FROM customers WHERE username = %s AND password = %s", (username,sha256_password))
            if cursor.rowcount == 0:
                result = '<p>Sorry! - the user name or password did not work. Please try again.</p>'
            else:
                cookie = SimpleCookie()
                toy = sha256(repr(time()).encode()).hexdigest()
                cookie['toy'] = toy
                session_store = open('sess_' + toy, writeback=True)
                session_store['authenticated'] = True
                session_store['username'] = username
                session_store.close()
                result = """
                   <p><b>You are now logged in! - Welcome %s!</b></p>
                   <p>Continue shopping and add to your basket!</i></p>
                   <p><a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/boys.py" id='larger' >Shop for <b>Boys Toys</b></a></p>
                   <p><a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/girls.py" id='larger' >Shop for <b>Girls Toys</b></a></p>""" % username
                loggedIn=True
                print(cookie)
            cursor.close()  
            connection.close()
        except (db.Error, IOError):
            result = '<p>Sorry! We are experiencing problems at the moment. Please call back later.</p>'

if not loggedIn:
    result2="""
			<h1>
			Welcome! Please Log In
			</h1>
			    <form action="login.py" method="post">
                                <label for="username">User name: </label>
                                <input type="text" name="username" id="username" value="%s" />
                                <br></br>
                                <label for="password">Password: </label>
                                <input type="password" name="password" id="password" />
                                <br></br>
                                <input type="submit" value="Login!" />
                                <br></br>
                            </form>
                        <p>
                           <a href="http://cs1.ucc.ie/~jd23/cgi-bin/lab7/register.py" id='larger' >Click here if you have not registered yet.</a>
			</p>
			
			""" % username
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
				Login Page: <br></br> The Toy Basket: Used Toy Shop
			</h1>

		</header>
		    <aside>
			<img id="slideshow" src="ball.jpg" />
		    </aside>
		<main>
		   <section>
			<p>
			%s
			</p>
			<p>
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
""" % (result,result2))
