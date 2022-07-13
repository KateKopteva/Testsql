from prettytable import PrettyTable
import mysql.connector
from mysql.connector import Error

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    port='3306',
    database='python_test'
)

def execute_read_query(query):
    my_cursor = mydb.cursor()
    try:
        my_cursor.execute(query)
        result = my_cursor.fetchall()
        return result
    except Error as e:
        print('The error')


select_users = ("""SELECT bid.client_number AS client, 
                  SUM(event_value.outcome = "win") AS wins,
                  SUM(event_value.outcome = "lose") AS lose
                  FROM bid
                  JOIN event_value ON bid.play_id = event_value.play_id AND bid.coefficient = event_value.value
                  GROUP BY client""")

select_team = ("""SELECT least(home_team, away_team) AS A, 
		            greatest(home_team, away_team) AS B, 
		            COUNT(*)
                    FROM event_entity
                    GROUP BY A, B
                    HAVING COUNT(*) >= 1
                    ORDER BY A, B""")

users = execute_read_query(select_users)
teams = execute_read_query(select_team)

th = ['client_number', 'Побед', 'Поражений']
columns = len(th)
table_users = PrettyTable(th)
for user in users:
    table_users.add_row(user)
print(table_users)

th_2 = ['game', 'games_count']
columns = len(th_2)
table_teams = PrettyTable(th_2)
table_teams.align['game'] = 'l'
table_teams.align['games_count'] = 'r'
teams.sort(key=lambda x: x[2])
for team in teams:
    my_tuple = (team[0]+'-'+team[1], team[2])
    table_teams.add_row(my_tuple)
print(table_teams)
