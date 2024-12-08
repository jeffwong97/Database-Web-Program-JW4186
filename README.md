# Database-Web-Program-JW4186
 Final project for Database Systems class

- Languages: Python, HTML
- Frameworks: flask, pymysql, bcrypt (for password encryption)
- Procedures:
    - Create MySQL Database 'WelcomeHome' on port 8889
    - Use provided SQL file to initialize tables and insert test data
    - Make sure port 5000 is open
    - ````python ./init.py````

### SQL Inquiries Used
- Login and User Session Handling
    - ````SELECT * FROM Person WHERE username = $username````
    - ````INSERT INTO Person VALUES($username, $hashedPassword, $firstName, $lastName, $email)````
    - ````INSERT INTO PersonPhone VALUES($username, $phone)````
    - ````INSERT INTO Act Values($username, $role)````
- Find Single Item
    - ````SELECT * FROM Piece WHERE itemID = $itemID````
- Find Order Items
    - ````SELECT * FROM ItemIn NATURAL JOIN Item WHERE orderID = $orderID ORDER BY ItemID ASC````
    - ````SELECT * FROM Piece NATURAL JOIN ItemIn WHERE orderID = $orderID ORDER BY pieceNum ASC````
- Accept Donation
    - ````SELECT rDescription FROM Role NATURAL JOIN Act WHERE userName = $username````
    - ````SELECT roleID FROM Act WHERE userName = $donorName````
    - ````SELECT * FROM Category WHERE mainCategory = $mainCategory AND subCategory = $subCategory````
    - ````INSERT INTO Category (mainCategory, subCategory) VALUES ($mainCategory, $subCategory)````
    - ````INSERT INTO Item (iDescription, color, isNew, hasPieces, material, mainCategory, subCategory) VALUES ($description, $color, $isNew, $hasPieces, $material, $mainCategory, $subCategory)````
    - ````INSERT INTO DonatedBy VALUES ($itemID, $donorName, $donateDate)````
    - ````UPDATE Item SET photo = $photo WHERE itemID = $itemID````
    - ````SELECT * FROM Piece WHERE ItemID = $itemID AND pieceNum = $pieceNum````
    - ````SELECT * FROM Location WHERE roomNum = $roomNum AND shelfNum = $shelfNum````
    - ````INSERT INTO Location (roomNum, shelfNum) VALUES ($roomNum, $shelfNum)````
    - ````INSERT INTO Piece VALUES ($itemID, $pieceNum, $pDescription, $length, $width, $height, $roomNum, $shelfNum, $pNotes)````
- Additional Feature 8: User's Tasks
    - ````SELECT * FROM Delivered LEFT JOIN Ordered ON Ordered.orderID = Delivered.orderID WHERE Delivered.userName = $username OR Ordered.supervisor = $username OR Ordered.client = $username UNION SELECT * FROM Delivered RIGHT JOIN Ordered ON Delivered.orderID = Ordered.orderID WHERE Delivered.userName = $username OR Ordered.supervisor = $username OR Ordered.client = $username````
- Additional Feature 10: Update Enabled
    - ````UPDATE Delivered SET status = $status WHERE orderID = $orderID````

### Lessons Learned
- First time using flask and bcrypt

### Work Division
- Worked individually for the entire project
