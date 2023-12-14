import pyodbc
from datetime import datetime

class SwimCoach:
    def __init__(self):
        self.connection = self.connect_db()

    def connect_db(self):
        connection_to_db = pyodbc.connect(
            r'Driver={SQL Server};Server={};Database=SwimCompetitions2021;Trusted_Connection=yes;')
        return connection_to_db

    def format_date(self, date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%d')
        year = date_object.year
        return year

    def get_year(self):
        with self.connection.cursor() as cursor:
            sql = "SELECT CompetitionId FROM Competition"
            cursor.execute(sql)
            values = cursor.fetchall()
            lst_id_competition = []
            for i in values:
                lst_id_competition.append(i[0])

        return lst_id_competition

    def get_distanse_style(self):
        with self.connection.cursor() as cursor:
            sql = f"SELECT Distanse, Style FROM Result"
            cursor.execute(sql)
            values = cursor.fetchall()
        lst_1 = [i[0] for i in values]
        lst_2 = [i[1] for i in values]
        lst_style = set(lst_2)
        lst_distance = set(lst_1)

        return lst_style, lst_distance

    def get_id_swimmer(self, lst_distanse, lst_style, lst_id_competition):
        result_swimmer = []
        with self.connection.cursor() as cursor:
            for id_competition in lst_id_competition:
                for style in lst_style:
                    for distance in lst_distanse:
                        sql = f"SELECT TOP 3 R.DeclaredTime, S.FirstName, S.LastName, C.CompetitionName, C.StartDate " \
                              f"FROM Result R " \
                              f"JOIN Swimmer S ON R.SwimmerId = S.SwimmerId " \
                              f"JOIN Competition C ON R.CompetitionId = C.CompetitionId " \
                              f"WHERE R.Distanse = {distance} AND R.Style = '{style}' AND R.CompetitionId = {id_competition} " \
                              f"ORDER BY R.DeclaredTime ASC"
                        cursor.execute(sql)
                        values = cursor.fetchall()
                        for place, (declared_time, first_name, last_name, competition_name, start_date) in enumerate(
                                values):
                            result_swimmer.append({
                                'firstname': first_name,
                                'lastname': last_name,
                                'competition_name': competition_name,
                                'YearComp': self.format_date(start_date),
                                'WinnerComp': place + 1
                            })
        return result_swimmer

    def rang_coach(self):
        lst_id_competition = self.get_year()
        lst_style, lst_distance = self.get_distanse_style()
        return self.get_id_swimmer(lst_distance, lst_style, lst_id_competition)


if __name__ == '__main__':
    coach = SwimCoach()
    print(coach.rang_coach())
