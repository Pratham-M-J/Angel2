create database angel2;

use angel2;

CREATE TABLE Broker (
    BrokerID INT(5) PRIMARY KEY,
    Name VARCHAR(15) NOT NULL,
    CommissionRate DECIMAL(5,2) NOT NULL,
    LicenseNumber VARCHAR(15) UNIQUE NOT NULL
);

INSERT INTO Broker VALUES (10001, 'AlphaSec', 0.50, 'LIC12345');

CREATE TABLE Stock ( 
	Stock_ID INT (5) PRIMARY KEY,
	`Stock Name` VARCHAR(15), 
    `Stock Price` INT (5), 
    `PE Ratio` INT (3)
);

CREATE TABLE `Futures & Options`(
	`F&O ID` INT (5) PRIMARY KEY, 
    `Type` VARCHAR (7), 
    `Contract Size` INT(5), 
    `Underlying Asset` INT (5), 
    `Expiry Date` date, Derivates INT (5)
);

CREATE TABLE `Order` (
	`Order ID` INT (5) PRIMARY KEY, 
	`Stock Name` VARCHAR (15), 
	Quantity INT (5), 
	`Stock ID` INT,
);


CREATE TABLE Trader ( 
	`DMAT Account Number` INT (5) NOT NULL PRIMARY KEY, 
    `Phone Number` INT (10), 
    `Name` VARCHAR (15) NOT NULL, 
    `Mail ID` VARCHAR (15), 
    Age INT (3) NOT NULL, 
    `Order ID` INT (5));

CREATE TABLE has_info (
    BrokerID INT(5),
    `Stock ID` INT(5),
    PRIMARY KEY (BrokerID, `Stock ID`),
    FOREIGN KEY (BrokerID) REFERENCES Broker(BrokerID),
    FOREIGN KEY (`Stock ID`) REFERENCES Stock(`Stock ID`)
);

create table trader_order (
	`trader id` int (5),
    `order id` int (5),
    primary key (`trader id`, `order id`),
    foreign key (`trader id`) references trader(`trader id`),
    foreign key (`order id`) references `order`(`order id`)
);

create table phone_number (
	`trader id` int (5),
    foreign key (`trader id`) references trader(`trader id`),
    phone_number int (10)
);


create table `mail id` (
	`trader id` int (5),
    foreign key (`trader id`) references trader(`trader id`),
    mail varchar (25)
);






