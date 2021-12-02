USE DataCubeProductConsumer
GO

SELECT ProductKey, CustomerKey, SUM(SalesAmount) as SumSalesAmount
FROM SalesAmountFact
GROUP BY CUBE(ProductKey, CustomerKey)
GO
