USE HKA_UeKlausur_A18
GO

-- LieferantKey: 1 bis 4
-- KundeKey: 1 bis 4
-- HerstellungsdatumKey: 1 bis 24
-- ProdukttypKey: 1 bis 3
-- QualitaetsstufeKey: 1 bis 6
INSERT INTO [Fact] (LieferantKey,KundeKey,HerstellungsdatumKey,ProdukttypKey,QualitaetsstufeKey,
	NoCharges,Produktionsdauer,Produzierte_Menge,[Year],[Quarter],[Month])
VALUES(1,1,1,1,1,5,128,5,2021,1,1)
GO

INSERT INTO [Fact] (LieferantKey,KundeKey,ProdukttypKey,QualitaetsstufeKey,
	NoCharges,Produktionsdauer,Produzierte_Menge,[Year],[Quarter],[Month],HerstellungsdatumKey)
VALUES(1,2,1,1,5,128,5,2021,1,1,1),(2,2,1,1,5,256,8,2021,1,1,1),(2,2,3,1,5,512,15,2021,1,1,1),(2,2,3,5,5,420,45,2021,1,1,1)
	,(1,2,1,1,5,128,5,2019,1,1,4),(2,2,1,1,5,256,8,2019,1,1,4),(2,2,3,1,5,512,15,2019,1,1,4),(2,2,3,5,5,420,45,2019,1,1,4)
	,(1,2,1,1,5,1128,5,2019,1,2,5),(2,2,1,1,5,26,4,2019,1,2,5),(2,2,3,1,5,412,15,2019,1,2,5),(2,2,3,5,5,320,45,2019,1,2,5)
GO

INSERT INTO [Fact] (LieferantKey,KundeKey,ProdukttypKey,QualitaetsstufeKey,
	NoCharges,Produktionsdauer,Produzierte_Menge,[Year],[Quarter],[Month],HerstellungsdatumKey)
VALUES (1,2,1,1,5,128,5,2019,2,5,15),(1,1,1,1,5,228,45,2019,2,5,15)
GO