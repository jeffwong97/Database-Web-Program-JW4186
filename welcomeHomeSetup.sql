DROP TABLE IF EXISTS Delivered;
DROP TABLE IF EXISTS ItemIn;
DROP TABLE IF EXISTS Ordered;
DROP TABLE IF EXISTS Piece;
DROP TABLE IF EXISTS Location;
DROP TABLE IF EXISTS Act;
DROP TABLE IF EXISTS Role;
DROP TABLE IF EXISTS DonatedBy;
DROP TABLE IF EXISTS PersonPhone;
DROP TABLE IF EXISTS Person;
DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS Category;

CREATE TABLE Category (
    mainCategory VARCHAR(50) NOT NULL,
    subCategory VARCHAR(50) NOT NULL,
    catNotes TEXT,
    PRIMARY KEY (mainCategory, subCategory)
);

CREATE TABLE Item (
    ItemID INT NOT NULL AUTO_INCREMENT,
    iDescription TEXT,
    photo BLOB, -- BLOB is better here, but for simplicity, we change it to VARCHAR; For p3 implementation, we recommend you to implement as blob
    color VARCHAR(20),
    isNew BOOLEAN DEFAULT TRUE,
    hasPieces BOOLEAN,
    material VARCHAR(50),
    mainCategory VARCHAR(50) NOT NULL,
    subCategory VARCHAR(50) NOT NULL,
    PRIMARY KEY (ItemID),
    FOREIGN KEY (mainCategory, subCategory) REFERENCES Category(mainCategory, subCategory)
);


CREATE TABLE Person (
    userName VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    PRIMARY KEY (userName)
);

CREATE TABLE PersonPhone (
    userName VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    PRIMARY KEY (userName, phone),
    FOREIGN KEY (userName) REFERENCES Person(userName)
);

CREATE TABLE DonatedBy (
    ItemID INT NOT NULL,
    userName VARCHAR(50) NOT NULL,
    donateDate DATE NOT NULL,
    PRIMARY KEY (ItemID, userName),
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID),
    FOREIGN KEY (userName) REFERENCES Person(userName)
);

CREATE TABLE Role (
    roleID VARCHAR(20) NOT NULL,
    rDescription VARCHAR(100),
    PRIMARY KEY (roleID)
);

CREATE TABLE Act (
    userName VARCHAR(50) NOT NULL,
    roleID VARCHAR(20) NOT NULL,
    PRIMARY KEY (userName, roleID),
    FOREIGN KEY (userName) REFERENCES Person(userName),
    FOREIGN KEY (roleID) REFERENCES Role(roleID)
);

CREATE TABLE Location (
    roomNum INT NOT NULL,
    shelfNum INT NOT NULL, -- not a point for deduction
    shelf VARCHAR(20),
    shelfDescription VARCHAR(200),
    PRIMARY KEY (roomNum, shelfNum)
);



CREATE TABLE Piece (
    ItemID INT NOT NULL,
    pieceNum INT NOT NULL,
    pDescription VARCHAR(200),
    length INT NOT NULL, -- for simplicity
    width INT NOT NULL,
    height INT NOT NULL,
    roomNum INT NOT NULL,
    shelfNum INT NOT NULL, 
    pNotes TEXT,
    PRIMARY KEY (ItemID, pieceNum),
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID),
    FOREIGN KEY (roomNum, shelfNum) REFERENCES Location(roomNum, shelfNum)
);

CREATE TABLE Ordered (
    orderID INT NOT NULL AUTO_INCREMENT,
    orderDate DATE NOT NULL,
    orderNotes VARCHAR(200),
    supervisor VARCHAR(50) NOT NULL,
    client VARCHAR(50) NOT NULL,
    PRIMARY KEY (orderID),
    FOREIGN KEY (supervisor) REFERENCES Person(userName),
    FOREIGN KEY (client) REFERENCES Person(userName)
);

CREATE TABLE ItemIn (
    ItemID INT NOT NULL,
    orderID INT NOT NULL,
    found BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (ItemID, orderID),
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID),
    FOREIGN KEY (orderID) REFERENCES Ordered(orderID)
);


CREATE TABLE Delivered (
    userName VARCHAR(50) NOT NULL,
    orderID INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    PRIMARY KEY (userName, orderID),
    FOREIGN KEY (userName) REFERENCES Person(userName),
    FOREIGN KEY (orderID) REFERENCES Ordered(orderID)
);


