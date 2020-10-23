DROP DATABASE IF EXISTS tasklist;
CREATE DATABASE tasklist;

DROP DATABASE IF EXISTS tasklist_test;
CREATE DATABASE tasklist_test;

DROP USER IF EXISTS tasklist_admin@localhost;
CREATE USER tasklist_admin@localhost IDENTIFIED BY "senha super dificil";
GRANT ALL ON tasklist.* TO tasklist_admin@localhost;
GRANT ALL ON tasklist_test.* TO tasklist_admin@localhost;

DROP USER IF EXISTS tasklist_app@localhost;
CREATE USER tasklist_app@localhost IDENTIFIED BY "senha impossivel";
GRANT SELECT, INSERT, UPDATE, DELETE ON tasklist.* TO tasklist_app@localhost;
GRANT SELECT, INSERT, UPDATE, DELETE ON tasklist_test.* TO tasklist_app@localhost;

COMMIT