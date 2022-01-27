CREATE DATABASE HKA_UeKlausur_A18
GO

USE HKA_UeKlausur_A18
GO


-- Lieferant, Kunde, Herstellungsdatum, Produkttyp, Qualitätsstufe

-- Dimensionstabelle Lieferant
CREATE TABLE [Lieferant](
[LieferantKey] [int] IDENTITY(1,1) NOT NULL,
[Name] [nvarchar](50) NOT NULL,
[Adresse] [nvarchar](50) NOT NULL,
CONSTRAINT [PK_Dimension_Lieferant_Item] PRIMARY KEY CLUSTERED 
(
[LieferantKey] ASC
) 
) 
GO

-- Dimensionstabelle Kunde
CREATE TABLE [Kunde](
[KundeKey] [int] IDENTITY(1,1) NOT NULL,
[Name] [nvarchar](50) NOT NULL,
[Adresse] [nvarchar](50) NOT NULL,
CONSTRAINT [PK_Dimension_Kunde_Item] PRIMARY KEY CLUSTERED 
(
[KundeKey] ASC
) 
) 
GO

-- Dimensionstabelle Kunde
CREATE TABLE [Herstellungsdatum](
[HerstellungsdatumKey] [int] IDENTITY(1,1) NOT NULL,
[ProductionDate] [datetime2] NOT NULL,
CONSTRAINT [PK_Dimension_Herstellungsdatum_Item] PRIMARY KEY CLUSTERED 
(
[HerstellungsdatumKey] ASC
) 
) 
GO

-- Dimensionstabelle Produkttyp
CREATE TABLE [Produkttyp](
[ProdukttypKey] [int] IDENTITY(1,1) NOT NULL,
[Color] [nvarchar](50) NOT NULL,
[Size] [nvarchar](50) NOT NULL,
CONSTRAINT [PK_Dimension_Produkttyp_Item] PRIMARY KEY CLUSTERED 
(
[ProdukttypKey] ASC
) 
) 
GO

-- Dimensionstabelle Qualitätsstufe
CREATE TABLE [Qualitaetsstufe](
[QualitaetsstufeKey] [int] IDENTITY(1,1) NOT NULL,
[Quality] [int] NOT NULL,
CONSTRAINT [PK_DimensionQualitaetsstufe_Item] PRIMARY KEY CLUSTERED 
(
[QualitaetsstufeKey] ASC
) 
) 
GO

USE HKA_UeKlausur_A18
GO

-- drei assoziierte numerische Werte (Measures): Anzahl
-- produzierte Chargen, Produktionsdauer und produzierte Menge
-- (Masse in Tonnen)
CREATE TABLE [Fact](
[FactKey][bigint] IDENTITY(1,1) NOT NULL,
[LieferantKey][int] NOT NULL,
[KundeKey][int] NOT NULL,
[HerstellungsdatumKey][int] NOT NULL,
[ProdukttypKey][int] NOT NULL,
[QualitaetsstufeKey][int] NOT NULL,
[NoCharges][int] NOT NULL,
[Produktionsdauer][int] NOT NULL,
[Produzierte_Menge][int] NOT NULL,
[Year][int] NOT NULL,
[Quarter][int] NOT NULL,
[Month][int] NOT NULL,
CONSTRAINT [SalesAmountKey] PRIMARY KEY CLUSTERED 
(
[FactKey] ASC
)
)

-- add key for Lieferant
ALTER TABLE [Fact]  WITH CHECK ADD  CONSTRAINT [FK_Fact_To_Lieferant_Key_Dimension_Lieferant] FOREIGN KEY([LieferantKey])
REFERENCES [Lieferant] ([LieferantKey])
GO
ALTER TABLE [Fact] CHECK CONSTRAINT [FK_Fact_To_Lieferant_Key_Dimension_Lieferant]
GO

-- add key for Kunde
ALTER TABLE [Fact]  WITH CHECK ADD  CONSTRAINT [FK_Fact_To_Kunde_Key_Dimension_Kunde] FOREIGN KEY([KundeKey])
REFERENCES [Kunde] ([KundeKey])
GO
ALTER TABLE [Fact] CHECK CONSTRAINT [FK_Fact_To_Kunde_Key_Dimension_Kunde]
GO

-- add key for Herstellungsdatum
ALTER TABLE [Fact]  WITH CHECK ADD  CONSTRAINT [FK_Fact_To_Herstellung_Key_Dimension_Herstellungsdatum] FOREIGN KEY([HerstellungsdatumKey])
REFERENCES [Herstellungsdatum] ([HerstellungsdatumKey])
GO
ALTER TABLE [Fact] CHECK CONSTRAINT [FK_Fact_To_Herstellung_Key_Dimension_Herstellungsdatum]
GO

-- add key for Produkttyp
ALTER TABLE [Fact]  WITH CHECK ADD  CONSTRAINT [FK_Fact_To_Produkttyp_Key_Dimension_Produkttyp] FOREIGN KEY([ProdukttypKey])
REFERENCES [Produkttyp] ([ProdukttypKey])
GO
ALTER TABLE [Fact] CHECK CONSTRAINT [FK_Fact_To_Produkttyp_Key_Dimension_Produkttyp]
GO

-- add key for Qualitaetsstufe
ALTER TABLE [Fact]  WITH CHECK ADD  CONSTRAINT [FK_Fact_To_Qualitaetsstufe_Key_Dimension_Qualitaetsstufe] FOREIGN KEY([QualitaetsstufeKey])
REFERENCES [Qualitaetsstufe] ([QualitaetsstufeKey])
GO
ALTER TABLE [Fact] CHECK CONSTRAINT [FK_Fact_To_Qualitaetsstufe_Key_Dimension_Qualitaetsstufe]
GO

