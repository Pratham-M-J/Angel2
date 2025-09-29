create database angel2;

use angel2;

CREATE TABLE `Stock` (
    `Stock ID` INT(5) NOT NULL PRIMARY KEY,
    `Stock Name` VARCHAR(15) NOT NULL,
    `Stock Price` INT NOT NULL,
    `PE Ratio` INT
);

CREATE TABLE `Trader` (
    `DMAT Account Number` INT NOT NULL PRIMARY KEY,
    `Phone Number` INT,
    `Name` VARCHAR(15) NOT NULL,
    `Mail ID` VARCHAR(15),
    `Age` INT NOT NULL,
    `Order ID` INT
);

CREATE TABLE `Futures & Options` (
    `F&O ID` INT PRIMARY KEY,
    `Type` VARCHAR(7),
    `Contract Size` INT,
    `Underlying Asset` INT,
    `Expiry Date` DATE,
    `Derivates` INT
);

CREATE TABLE `Order` (
    `Order ID` INT PRIMARY KEY,
    `Stock Name` VARCHAR(15),
    `Quantity` INT,
    `Stock ID` INT
);


CREATE TABLE Broker (
    BrokerID INT PRIMARY KEY,
    Name VARCHAR(15) NOT NULL,
    CommissionRate DECIMAL(5,2) NOT NULL,
    LicenseNumber VARCHAR(15) UNIQUE NOT NULL
);

CREATE TABLE has_info (
    BrokerID INT(5),
    `Stock ID` INT(5),
    PRIMARY KEY (BrokerID, `Stock ID`),
    FOREIGN KEY (BrokerID) REFERENCES Broker(BrokerID),
    FOREIGN KEY (`Stock ID`) REFERENCES Stock(`Stock ID`)
);

create table trader_order (
	`trader id` int,
    `order id` int,
    primary key (`trader id`, `order id`),
    foreign key (`trader id`) references trader(`DMAT Account Number`),
    foreign key (`order id`) references `order`(`order id`)
);

create table phone_number (
	`trader id` int ,
    foreign key (`trader id`) references trader(`DMAT Account Number`),
    phone_number int (10)
);


create table `mail id` (
	`trader id` int,
    foreign key (`trader id`) references trader(`DMAT Account Number`),
	`mail id` varchar (25)
);






