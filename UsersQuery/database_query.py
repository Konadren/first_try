from UsersPreferedDates.dates import start_date, end_date

commit_query = ('SELECT Comeets.ID, Comeets.PersonId, Comeets.Date, Comeets.ComeetMessage, Persons.Name, '
                'Persons.LastName FROM Comeets JOIN Persons ON Comeets.PersonId = Persons.ID')

crunches_query_1 = ("SELECT DISTINCT work_hours.PersonId, Persons.Name, Persons.LastName FROM work_hours JOIN Persons "
                   "ON work_hours.PersonId = Persons.ID")

crunches_query_2 = (f"SELECT Date, Hours_worked FROM work_hours WHERE PersonId = ? AND Date BETWEEN '{start_date}' AND "
            f"'{end_date}'")

messages_query = (f"SELECT Date, Amount FROM Messages WHERE PersonId = ? AND Date"
                  f" BETWEEN '{start_date}' AND '{end_date}'")

tasks_query_1 = ("SELECT DISTINCT PersonId FROM TasksChanges")

tasks_query_2 = (f"SELECT Date, Amount FROM TasksChanges WHERE PersonId = ? AND Date"
                 f" BETWEEN '{start_date}' AND '{end_date}'")

