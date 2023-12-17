USE SwimCompetitions2021;

SELECT s.FirstName, s.LastName, s.CoachId, r.DeclaredTime, r.Distanse, r.Style, r.CompetitionId, CONCAT(c.FirstName, ' ', c.LastName) AS Coach, c.GradeTitle
FROM Swimmer AS s
JOIN Result AS r ON s.SwimmerId = r.SwimmerId
JOIN Coach AS c ON s.CoachId = c.CoachId;
