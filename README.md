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
    - ````INSERT INTO Person VALUES($username, $hashed_password, $first_name, $last_name, $email)````
    - ````INSERT INTO PersonPhone VALUES($username, $phone)````
    - ````INSERT INTO Act Values($username, $role)````
- Find Single Item
    - ````SELECT * FROM Piece WHERE itemID = $itemID````
- Find Order Items
    - ````SELECT * FROM ItemIn NATURAL JOIN Item WHERE orderID = $orderID ORDER BY ItemID ASC````
    - ````SELECT * FROM Piece NATURAL JOIN ItemIn WHERE orderID = $orderID ORDER BY pieceNum ASC````
- Accept Donation
    - ````SELECT * FROM Piece WHERE itemID = $itemID````
    - 

Languagesandframeworksyouused●Anychangesyoumadetotheschema,andtheirpurpose●Anyadditionalconstraints,triggers,storedprocedures,etc;●Themainqueriesforeachofthefeaturesyouimplemented.ShowtheseasplainSQL,eitherwithplace-holdersordummyvaluesforvaluesthatarebeingfilledinbasedonusers’choices(similartotheargumentyouwouldpasstoexecuteapreparedstatement).●Anydifficultiesyouencountered,lessonslearned,etc●Whichteammembersdidwhat.Thisreportcanbewritteninbulletpointformatandshouldnotbemorethanafewpageslong.
