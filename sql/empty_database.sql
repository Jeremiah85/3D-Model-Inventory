BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "tblSource" (
	"Source_ID"	INTEGER UNIQUE,
	"Source_Name"	TEXT,
	"Source_Website"	TEXT,
	PRIMARY KEY("Source_ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "tblArtist" (
	"Artist_ID"	INTEGER UNIQUE,
	"Artist_Name"	TEXT,
	"Artist_Website"	TEXT,
	"Artist_Email"	TEXT,
	"Artist_Folder"	TEXT,
	PRIMARY KEY("Artist_ID" AUTOINCREMENT)
);
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
CREATE TABLE IF NOT EXISTS "tblSchema" (
	"label"	TEXT NOT NULL,
	"version"	INTEGER NOT NULL
);
INSERT INTO "tblSchema" ("label","version") VALUES ("current", 2);
COMMIT;
