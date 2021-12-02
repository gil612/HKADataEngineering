USE DataCubeProductConsumer
GO

CREATE TABLE [Customer](
[CustomerKey] [int] IDENTITY(1,1) NOT NULL,
[Customer] [nvarchar](50) NOT NULL,
CONSTRAINT [PK_Dimension_Customer] PRIMARY KEY CLUSTERED 
(
[CustomerKey] ASC
) 
) 
GO