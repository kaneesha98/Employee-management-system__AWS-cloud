import sqlite3

#Open database
conn = sqlite3.connect('main.db')
c=conn.cursor()

#Create table
c.execute('''DROP TABLE IF EXISTS employee''')
c.execute('''CREATE TABLE IF NOT EXISTS employee
		(Id INTEGER PRIMARY KEY AUTOINCREMENT, 
		email TEXT,
		password TEXT,
		designation TEXT,
		firstName TEXT,
		lastName TEXT,
		address1 TEXT,
		address2 TEXT,
		bloodgroup TEXT,
		city TEXT,
		state TEXT,
		country TEXT, 
		phone TEXT,
		start_date TEXT,
		dob TEXT
		)''')
c.execute('''INSERT or REPLACE INTO employee VALUES
(1, 'mukul@gmail.com', 'mukul123', 'Data Engineer', 'Mukul', 'Shah', 'Dhaval_Chowk_Newlines12',
'Paldi_society_Ahmd', 'AB+', 'Ahmedabad','Gujarat','India','0091654774', '23-05-2016', '14-11-1990'),
(2, 'parul23@gmail.com', 'parul09', 'Software Architect', 'Parul', 'Singh', 'Green_city_crossroads',
'42_Jumma_Masjid_Mandvi', 'O+', 'Mumbai', 'Maharashtra', 'India', '0091457721', '13-02-2011', '20-01-1987'),
(3, 'steve67@gmail.com', 'steve00', 'Production manager', 'Steve', 'Jobs', 'Palo_society_Richwoods',
'Highland_roads_Pier 39', 'O+', 'San Fransisco', 'California', 'USA', '0077412399', '12-01-2017', '12-12-1992'),
(4, 'robin@gmail.com', 'robinhood', 'Deputy manager', 'Robin', 'Stanley', 'Ardenwoods_near_Lucky_bookstore',
'Planckroads_Christwood_church', 'B+', 'LA', 'California', 'USA', '0034891109', '13-03-2018', '12-11-1991'),
(5, 'sana123@yahoo.com', 'sanakhan', 'Food Deputy head', 'Sana', 'Khan', 'Palki_society_Bunderpur',
'Jama_Masjid_New Delhi', 'AB-', 'New Delhi', 'New Delhi', 'India', '00912375634', '01-01-2013', '01-09-1994')''')
conn.commit()
c.close()
conn.close()
