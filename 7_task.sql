CREATE PROCEDURE GetTopCoaches
AS
BEGIN
    CREATE TABLE #CoachRatings (
        CoachId INT,
        RatingSum INT
    )

    DECLARE @CompetitionIds TABLE (Id INT)
    INSERT INTO @CompetitionIds
    SELECT CompetitionId FROM Competition

    DECLARE @Styles TABLE (Style VARCHAR(50))
    INSERT INTO @Styles
    SELECT DISTINCT Style FROM Result

    DECLARE @Distances TABLE (Distance INT)
    INSERT INTO @Distances
    SELECT DISTINCT Distanse FROM Result

    DECLARE @CoachIds TABLE (Id INT)
    INSERT INTO @CoachIds
    SELECT CoachId FROM Coach

    DECLARE @CompetitionId INT
    DECLARE @Style VARCHAR(50)
    DECLARE @Distance INT
    DECLARE @SwimmerId INT
    DECLARE @Place INT
    DECLARE @IdCoach INT
    DECLARE @Element INT

    DECLARE competition_cursor CURSOR FOR
    SELECT Id, Style, Distance FROM @CompetitionIds, @Styles, @Distances

    OPEN competition_cursor
    FETCH NEXT FROM competition_cursor INTO @CompetitionId, @Style, @Distance

    WHILE @@FETCH_STATUS = 0
    BEGIN
        DECLARE swimmer_cursor CURSOR FOR
        SELECT TOP 3 SwimmerId
        FROM Result
        WHERE Distanse = @Distance AND Style = @Style AND CompetitionId = @CompetitionId
        ORDER BY DeclaredTime ASC

        OPEN swimmer_cursor
        FETCH NEXT FROM swimmer_cursor INTO @SwimmerId

        SET @Place = 0

        WHILE @@FETCH_STATUS = 0
        BEGIN
            SELECT @IdCoach = CoachId
            FROM Swimmer
            WHERE SwimmerId = @SwimmerId

            SELECT @Element = COALESCE((SELECT RatingSum FROM #CoachRatings WHERE CoachId = @IdCoach), 0)
            SET @Element = @Element + (3 - @Place)

            IF EXISTS (SELECT 1 FROM #CoachRatings WHERE CoachId = @IdCoach)
            BEGIN
                UPDATE #CoachRatings SET RatingSum = @Element WHERE CoachId = @IdCoach
            END
            ELSE
            BEGIN
                INSERT INTO #CoachRatings (CoachId, RatingSum) VALUES (@IdCoach, @Element)
            END

            SET @Place = @Place + 1

            FETCH NEXT FROM swimmer_cursor INTO @SwimmerId
        END

        CLOSE swimmer_cursor
        DEALLOCATE swimmer_cursor

        FETCH NEXT FROM competition_cursor INTO @CompetitionId, @Style, @Distance
    END

    CLOSE competition_cursor
    DEALLOCATE competition_cursor

    SELECT TOP 10 c.FirstName + ' ' + c.LastName AS Coach, cr.RatingSum
    FROM Coach c
    INNER JOIN #CoachRatings cr ON c.CoachId = cr.CoachId
    ORDER BY cr.RatingSum DESC

    DROP TABLE #CoachRatings
END