-- Test data
INSERT INTO Person VALUES ('jeffclient', '$2b$12$fMsmEgQr5I6qUfmha0Js/On3R0wFH8ZkfBLljwtxM9gOZVNy1.flW', 'jeff', 'client', 'jeffclient@nyu.edu'); --pwd: jeffclient
INSERT INTO Person VALUES ('jeffdonor', '$2b$12$nY62hYB43UNbF6NpM8FA3.t9RclIPruw4L9DY/JBUYBCBId/gjs66', 'jeff', 'donor', 'jeffdonor@nyu.edu'); --pwd: jeffdonor
INSERT INTO Person VALUES ('jeffstaff', '$2b$12$c.OCHX9lf5352Atb9dtqc.CNyabEvacTfUnq.2LPDeHSYWz4B3ety', 'jeff', 'staff', 'jeffstaff@nyu.edu'); --pwd: jeffstaff
INSERT INTO Person VALUES ('jeffvolunteer', '$2b$12$HFeR3W4mWRSgESsTPWZ3mO.E08SxcfuLIkQzL26/7vLmL2pjEaqSC', 'jeff', 'volunteer', 'jeffvolunteer@nyu.edu'); --pwd: jeffvolunteer
INSERT INTO PersonPhone VALUES ('jeffclient', '5678901234'), ('jeffdonor', '2345678901'), ('jeffstaff', '3456789012'), ('jeffvolunteer', '4567890123');
INSERT INTO Role VALUES ('1', 'Client'), ('2', 'Donor'), ('3', 'Staff'), ('4', 'Volunteer');
INSERT INTO Act VALUES ('jeffclient', '1'), ('jeffdonor', '2'), ('jeffstaff', '3'), ('jeffvolunteer', '4');
INSERT INTO Category VALUES ('Furniture', 'Sofa', 'no notes'), ('Furniture', 'Chair', 'no notes'), ('Furniture', 'Dining Set', 'no notes'), ('Kitchenware', 'Pots and Pans', 'no notes');
INSERT INTO Ordered VALUES (12345, DATE '2024-11-08', 'multiple pieces', 'jeffstaff', 'jeffclient'), (23456, DATE '2024-11-06', NULL, 'jeffstaff', 'jeffclient');
INSERT INTO Delivered VALUES ('jeffstaff', 12345, 'Scheduled', DATE '2024-11-12'), ('jeffvolunteer', 23456, 'Completed', DATE '2024-11-10');
INSERT INTO Item (iDescription, isNew, hasPieces, mainCategory, subCategory) VALUES ('Brown leather armchair', FALSE, FALSE, 'Furniture', 'Chair'), ('Walnut dining table w/4 chairs', FALSE, TRUE, 'Furniture', 'Dining Set'), ('12 inch cast iron pan', TRUE, FALSE, 'Kitchenware', 'Pots and Pans'), ('2-piece yellow sofa', FALSE, TRUE, 'Furniture', 'Sofa');
INSERT INTO DonatedBy VALUES (1, 'jeffdonor', DATE '2024-10-01'), (2, 'jeffdonor', DATE '2024-09-01'), (3, 'jeffdonor', DATE '2024-08-01'), (4, 'jeffdonor', DATE '2024-11-01');
INSERT INTO ItemIn VALUES (1, 12345, TRUE), (2, 23456, FALSE), (3, 23456, TRUE);
INSERT INTO Location VALUES (5, 0, 'shelf', 'shelf'), (1, 1, 'shelf', 'shelf'), (1, 2, 'shelf', 'shelf'), (2, 1, 'shelf', 'shelf');
INSERT INTO Piece VALUES (1, 1, 'Only Piece', 4, 5, 6, 1, 1, 'no notes'), (2, 1, 'Table', 7, 8, 9, 1, 2, 'heavy'), (2, 2, 'Chairs', 2, 3, 4, 1, 2, '4 chairs'), (3, 1, 'Only Piece', 1, 1, 1, 2, 1, 'no notes'), (4, 1, 'Sofa body', 10, 11, 12, 5, 0, 'heavy'), (4, 2, 'Cushion', 1, 1, 1, 5, 0, '4 cushions');