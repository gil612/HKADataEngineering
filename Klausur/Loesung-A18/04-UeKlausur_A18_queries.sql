USE HKA_UeKlausur_A18
GO

-- Gesamte produzierte Menge nach Produkttyp im Jahr 2021
SELECT DISTINCT(ProdukttypKey), SUM(Produzierte_Menge)
OVER (PARTITION BY ProdukttypKey) AS SumProduzierteMenge
FROM Fact
WHERE Year=2021

--Year-to-date produzierte Menge nach Produkttyp in den Jahren
--    2019 bis 2021 aufgeschlüsselt nach Monaten
SELECT [Year],[Month],ProdukttypKey,Produzierte_Menge,
SUM(Produzierte_Menge) OVER (PARTITION BY ProdukttypKey,[Year]
ORDER BY [Month] ROWS UNBOUNDED PRECEDING) AS YTD
FROM Fact F
--optional können mit Hilfe des ProdukttypKeys die Eigenschaften des Produkts ausgegeben werden:
SELECT [Year],[Month],P.Color,P.Size,Produzierte_Menge,
SUM(Produzierte_Menge) OVER (PARTITION BY F.ProdukttypKey,[Year]
ORDER BY [Month] ROWS UNBOUNDED PRECEDING) AS YTD
FROM Fact F, Produkttyp P
WHERE F.ProdukttypKey=P.ProdukttypKey

--Produzierte Menge aufgeschlüsselt nach a) Quartalen,
--    b) Kunde, c) Produkttyp und d) Qualitätsstufe

SELECT [Quarter], KundeKey, ProdukttypKey, QualitaetsstufeKey, SUM(Produzierte_Menge) as
SumMenge
FROM Fact
GROUP BY ROLLUP([Quarter], KundeKey, ProdukttypKey, QualitaetsstufeKey)

-- Hierarchien beziehen sich auf die Zeit.
-- Jahr
-- Quartal
-- Monat