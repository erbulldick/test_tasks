import pyodbc

class SwimCompetitions:
    def __init__(self):
        self.connection = self.connect_db()

    def connect_db(self):
        connection_to_db = pyodbc.connect(
            r'Driver={SQL Server};Server={};Database=SwimCompetitions2021;Trusted_Connection=yes;')
        return connection_to_db

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

    def get_coach(self):
        with self.connection.cursor() as cursor:
            sql = "SELECT CoachId, FirstName, LastName FROM Coach"
            cursor.execute(sql)
            value = cursor.fetchall()
        lst_coach = {i[0]: 0 for i in value}

        return lst_coach

    def get_id_swimmer(self, lst_distance, lst_style, lst_id_competition):
        lst_coach = self.get_coach()

        for id_competition in lst_id_competition:
            for style in lst_style:
                for distance in lst_distance:
                    with self.connection.cursor() as cursor:
                        sql1 = f"SELECT TOP 3 DeclaredTime, SwimmerId FROM Result" \
                               f" WHERE Distanse = {distance} and Style = '{style}' and CompetitionId = {id_competition}  ORDER BY DeclaredTime ASC"
                        cursor.execute(sql1)
                        values1 = cursor.fetchall()
                    for i in values1:
                        with self.connection.cursor() as cursor:
                            for place, time in enumerate(i):
                                sql = f"SELECT CoachId FROM Swimmer" \
                                       f" WHERE SwimmerId = '{i[1]}'"
                                cursor.execute(sql)
                                id_coach = cursor.fetchone()
                                element = lst_coach.get(id_coach[0], 0)
                                if place == 0:
                                    element += 3
                                elif place == 1:
                                    element += 2
                                elif place == 2:
                                    element += 1
                                lst_coach[id_coach[0]] = element

        sorted_dict = dict(sorted(lst_coach.items(), key=lambda x: x[1], reverse=True))
        first_ten_values = dict(list(sorted_dict.items())[:10])
        with self.connection.cursor() as cursor:
            sql = f"SELECT CoachId, FirstName, LastName FROM Coach WHERE CoachId IN ({', '.join(str(key) for key in first_ten_values)})"
            cursor.execute(sql)
            results = cursor.fetchall()

        first_ten_values = {f"{row[1]} {row[2]}": first_ten_values[key] for key, row in zip(first_ten_values, results)}

        return first_ten_values

    def main(self):
        lst_id_competition = self.get_year()
        lst_style, lst_distance = self.get_distanse_style()
        self.get_coach()
        print(self.get_id_swimmer(lst_distance, lst_style, lst_id_competition))


if __name__ == '__main__':
    swim_competitions = SwimCompetitions()
    swim_competitions.main()
