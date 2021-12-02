USE DataCubeProductConsumer
GO

CREATE TABLE [Product](
[ProductKey] [int] IDENTITY(1,1) NOT NULL,
[Name] [nvarchar](50) NOT NULL,
CONSTRAINT [PK_Dimension_Product_Item] PRIMARY KEY CLUSTERED 
(
[ProductKey] ASC
) 
) 
GO