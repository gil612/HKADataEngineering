USE DataCubeWithYear
GO

SELECT [Name], [Year], [Month], SalesAmount,
SUM(SalesAmount) OVER(PARTITION BY S.ProductKey, [Year] ORDER BY [Month]
ROWS UNBOUNDED PRECEDING) AS YTD
FROM SalesAmountFact S, Product P
WHERE S.ProductKey=P.ProductKey
