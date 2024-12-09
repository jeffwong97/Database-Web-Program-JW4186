#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
from app import app
import pymysql.cursors
import bcrypt
import os
from datetime import date
from werkzeug.utils import secure_filename
import bleach


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port = 8889,
                       user='root',
                       password='root',
                       db='WelcomeHome',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


#Define a route to landing page
@app.route('/')
def index():
    if session.get("logged_in"):
         return redirect(url_for('home'))
    return render_template('index.html')


#Define route for login
@app.route('/login')
def login():
    if session.get("logged_in"):
         return redirect(url_for('home'))
    return render_template('login.html')


#Define route for register
@app.route('/register')
def register():
    if session.get("logged_in"):
         return redirect(url_for('home'))
    return render_template('register.html')


#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    if session.get("logged_in"):
         return redirect(url_for('home'))
    if request.method == 'GET':
         return redirect(url_for('login'))
    #grabs information from the forms
    username = bleach.clean(request.form['username'])
    password = bleach.clean(request.form['password'])

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Person WHERE username = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    cursor.close()
    error = None
    if(data):
        #compare hashed passwords
        hashed = data.get('password')
        hashed_bytes = hashed.encode('utf-8')
        password_bytes = password.encode('utf-8')
        if bcrypt.hashpw(password_bytes, hashed_bytes) == hashed_bytes:
            #creates a session for the the user
            session['username'] = username
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            #returns an error message to the html page
            error = 'Incorrect password'
            return render_template('login.html', error=error)
    else:
        #returns an error message to the html page
        error = 'Invalid username'
        return render_template('login.html', error=error)


#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    if session.get("logged_in"):
         return redirect(url_for('home'))
    if request.method == 'GET':
         return redirect(url_for('register'))
    #grabs information from the forms
    username = bleach.clean(request.form['username'])
    password = bleach.clean(request.form['password'])
    fname = bleach.clean(request.form['fname'])
    lname = bleach.clean(request.form['lname'])
    email = bleach.clean(request.form['email'])
    phone = bleach.clean(request.form['phone'])
    role = bleach.clean(request.form['role'])

    #salt and hash password
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Person WHERE username = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO Person VALUES(%s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, hashed, fname, lname, email))
        phoneins = 'INSERT INTO PersonPhone VALUES(%s, %s)'
        cursor.execute(phoneins, (username, phone))
        actins = 'INSERT INTO Act VALUES(%s, %s)'
        cursor.execute(actins, (username, role))
        conn.commit()
        cursor.close()
        return render_template('index.html')


@app.route('/home')
def home():
    if not session.get("logged_in"):
        return redirect(url_for('index'))
    user = session['username']
    cursor = conn.cursor()
    query = 'SELECT rDescription FROM Role NATURAL JOIN Act WHERE userName = %s'
    cursor.execute(query, (user))
    role = cursor.fetchone()

    #Additional Features 8: User's tasks and 10: Update enabled
    query = 'SELECT * FROM Delivered LEFT JOIN Ordered ON Ordered.orderID = Delivered.orderID WHERE Delivered.userName = %s OR Ordered.supervisor = %s OR Ordered.client = %s UNION SELECT * FROM Delivered RIGHT JOIN Ordered ON Delivered.orderID = Ordered.orderID WHERE Delivered.userName = %s OR Ordered.supervisor = %s OR Ordered.client = %s'
    cursor.execute(query, (user, user, user, user, user, user))
    tasks = cursor.fetchall()
    conn.commit()
    cursor.close()
    return render_template('home.html', username=user, role=role, tasks=tasks)

        
@app.route('/item', methods=['GET', 'POST'])
def item():
    if not session.get("logged_in"):
        return redirect(url_for('index'))
    if request.method == 'GET':
         return redirect(url_for('home'))
    username = session['username']
    itemID = bleach.clean(request.form['itemID'])
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Piece WHERE itemID = %s'
    cursor.execute(query, (itemID))
    #stores the results in a variable
    data = cursor.fetchall()
    #use fetchall() if you are expecting more than 1 data row
    query = 'SELECT rDescription FROM Role NATURAL JOIN Act WHERE userName = %s'
    cursor.execute(query, (username))
    role = cursor.fetchone()
    query = 'SELECT * FROM Delivered LEFT JOIN Ordered ON Ordered.orderID = Delivered.orderID WHERE Delivered.userName = %s OR Ordered.supervisor = %s OR Ordered.client = %s UNION SELECT * FROM Delivered RIGHT JOIN Ordered ON Delivered.orderID = Ordered.orderID WHERE Delivered.userName = %s OR Ordered.supervisor = %s OR Ordered.client = %s'
    cursor.execute(query, (username, username, username, username, username, username))
    tasks = cursor.fetchall()
    conn.commit()
    cursor.close()
    if (data):
        message = "Here are the locations for all pieces in item " + itemID
    else:
         message = "Item does not exist!"
    return render_template('home.html', username=username, pieces=data, itemMessage=message, role=role, tasks=tasks)


