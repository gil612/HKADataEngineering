USE DataCubeProductConsumer
GO

CREATE TABLE [SalesAmountFact](
[SalesAmountKey][bigint] IDENTITY(1,1) NOT NULL,
[ProductKey][int] NOT NULL,
[CustomerKey][int] NOT NULL,
[SalesAmount][int] NOT NULL,
CONSTRAINT [SalesAmountKey] PRIMARY KEY CLUSTERED 
(
[SalesAmountKey] ASC
)
)

ALTER TABLE [SalesAmountFact]  WITH CHECK ADD  CONSTRAINT [FK_SalesAmountFact_To_Customer_Key_Dimension_Customer] FOREIGN KEY([CustomerKey])
REFERENCES [Customer] ([CustomerKey])
GO

ALTER TABLE [SalesAmountFact] CHECK CONSTRAINT [FK_SalesAmountFact_To_Customer_Key_Dimension_Customer]
GO

ALTER TABLE [SalesAmountFact]  WITH CHECK ADD  CONSTRAINT [FK_SalesAmountFact_To_Product_Key_Dimension_Product] FOREIGN KEY([ProductKey])
REFERENCES [Product] ([ProductKey])
GO

ALTER TABLE [SalesAmountFact] CHECK CONSTRAINT [FK_SalesAmountFact_To_Product_Key_Dimension_Product]
GO