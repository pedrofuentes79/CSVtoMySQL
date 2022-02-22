import mysql.connector
import csv
from utils import check_keywords, space_remover, quote_remover
#MySQL connector
#Take into account that the user must have privileges and the database must have been created beforehand
db = mysql.connector.connect(
    host="localhost",
    user="your_user",
    passwd="your_passwd",
    database="your_db")
c = db.cursor()



#CSV CONFIGURATION

filename = "Sample2000.csv"
tablename = filename[:-4]
column_names = []
column_1 = []
data_types = []
    
    
#get first row, which are the names of all the columns
with open(filename) as csvfile:
    #init file reader
    reader = csv.reader(csvfile, delimiter=",")
    #check the first row in the file to get all column names
    for row in reader:
        column_names.append(row)
        column_names = column_names[0]
        for x in range(len(column_names)):
            #reformat column names so they are correct and dont interfere with SQL syntax
            #check if this counts as prevention for sql injection
            column_names[x] = space_remover(column_names[x])
            column_names[x] = check_keywords(column_names[x])
        break 
    #get first column to check for the datatypes
    counter = 0
    for row in reader:
        if counter == 1:
            column_1.append(row)
            column_1 = column_1[0]
            break
        counter += 1   
    #check datatypes (this does not cover most datatypes, a feature to add in the future)
    for cell in column_1:
        if cell.isdigit():
            if int(cell) > 4294967295:
                data_types.append("BIGINT")
            else:
                data_types.append("INT")
        else:
            data_types.append("VARCHAR(255)")

#SQL EXECUTES
#create the table with only the first row of the csv file as column values
c.execute("USE maindb")
c.execute("CREATE TABLE %s (%s %s);" % (tablename, column_names[0], data_types[0]))

#add the other columns
for i in range(1, len(column_names)):
    c.execute("ALTER TABLE %s ADD COLUMN %s %s;" % (tablename, column_names[i], data_types[i]))

#READING CSV AND PARSING TO THE SQL DB
with open(filename) as csvfile:
    counter = 0
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        #This is for the reader to avoid writing the first row, which are the column names
        if counter < 1:
            counter +=1
        else:
            for m in range(len(row)):
                #if the cell value is an integer, 
                #format it so it is correct to be inserted into the db as an int
                if row[m].isdigit():
                    row[m] = int(row[m])
                else:
                    #Changes double quotes to single quotes so they do not interfere with sql syntax
                    row[m] = quote_remover(row[m])
            #COLUMN CONFIGURATION
            column_names_string = ""
            for n in range(len(column_names)-1):
                #Add the list elements with a comma to the string (up to the last one)
                column_names_string += column_names[n] + ", "
                #The last element must not have a comma after it, it would be a trailing comma otherwise
            column_names_string += column_names[-1]


            #FORMAT THE QUERY AND EXECUTE IT
                #This string format is for the queries to be somewhat like this:
                #(123098235, 'TALES_OF_SHIVA', 'Mark', 'mark', 0)
            arguments = "("
            for o in range(len(data_types)-1):
                if data_types[o] == "BIGINT" or data_types[o] == "INT":
                    arguments += "%s, " 
                else:
                    arguments += '''"%s", ''' 
            #This sepparated if statement is because the last query must not have a trailing comma
            #It also adds the last parentheses
            if data_types[-1] == "BIGINT"  or data_types[-1] == "INT":
                arguments += "%s);"
            else:
                arguments += '''"%s");'''
            #piecing strings together
            query = f"INSERT INTO {tablename} ({column_names_string}) VALUES "
            final_query = query + arguments
            c.execute(final_query % tuple(row))
db.commit()
db.close()