CREATE PROCEDURE GetSwimmerRankings_2
AS
BEGIN
    USE SwimCompetitions2021
    DECLARE @lst_distance TABLE (Distance VARCHAR(50))
    DECLARE @lst_style TABLE (Style VARCHAR(50))
    DECLARE @result_swimmer TABLE (
        firstname VARCHAR(50),
        lastname VARCHAR(50),
        competition_name VARCHAR(50),
        YearComp DATE,
        WinnerComp INT
    )

    INSERT INTO @lst_distance (Distance)
    SELECT DISTINCT Distanse FROM Result

    INSERT INTO @lst_style (Style)
    SELECT DISTINCT Style FROM Result

    DECLARE @id_competition INT
    DECLARE @start_date DATE
    DECLARE @style VARCHAR(50)
    DECLARE @distance VARCHAR(50)

    DECLARE competition_cursor CURSOR FOR
    SELECT CompetitionId, StartDate FROM Competition

    OPEN competition_cursor
    FETCH NEXT FROM competition_cursor INTO @id_competition, @start_date

    WHILE @@FETCH_STATUS = 0
    BEGIN
        DECLARE style_cursor CURSOR FOR
        SELECT Style FROM @lst_style

        OPEN style_cursor
        FETCH NEXT FROM style_cursor INTO @style

        WHILE @@FETCH_STATUS = 0
        BEGIN
            DECLARE distance_cursor CURSOR FOR
            SELECT Distance FROM @lst_distance

            OPEN distance_cursor
            FETCH NEXT FROM distance_cursor INTO @distance

            WHILE @@FETCH_STATUS = 0
            BEGIN
                INSERT INTO @result_swimmer (firstname, lastname, competition_name, YearComp, WinnerComp)
                SELECT TOP 3 S.FirstName, S.LastName, C.CompetitionName, @start_date, ROW_NUMBER() OVER (ORDER BY R.DeclaredTime ASC)
                FROM Result R
                JOIN Swimmer S ON R.SwimmerId = S.SwimmerId
                JOIN Competition C ON R.CompetitionId = C.CompetitionId
                WHERE R.Distanse = @distance AND R.Style = @style AND R.CompetitionId = @id_competition
                ORDER BY R.DeclaredTime ASC

                FETCH NEXT FROM distance_cursor INTO @distance
            END

            CLOSE distance_cursor
            DEALLOCATE distance_cursor

            FETCH NEXT FROM style_cursor INTO @style
        END

        CLOSE style_cursor
        DEALLOCATE style_cursor

        FETCH NEXT FROM competition_cursor INTO @id_competition, @start_date
    END

    CLOSE competition_cursor
    DEALLOCATE competition_cursor

    SELECT * FROM @result_swimmer
END

EXEC GetSwimmerRankings_2;