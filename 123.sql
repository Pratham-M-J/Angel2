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
    foreign key (`trader id`) references trader(`trader id`),
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

ALTER TABLE `Futures & Options`
ADD CONSTRAINT derivative_of_derivative
FOREIGN KEY (Derivates) REFERENCES `Futures & Options`(`F&O ID`);

ALTER TABLE `Trader`
ADD CONSTRAINT trader_orderid
FOREIGN KEY (`Order ID`) REFERENCES `Order`(`Order ID`);

ALTER TABLE `Order`
ADD CONSTRAINT order_stockid
FOREIGN KEY (`Stock ID`) REFERENCES `Stock`(`Stock ID`);

ALTER TABLE `Futures & Options`
ADD CONSTRAINT underlying_asset
FOREIGN KEY (`Underlying Asset`) REFERENCES `Stock` (`Stock ID`);

ALTER TABLE Broker
ADD CONSTRAINT chk_commission CHECK (CommissionRate >= 0);

ALTER TABLE has_info
DROP FOREIGN KEY has_info_ibfk_1,
DROP FOREIGN KEY has_info_ibfk_2;

ALTER TABLE has_info
ADD CONSTRAINT fk_hasinfo_broker FOREIGN KEY (BrokerID)
    REFERENCES Broker(BrokerID)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_hasinfo_stock FOREIGN KEY (`Stock ID`)
    REFERENCES Stock(`Stock ID`)
    ON DELETE CASCADE ON UPDATE CASCADE;


alter table trader_order
drop foreign key trader_order_ibfk_1,
drop foreign key trader_order_ibfk_2;

ALTER TABLE trader_order
ADD CONSTRAINT fk_traderorder_trader FOREIGN KEY (`trader id`)
    REFERENCES Trader(`DMAT Account Number`)
    ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT fk_traderorder_order FOREIGN KEY (`order id`)
    REFERENCES `Order`(`order id`)
    ON DELETE CASCADE ON UPDATE CASCADE;
    
ALTER TABLE phone_number
ADD CONSTRAINT pk_phone PRIMARY KEY (`trader id`, phone_number);

ALTER TABLE phone_number
MODIFY phone_number VARCHAR(15) NOT NULL;

ALTER TABLE `mail id`
ADD CONSTRAINT pk_mail PRIMARY KEY (`trader id`, `mail id`);

ALTER TABLE `mail id`
MODIFY `mail id` VARCHAR(25) NOT NULL;