@app.route('/order', methods=['GET', 'POST'])
def order():
    if not session.get("logged_in"):
        return redirect(url_for('index'))
    if request.method == 'GET':
         return redirect(url_for('home'))
    username = session['username']
    orderID = bleach.clean(request.form['orderID'])
    cursor = conn.cursor()
    itemQuery = 'SELECT * FROM ItemIn NATURAL JOIN Item WHERE orderID = %s ORDER BY ItemID ASC'
    cursor.execute(itemQuery, (orderID))
    items = cursor.fetchall()
    pieceQuery = 'SELECT * FROM Piece NATURAL JOIN ItemIn WHERE orderID = %s ORDER BY pieceNum ASC'
    cursor.execute(pieceQuery, (orderID))
    pieces = cursor.fetchall()
    query = 'SELECT rDescription FROM Role NATURAL JOIN Act WHERE userName = %s'
    cursor.execute(query, (username))
    role = cursor.fetchone()
    query = 'SELECT * FROM Delivered LEFT JOIN Ordered ON Ordered.orderID = Delivered.orderID WHERE Delivered.userName = %s OR Ordered.supervisor = %s OR Ordered.client = %s UNION SELECT * FROM Delivered RIGHT JOIN Ordered ON Delivered.orderID = Ordered.orderID WHERE Delivered.userName = %s OR Ordered.supervisor = %s OR Ordered.client = %s'
    cursor.execute(query, (username, username, username, username, username, username))
    tasks = cursor.fetchall()
    conn.commit()
    cursor.close()
    if pieces:
        message = "Here are the locations for all pieces in order " + orderID
    else:
         message = "Order does not exist!"
    return render_template('home.html', username=username, items=items, itemsPieces=pieces, orderMessage=message, role=role, tasks=tasks)
    

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload():
    if not session.get("logged_in"):
        return redirect(url_for('index'))
    if request.method == 'POST':
        message = ""
        cursor = conn.cursor()
        username = session['username']
        query = 'SELECT rDescription FROM Role NATURAL JOIN Act WHERE userName = %s'
        cursor.execute(query, (username))
        userRole = cursor.fetchone()
        donor = bleach.clean(request.form['donor'])
        description = bleach.clean(request.form['description'])
        color = bleach.clean(request.form['color'])
        isNew = bleach.clean(request.form['isNew'])
        hasPieces = bleach.clean(request.form['hasPieces'])
        material = bleach.clean(request.form['material'])
        mainCategory = bleach.clean(request.form['mainCategory'])
        subCategory = bleach.clean(request.form['subCategory'])

        #check donor role
        query = 'SELECT roleID FROM Act WHERE userName = %s'
        cursor.execute(query, (donor))
        donorRole = cursor.fetchone()
        if (donorRole is None or donorRole.get('roleID') != '2'):
            message = 'No donor found with the provided username'
            query = 'SELECT * FROM Delivered LEFT JOIN Ordered ON Ordered.orderID = Delivered.orderID WHERE Delivered.userName = %s OR Ordered.supervisor = %s OR Ordered.client = %s UNION SELECT * FROM Delivered RIGHT JOIN Ordered ON Delivered.orderID = Ordered.orderID WHERE Delivered.userName = %s OR Ordered.supervisor = %s OR Ordered.client = %s'
            cursor.execute(query, (username, username, username, username, username, username))
            tasks = cursor.fetchall()
            conn.commit()
            cursor.close()
            return render_template('home.html', username=username, error=message, role=userRole, tasks=tasks)
        
        # add category if not preexisting
        query = 'SELECT * FROM Category WHERE mainCategory = %s AND subCategory = %s'
        cursor.execute(query, (mainCategory, subCategory))
        category = cursor.fetchone()
        if (category is None):
            query = 'INSERT INTO Category (mainCategory, subCategory) VALUES (%s, %s)'
            cursor.execute(query, (mainCategory, subCategory))

        # add to item table
        query = 'INSERT INTO Item (iDescription, color, isNew, hasPieces, material, mainCategory, subCategory) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query, (description, color, isNew, hasPieces, material, mainCategory, subCategory))

        # add to DonatedBy table
        itemID = cursor.lastrowid
        donateDate = date.today()
        query = 'INSERT INTO DonatedBy VALUES (%s, %s, %s)'
        cursor.execute(query, (itemID, donor, donateDate))

        # check if the post request has the file part
        if 'photo' not in request.files:
            message = 'Donation accepted'
            conn.commit()
            cursor.close()
            return render_template('piece.html', username=username, message=message, itemID=itemID, hasPieces=hasPieces)
        file = request.files['photo']
        if file.filename == '':
            message = 'Donation accepted'
            conn.commit()
            cursor.close()
            return render_template('piece.html', username=username, message=message, itemID=itemID, hasPieces=hasPieces)
        if file and allowed_file(file.filename):
            # if saving picture to folder instead
            # filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            binary = file.read()
            query = 'UPDATE Item SET photo = %s WHERE itemID = %s'
            cursor.execute(query, (binary, itemID))
            conn.commit()
            cursor.close()
            file.close()
            message = 'Donation accepted with photo'
            return render_template('piece.html', username=username, message=message, itemID=itemID, hasPieces=hasPieces)
        else:
            message = 'Donation accepted without photo. Allowed file types are png, jpg, jpeg, gif'
            return render_template('piece.html', username=username, message=message, itemID=itemID, hasPieces=hasPieces)
    else:
        return redirect(url_for('home'))


