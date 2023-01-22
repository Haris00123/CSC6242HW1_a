########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv
# import os
# os.chdir('C:/Users/haris/Desktop/CSC_6242/HW1_a/Q2_Haris')
#################################################################################

## Change to False to disable Sample
SHOW = True

############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("csc6242hw1.db")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')
        
        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)",("1","test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())

######################################################################

class HW2_sql():
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
    
        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)
    ######################################################################
    ######################################################################

    # GTusername [0 points]
    def GTusername(self):
        gt_username = "mmasood30"
        return gt_username
    
    # Part a.i Create Tables [2 points]
    def part_ai_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_1_sql = "CREATE TABLE movies(id INTEGER, title TEXT, score REAL);"
        ######################################################################
        
        return self.execute_query(connection, part_ai_1_sql)

    def part_ai_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_2_sql = "CREATE TABLE movie_cast(movie_id INTEGER,cast_id INTEGER,cast_name TEXT,birthday TEXT,popularity REAL);"
        ######################################################################
        
        return self.execute_query(connection, part_ai_2_sql)
    
    # Part a.ii Import Data [2 points]
    def part_aii_1(self,connection,path):
        ############### CREATE IMPORT CODE BELOW ############################
        csv_read=csv.re
       ######################################################################

        cursor=connection.cursor()

        '''inserting into movies table'''
        query='''INSERT INTO movies(id,title,score) 
        VALUES (?,?,?);'''

        with open('data/movies.csv',newline='',encoding='UTF-8') as csvfile:
            reader=csv.reader(csvfile,delimiter=',')
            for row in reader:
                vals=(int(row[0]),row[1],float(row[2]))
                cursor.execute(query,vals)

        
        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
    
    def part_aii_2(self,connection, path):
        ############### CREATE IMPORT CODE BELOW ############################
        cursor=connection.cursor()

        '''Inserting into movie_cast'''
        query='''INSERT INTO movie_cast(movie_id,cast_id,cast_name,birthday,popularity) 
        VALUES (?,?,?,?,?);'''

        with open('data/movie_cast.csv',newline='',encoding='UTF-8') as csvfile:
            reader=csv.reader(csvfile,delimiter=',')
            for row in reader:
                vals=(int(row[0]),int(row[1]),row[2],row[3],float(row[4]))
                cursor.execute(query,vals)

        ######################################################################
        
        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part a.iii Vertical Database Partitioning [5 points]
    def part_aiii(self,connection):
        ############### EDIT CREATE TABLE SQL STATEMENT ###################################
        part_aiii_sql = "CREATE TABLE cast_bio(cast_id INTEGER,cast_name TEXT,birthday TEXT,popularity REAL);"
        ######################################################################
        
        self.execute_query(connection, part_aiii_sql)
        
        ############### CREATE IMPORT CODE BELOW ############################
        part_aiii_insert_sql = "INSERT INTO cast_bio(cast_id,cast_name,birthday,popularity) SELECT DISTINCT cast_id,cast_name,birthday,popularity FROM movie_cast"
        ######################################################################
        
        self.execute_query(connection, part_aiii_insert_sql)
        
        sql = "SELECT COUNT(cast_id) FROM cast_bio;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
       

    # Part b Create Indexes [1 points]
    def part_b_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_1_sql = "CREATE INDEX movie_index ON movies (id)"
        ######################################################################
        return self.execute_query(connection, part_b_1_sql)
    
    def part_b_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_2_sql = "CREATE INDEX cast_index ON movie_cast (cast_id)"
        ######################################################################
        return self.execute_query(connection, part_b_2_sql)
    
    def part_b_3(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_3_sql = "CREATE INDEX cast_bio_index ON cast_bio (cast_id)"
        ######################################################################
        return self.execute_query(connection, part_b_3_sql)
    
    # Part c Calculate a Proportion [3 points]
    def part_c(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_c_sql='''SELECT PRINTF("%.2f",CAST(SUM(selected) AS float)/CAST(COUNT(*) AS float)*100) AS field
                    FROM
                        (SELECT *,CASE
                            WHEN ((CAST(substr(birthday,-2) AS INTEGER) >=65) AND (CAST(substr(birthday,-2) AS INTEGER) <=85)) THEN 1
                            ELSE 0
                            END AS selected
                            FROM cast_bio) AS tmp'''
        ######################################################################
        cursor = connection.execute(part_c_sql)
        return cursor.fetchall()[0][0]

    # Part d Find the Most Prolific Actors [4 points]
    def part_d(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_d_sql = '''SELECT cast_name,COUNT(*) AS appearances 
        FROM movie_cast
        WHERE popularity>10
        GROUP BY cast_id,cast_name
        ORDER BY COUNT(*) DESC, cast_name ASC
        LIMIT 5'''
        ######################################################################
        cursor = connection.execute(part_d_sql)
        return cursor.fetchall()

    # Part e Find the Highest Scoring Movies With the Least Amount of Cast [4 points]
    def part_e(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_e_sql = '''SELECT title,PRINTF("%.2f",score),cast_num
                        FROM movies
                        LEFT JOIN
                        (SELECT movie_id,COUNT(*) AS cast_num
                        FROM movie_cast
                        GROUP BY movie_id) AS A
                        ON movies.id=A.movie_id
                        ORDER BY score DESC,cast_num ASC,title ASC
                        LIMIT 5
                        '''
        ######################################################################
        cursor = connection.execute(part_e_sql)
        return cursor.fetchall()
    
    # Part f Get High Scoring Actors [4 points]
    def part_f(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_f_sql = '''SELECT cast_id,cast_name,PRINTF("%.2f",AVG(score)) as average_score
FROM
(SELECT id,title,score,cast_id,cast_name
FROM movies
INNER JOIN movie_cast
ON movies.id=movie_cast.movie_id
WHERE score>=25) AS tmp
GROUP BY cast_id,cast_name
HAVING COUNT(id)>=3
ORDER BY average_score DESC,cast_name ASC
LIMIT 10'''

        ######################################################################
        cursor = connection.execute(part_f_sql)
        return cursor.fetchall()

    # Part g Creating Views [6 points]
    def part_g(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_sql = '''CREATE VIEW good_collaboration
                        AS
                        SELECT first_id AS cast_member_id1,second_id AS cast_member_id2,COUNT(movie_id) AS movie_count,AVG(score) AS average_movie_score
                        FROM
                        (SELECT A.movie_id,A.cast_id AS first_id,A.cast_name AS first_name,B.cast_id AS second_id,B.cast_name AS second_name
                        FROM movie_cast AS A
                        INNER JOIN movie_cast B
                        On A.movie_id=B.movie_id AND A.cast_id<B.cast_id
                        WHERE A.cast_id!=B.cast_id) AS tmp
                        INNER JOIN movies
                        ON tmp.movie_id=movies.id
                        GROUP BY first_id,first_name,second_id,second_name
                        HAVING movie_count>=3 and average_movie_score>=40'''
        ######################################################################
        return self.execute_query(connection, part_g_sql)
    
    def part_gi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_i_sql = '''SELECT id AS cast_id,cast_name,printf("%.2f",tmp.collaboration_score_raw) AS collaboration_score
                        FROM
                        (SELECT cast_member_id1 AS id,AVG(average_movie_score) as collaboration_score_raw FROM
                        (SELECT cast_member_id1,average_movie_score
                        FROM good_collaboration
                        UNION ALL
                        SELECT cast_member_id2 AS cast_member_id1,average_movie_score
                        FROM good_collaboration)
                        GROUP BY cast_member_id1
                        ORDER BY collaboration_score_raw DESC
                        LIMIT 5) AS tmp
                        LEFT JOIN cast_bio
                        ON tmp.id=cast_bio.cast_id
                        ORDER BY collaboration_score_raw DESC,cast_name ASC'''
        ######################################################################
        cursor = connection.execute(part_g_i_sql)
        return cursor.fetchall()
    
    # Part h FTS [4 points]
    def part_h(self,connection,path):
        ############### EDIT SQL STATEMENT ###################################
        part_h_sql ='''CREATE VIRTUAL TABLE movie_overview USING fts3(id INTEGER, overview TEXT);'''
        ######################################################################
        connection.execute(part_h_sql)
        ############### CREATE IMPORT CODE BELOW ############################

        cursor=connection.cursor()

        '''Inserting into movie_overview'''
        query='''INSERT INTO movie_overview(id,overview) 
        VALUES (?,?);'''

        with open('data/movie_overview.csv',newline='',encoding='UTF-8-sig') as csvfile:
            reader=csv.reader(csvfile,delimiter=',')
            for row in reader:
                vals=(int(row[0]),row[1])
                cursor.execute(query,vals)   
        ######################################################################
        sql = "SELECT COUNT(id) FROM movie_overview;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
        
    def part_hi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hi_sql = '''SELECT COUNT(*) FROM movie_overview WHERE overview MATCH 'fight'  '''
        ######################################################################
        cursor = connection.execute(part_hi_sql)
        return cursor.fetchall()[0][0]
    
    def part_hii(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hii_sql = "SELECT COUNT(*) FROM movie_overview WHERE overview MATCH 'space NEAR/5 program'"
        ######################################################################
        cursor = connection.execute(part_hii_sql)
        return cursor.fetchall()[0][0]


if __name__ == "__main__":
    
    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################s
    if SHOW == True:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    db = HW2_sql()
    try:
        conn = db.create_connection("Q2")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except:
        print("Error in Table Drops")

    try:
        print('\033[32m' + "part ai 1: " + '\033[m' + str(db.part_ai_1(conn)))
        print('\033[32m' + "part ai 2: " + '\033[m' + str(db.part_ai_2(conn)))
    except:
         print("Error in Part a.i")

    try:
        print('\033[32m' + "Row count for Movies Table: " + '\033[m' + str(db.part_aii_1(conn,"data/movies.csv")))
        print('\033[32m' + "Row count for Movie Cast Table: " + '\033[m' + str(db.part_aii_2(conn,"data/movie_cast.csv")))
    except:
        print("Error in part a.ii")

    try:
        print('\033[32m' + "Row count for Cast Bio Table: " + '\033[m' + str(db.part_aiii(conn)))
    except:
        print("Error in part a.iii")

    try:
        print('\033[32m' + "part b 1: " + '\033[m' + db.part_b_1(conn))
        print('\033[32m' + "part b 2: " + '\033[m' + db.part_b_2(conn))
        print('\033[32m' + "part b 3: " + '\033[m' + db.part_b_3(conn))
    except:
        print("Error in part b")

    try:
        print('\033[32m' + "part c: " + '\033[m' + str(db.part_c(conn)))
    except:
        print("Error in part c")

    try:
        print('\033[32m' + "part d: " + '\033[m')
        for line in db.part_d(conn):
            print(line[0],line[1])
    except:
        print("Error in part d")

    try:
        print('\033[32m' + "part e: " + '\033[m')
        for line in db.part_e(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part e")

    try:
        print('\033[32m' + "part f: " + '\033[m')
        for line in db.part_f(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part f")
    
    try:
        print('\033[32m' + "part g: " + '\033[m' + str(db.part_g(conn)))
        print('\033[32m' + "part g.i: " + '\033[m')
        for line in db.part_gi(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part g")

    try:   
        print('\033[32m' + "part h.i: " + '\033[m'+ str(db.part_h(conn,"data/movie_overview.csv")))
        print('\033[32m' + "Count h.ii: " + '\033[m' + str(db.part_hi(conn)))
        print('\033[32m' + "Count h.iii: " + '\033[m' + str(db.part_hii(conn)))
    except:
        print("Error in part h")

    conn.close()
    #################################################################################
    #################################################################################
  
