BEGIN TRANSACTION;
DROP TABLE IF EXISTS "tblSource";
CREATE TABLE IF NOT EXISTS "tblSource" (
	"Source_ID"	INTEGER UNIQUE,
	"Source_Name"	TEXT,
	"Source_Website"	TEXT,
	PRIMARY KEY("Source_ID" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "tblArtist";
CREATE TABLE IF NOT EXISTS "tblArtist" (
	"Artist_ID"	INTEGER UNIQUE,
	"Artist_Name"	TEXT,
	"Artist_Website"	TEXT,
	"Artist_Email"	TEXT,
	"Artist_Folder"	TEXT,
	PRIMARY KEY("Artist_ID" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "tblModel";
CREATE TABLE IF NOT EXISTS "tblModel" (
	"Model_ID"	INTEGER UNIQUE,
	"Model_Name"	TEXT,
	"Artist"	INTEGER,
	"Set_Name"	TEXT,
	"Source"	INTEGER,
	"Source_Note"	TEXT,
	"Supports"	INTEGER,
	"Format"	TEXT,
	"Printed"	INTEGER,
	PRIMARY KEY("Model_ID" AUTOINCREMENT)
);
COMMIT;
