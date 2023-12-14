import pyodbc


def connect_db():
    connection_to_db = pyodbc.connect(
        r'Driver={SQL Server};Server={};Database=SwimCompetitions2021;Trusted_Connection=yes;')
    return connection_to_db

def get_coach(connection):
    with connection.cursor() as cursor:
        sql = "SELECT CoachId FROM Coach"
        cursor.execute(sql)
        value = cursor.fetchall()
    return [i[0] for i in value]


def print_coach(connection):
    result = []
    with connection.cursor() as cursor:
        sql = "SELECT s.FirstName, s.LastName, s.CoachId, r.DeclaredTime, r.Distanse, r.Style, r.CompetitionId, c.FirstName, c.LastName, c.GradeTitle " \
              "FROM Swimmer AS s " \
              "JOIN Result AS r ON s.SwimmerId = r.SwimmerId " \
              "JOIN Coach AS c ON s.CoachId = c.CoachId"
        cursor.execute(sql)
        rows = cursor.fetchall()

    for row in rows:
        first_name, last_name, coach_id, declared_time, distance, style, competition_id, coach_first_name, coach_last_name, grade_title = row

        result.append(f"DeclaredTime: {declared_time}, distance: {distance}, style: {style}, "
                      f"SwimmerId: {row[0]}, CompetitionId: {competition_id}, "
                      f"CoachId: {coach_id}, first_name: {first_name}, last_name: {last_name}, "
                      f"grade_title: {grade_title}, coach: {coach_first_name} {coach_last_name}")

    return result



def main():
    conn = connect_db()
    print(print_coach(conn))


if __name__ == '__main__':
    main()