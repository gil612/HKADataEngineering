USE DataCubeWithYear
GO

INSERT INTO [SalesAmountFact] (ProductKey,
CustomerKey,SalesAmount,[Year],[Month])
VALUES
(1,1,100,2011,10),
(1,1,50,2011,11),
(1,2,55,2011,11),
(1,1,100,2011,12)
GO

INSERT INTO [SalesAmountFact] (ProductKey,
CustomerKey,SalesAmount,[Year],[Month])
VALUES
(2,1,60,2011,12),
(2,1,40,2012,1),
(2,1,70,2012,2),
(3,1,30,2012,1),
(3,1,50,2012,2),
(3,1,40,2012,3)
GO
