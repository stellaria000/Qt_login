USE TEST;

CREATE TABLES- SYSTEMS, ACCOUNTS
CREATE TABLE SYSTEMS(
 SYS_ID INTEGER PRIMARY KEY, 
 SYS_NAME VARCHAR(50)
);

CREATE TABLE ACCOUNTS(
 ACCOUNT_PACKAGE_LIST VARCHAR(64), 
 ID VARCHAR(255) PRIMARY KEY, 
 PASSWORD INTEGER
);

# INSERT INTO DATABASE- SYSTEMS
INSERT INTO SYSTEMS 
VALUES(1, "SECURITY"), 
(2, "INTERSECTION");
INSERT INTO SYSTEMS 
VALUES(3, "SCHOOLZONE"), (4, "LEFT_TURN");

INSERT INTO SYSTEMS VALUES
(5, "NEW SYSTEM 1"), (6, "NEW SYSTEM 2";)

# INSERT INTO DATABASE- ACCOUNTS
-- INSERT INTO ACCOUNTS VALUES(WRONG QUERY)
-- (1, "SEC", 1234), (2, "ITS", 1234), (3, "SCH", 1234), (4, "LFT", 1234)
-- SELECT A.SYS_ID, A.ID, A.PASSWORD 
-- FROM ACCOUNTS A, SYSTEMS S
-- WHERE A.SYS_ID = S.SYS_ID;

-- RIGHT QUERY
INSERT INTO ACCOUNTS (SYS_ID, ID, PASSWORD)
SELECT S.SYS_ID, 'new_id', 1234 
FROM SYSTEMS S
WHERE S.SYS_ID = 1;

-- INSERT INTO ACCOUNTS VALUES 
-- ('1', "SEC", 1234), ('2', "ITS", 1234), ('3', "SCH", 1234), ('4', "LFT", 1234);
INSERT INTO ACCOUNTS VALUES ('1', "SEC", 1234), ('4', "LFT", 1234);
INSERT INTO ACCOUNTS(ID, PASSWORD) VALUES("ADMINISTRATOR", 1234);
-- SELECT TO SEE THE DATAS
SELECT * FROM ACCOUNTS
WHERE ACCOUNT_PACKAGE_LIST LIKE '1%'
   OR ACCOUNT_PACKAGE_LIST LIKE '%1%'
   OR ACCOUNT_PACKAGE_LIST LIKE '%1'
   OR ACCOUNT_PACKAGE_LIST = '1';

SELECT * FROM SYSTEMS;
SELECT * FROM ACCOUNTS;

SELECT COUNT(ACCOUNT_PACKAGE_LIST) FROM ACCOUNTS
WHERE ACCOUNT_PACKAGE_LIST LIKE '%1%' 
OR ACCOUNT_PACKAGE_LIST LIKE '%1'
OR ACCOUNT_PACKAGE_LIST LIKE '%1%'
OR ACCOUNT_PACKAGE_LIST= '1';

-- SELECT S.SYS_ID, A.ID, A.PASSWORD
-- FROM ACCOUNTS A, SYSTEMS S
-- WHERE S.SYS_ID= A.SYS_ID
-- ORDER BY A.SYS_ID ASC ;

--  GENERATE TESTING ACCOUNTS
INSERT INTO ACCOUNTS(ACCOUNT_PACKAGE_LIST, ID, PASSWORD) VALUES 
("1", "SECURITY", 1234), 
("1, 2", "CCTV", 1234), 
("2", "ITS", 1234), 
("2, 3", "INTERSECTION", 1234), 
("2, 1", "INTSEC", 1234), 
("3", "SCH", 1234), 
("3", "SCHOOLZONE", 1234), 
("3, 2", "SZONE", 1234), 
("4, 1", "LEFT", 1234), 
("4", "LEFT_TURN", 1234), 
("4, 2", "LTURN", 1234);

-- DELETE DATAS IN TABLES
DELETE FROM SYSTEMS;
DELETE FROM ACCOUNTS;

-- DELETE TABLES
DROP TABLE SYSTEMS;
DROP TABLE ACCOUNTS;

