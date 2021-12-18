USE DataCubeWithYear
GO

SELECT ProductKey, [Year], [Month], SalesAmount, AVG(SalesAmount)
OVER(PARTITION BY ProductKey ORDER BY [Year], [Month]
ROWS 2 PRECEDING) AS MovAvgFROM SalesAmountFact
