#This script will parse the hurricanes.html file into a sqlite3 database named hurricanes.db using beautifulsoup4

from bs4 import BeautifulSoup
import sqlite3

#open hurricanes.html, read it in and create soup object
with open("hurricanes.html", "r") as f:
    
    contents = f.read()

    soup = BeautifulSoup(contents)

#As all the table data is stored in table tags with the wikitable sortable jquery-tablesorter, pull all out and store them in a dataset.
tabledata = soup.find_all('table', class_="wikitable sortable jquery-tablesorter")

#remove the last object from the list as that table is not of the needed dataset
del tabledata[-1]

#set the arrays to take in the values
years = []
trop_storms = []
hurricanes = []
major_hurricanes = []
deaths = []
storms = []
notes = []
damages = []

#set table_year which will be used to differentiate the tables by year
table_year = 0

#take each table out of the tabledata
for table in tabledata:

#from that table just take out the td values
    data = table.find_all('td')

#find the first year from that table to set as table_year and use to determine how to pull the data
    try:
        table_year = int(table.td.a.string)
    except: 
        break

#iterate through the td data set for each grouping of tables by year
    for i in range(0, len(data)):

#if the table is from before 1900 it has 9 columns, so iterate through them and pull the data
        if table_year < 1900:
            if i%9 == 0:
                year = int(data[i].a.string)
                years.append(year)
            if i%9 == 2:
                trop_storm = data[i].string
                trop_storms.append(trop_storm)
            if i%9 == 3:
                hurricane = data[i].string
                hurricanes.append(hurricane)
            if i%9 == 4:
                major_hurricane = data[i].string
                major_hurricanes.append(major_hurricane)
            if i%9 == 5:
                death = data[i].string
                deaths.append(death)
            if i%9 == 6:
                #the strongest storm could be a string from a or from the td
                try:
                    storm = data[i].a.string
                except:
                    storm = data[i].string
                storms.append(storm)
            if i%9 == 8:
                note = data[i]
                notes.append(note)
                #since no damages exist til later tables just iterate with a null value
                damage = ""
                damages.append(damage)
#run through tables with the years before 1980. They have one more column to handle. Damages
        elif table_year < 1980:
            if i%10 == 0:
                year = int(data[i].a.string)
                years.append(year)
            if i%10 == 2:
                trop_storm = data[i].string
                trop_storms.append(trop_storm)
            if i%10 == 3:
                hurricane = data[i].string
                hurricanes.append(hurricane)
            if i%10 == 4:
                major_hurricane = data[i].string
                major_hurricanes.append(major_hurricane)
            if i%10 == 5:
                death = data[i].string
                deaths.append(death)
            if i%10 == 6:
                damage = data[i].string
                damages.append(damage)
            if i%10 == 7:
                try:
                    storm = data[i].a.string
                except:
                    storm = data[i].string
                storms.append(storm)
            if i%10 == 9:
                note = data[i]
                notes.append(note)
#grab the remaining tables. The two decades in the 2000s have a total row so skip that by seeing if it contains a b string which only exists in the totals rows
        else:
            try:
                data[i].b.string
            except:
                if i%11 == 0:
                    year = int(data[i].a.string)
                    years.append(year)
                if i%11 == 3:
                    trop_storm = data[i].string
                    trop_storms.append(trop_storm)
                if i%11 == 4:
                    hurricane = data[i].string
                    hurricanes.append(hurricane)
                if i%11 == 5:
                    major_hurricane = data[i].string
                    major_hurricanes.append(major_hurricane)
                if i%11 == 6:
                    death = data[i].string
                    deaths.append(death)
                if i%11 == 7:
                    damage = data[i].string
                    damages.append(damage)
                if i%11 == 8:
                    try:
                        storm = data[i].a.string
                    except:
                        storm = data[i].string
                    storms.append(storm)
                if i%11 == 10:
                    note = data[i]
                    notes.append(note)

#remove the last value of storms as it contains an unneeded value
del storms[-1]

#create connection to the database file. It must be in the same directory as this file being run.
conn = sqlite3.connect("hurricanes.db")
c = conn.cursor()

#import all data into the database

for i in range(0, len(years)):
    sql = '''INSERT INTO atlantic_hurricanes (year) VALUES (?)'''
    c.execute(sql, (years[i],))

for i in range(0, len(trop_storms)):
    sql = '''UPDATE atlantic_hurricanes SET tropical_storms=? WHERE year=?'''
    c.execute(sql, (trop_storms[i],years[i],))

for i in range(0, len(hurricanes)):
    sql = '''UPDATE atlantic_hurricanes SET hurricanes=? WHERE year=?'''
    c.execute(sql, (hurricanes[i],years[i],))

for i in range(0, len(major_hurricanes)):
    sql = '''UPDATE atlantic_hurricanes SET major_hurricanes=? WHERE year=?'''
    c.execute(sql, (major_hurricanes[i],years[i],))

for i in range(0, len(deaths)):
    sql = '''UPDATE atlantic_hurricanes SET deaths=? WHERE year=?'''
    c.execute(sql, (deaths[i],years[i],))

for i in range(0, len(storms)):
    sql = '''UPDATE atlantic_hurricanes SET notes=? WHERE year=?'''
    c.execute(sql, (storms[i],years[i],))

for i in range(0, len(damages)):
    sql = '''UPDATE atlantic_hurricanes SET damage=? WHERE year=?'''
    c.execute(sql, (damages[i],years[i],))

#commit the changes and close the connection
conn.commit()
conn.close()
