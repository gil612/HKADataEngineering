USE DataCubeProductConsumer
GO

SELECT ProductKey, CustomerKey, SUM(SalesAmount) as SumSalesAmount
FROM SalesAmountFact
GROUP BY ROLLUP(ProductKey, CustomerKey)
GO