@app.route('/piece', methods=['POST'])
def piece():
    if not session.get("logged_in"):
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = session['username']
        itemID = bleach.clean(request.form['itemID'])
        pieceNum = bleach.clean(request.form['pieceNum'])
        pDescription = bleach.clean(request.form['pDescription'])
        length = bleach.clean(request.form['length'])
        width = bleach.clean(request.form['width'])
        height = bleach.clean(request.form['height'])
        roomNum = bleach.clean(request.form['roomNum'])
        shelfNum = bleach.clean(request.form['shelfNum'])
        pNotes = bleach.clean(request.form['pNotes'])
        hasPieces = bleach.clean(request.form['hasPieces'])
        more = bleach.clean(request.form['continue'])

        # check if pieceNum is unique for item
        cursor = conn.cursor()
        query = 'SELECT * FROM Piece WHERE ItemID = %s AND pieceNum = %s'
        cursor.execute(query, (itemID, pieceNum))
        data = cursor.fetchone()
        if (data):
            message = 'A piece with this number already exists for this item'
            conn.commit()
            cursor.close()
            return render_template('piece.html', username=username, message=message, itemID=itemID, hasPieces=hasPieces)
        query = 'SELECT * FROM Location WHERE roomNum = %s AND shelfNum = %s'
        cursor.execute(query, (roomNum, shelfNum))
        data = cursor.fetchone()
        if (data is None):
            query = 'INSERT INTO Location (roomNum, shelfNum) VALUES (%s, %s)'
            cursor.execute(query, (roomNum, shelfNum))
        query = 'INSERT INTO Piece VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query, (itemID, pieceNum, pDescription, length, width, height, roomNum, shelfNum, pNotes))
        conn.commit()
        cursor.close()
        if (more == 'yes'):
            message = 'Piece location logged, please continue'
            return render_template('piece.html', username=username, message=message, itemID=itemID, hasPieces=hasPieces)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


# Additional Feature 10: update enabled
@app.route('/update', methods=['POST'])
def update():
    if not session.get("logged_in"):
        return redirect(url_for('index'))
    if not request.method == 'POST':
        return redirect(url_for('home'))
    orderID = bleach.clean(request.form['orderID'])
    newStatus = bleach.clean(request.form['newStatus'])
    cursor = conn.cursor()
    query = 'UPDATE Delivered SET status = %s WHERE orderID = %s'
    cursor.execute(query, (newStatus, orderID))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('username')
    return redirect('/')


app.secret_key = 'afdhuaisfo3w8efaof9428e9afuaf'
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = False)

