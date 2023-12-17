import pyodbc

class CoachAnalyzer:
    def __init__(self):
        self.connection_to_db = pyodbc.connect(
            r'Driver={SQL Server};Server={};Database=SwimCompetitions2021;Trusted_Connection=yes;')

    def get_top_coaches(self):
        lst_id_competition = self._get_competition_ids()
        values_style = self._get_distinct_values("Style")
        values_dist = self._get_distinct_values("Distanse")
        coach_ids = self._get_coach_ids()
        lst_coach = {coach_id: 0 for coach_id in coach_ids}

        for id_competition in lst_id_competition:
            for style in values_style:
                for distance in values_dist:
                    lst_id_swimmer = self._get_top_3_swimmers(id_competition, style, distance)
                    for place, (declared_time, swimmer_id) in enumerate(lst_id_swimmer):
                        id_coach = self._get_coach_id(swimmer_id)
                        element = lst_coach.get(id_coach, 0)
                        element += (3 - place)
                        lst_coach[id_coach] = element

        sorted_coaches = sorted(lst_coach.items(), key=lambda x: x[1], reverse=True)
        top_10_coaches = sorted_coaches[:10]
        result_list = self._get_coach_results(top_10_coaches)

        return result_list

    def _get_competition_ids(self):
        with self.connection_to_db.cursor() as cursor:
            cursor.execute("SELECT CompetitionId FROM Competition")
            return [i[0] for i in cursor.fetchall()]

    def _get_distinct_values(self, column_name):
        with self.connection_to_db.cursor() as cursor:
            cursor.execute(f"SELECT DISTINCT {column_name} FROM Result")
            return [i[0] for i in cursor.fetchall()]

    def _get_coach_ids(self):
        with self.connection_to_db.cursor() as cursor:
            cursor.execute("SELECT CoachId FROM Coach")
            return [i[0] for i in cursor.fetchall()]

    def _get_top_3_swimmers(self, competition_id, style, distance):
        with self.connection_to_db.cursor() as cursor:
            cursor.execute(
                """
                SELECT TOP 3 DeclaredTime, SwimmerId
                FROM Result
                WHERE Distanse = ? AND Style = ? AND CompetitionId = ?
                ORDER BY DeclaredTime ASC
                """,
                (distance, style, competition_id),
            )
            return cursor.fetchall()

    def _get_coach_id(self, swimmer_id):
        with self.connection_to_db.cursor() as cursor:
            cursor.execute(
                """
                SELECT CoachId
                FROM Swimmer
                WHERE SwimmerId = ?
                """,
                (swimmer_id,),
            )
            return cursor.fetchone()[0]

    def _get_coach_results(self, top_coaches):
        result_list = []
        with self.connection_to_db.cursor() as cursor:
            for key in top_coaches:
                cursor.execute("SELECT FirstName, LastName FROM Coach WHERE CoachId = ?", (key[0],))
                results = cursor.fetchone()
                result_list.append({
                    'Coach': f'{results[0]} {results[1]}',
                    'ratingSum': key[1]})
        return result_list

coach_analyzer = CoachAnalyzer()
print(coach_analyzer.get_top_coaches())
