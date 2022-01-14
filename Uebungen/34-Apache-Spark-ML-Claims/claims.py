# source: https://www.informatik-aktuell.de/entwicklung/methoden/einfuehrung-in-spark-ein-text-mining-projekt.html

from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id, concat_ws

claimsFile = "patent_claims_excerpt.csv"
# claimsFile = "patent_claims_excerpt2.csv"
# claimsFile = "patent_claims_fulltext.csv"
spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
# full text
claimsData = spark.read.text(claimsFile) # .cache()     
numAs = claimsData.filter(claimsData.value.contains('a')).count()
numBs = claimsData.filter(claimsData.value.contains('b')).count()
print("Lines with a: %i, lines with b: %i" % (numAs, numBs))
print(claimsData.head(2))


# select columns from csv file
# create a column with an id
claims_df=spark.read.csv(claimsFile,sep=',',header=True,quote='"') \
        .withColumn("id", monotonically_increasing_id()) \
        .drop("claim_no") \
        .drop("dependencies") \
        .drop("ind_flg") \
        .drop("appl_id")
print(claims_df.columns)
print(claims_df.count())
print(claims_df.head(3))

"""
Datenaufbereitung und Speichern
Im nächsten Schritt wollen wir den Text so aufbereiten, dass der Fließtext auf einzelne, normalisierte Worte reduziert wird.
Dafür verwenden wir zwei vorhandene Funktionen aus der MLlib-Library und zwei user-defined functions.
Ein Tokenizer trennt den gesamten Claims-Text zunächst in einzelne Worte,
getrennt an allen nicht-alphanumerischen Zeichen ("\W" in python regex-Syntax).
Viele davon sind aber zu häufig und unspezifisch (and, but, is, the, etc.) und
daher für unsere geplante Ähnlichkeitssuche nutzlos.
Wir entfernen diese sogenannten Stoppworte mit dem StopWordsRemover in MLlib.
"""
from pyspark.ml.feature import RegexTokenizer
tokenizer=RegexTokenizer(inputCol="claim_txt", outputCol="claimToken", pattern="\\W")
tok_df=tokenizer.transform(claims_df)

from pyspark.ml.feature import StopWordsRemover
sw_remover=StopWordsRemover(inputCol="claimToken", outputCol="claimNoStopWords")
swr_df=sw_remover.transform(tok_df)

"""
Zum Entfernen von Ziffern und Zahlen gibt es leider keine fertige Funktion,
also definieren wir unsere eigene. Um eine Funktion auf einer Spalte des DataFrames anzuwenden,
können wir user-defined functions (UDF) von SparkSQL nutzen.
Wie in vielen SQL-Umgebungen erweitern sie auch in SparkSQL den Funktionsumfang der angebotenen SQL-Funktionalität.
Wir wollen sie verwenden, um eine neue Spalte aus der Token-Spalte abzuleiten.
Dazu entwerfen wir erst eine Funktion remove_numbers()  in normaler Pythonsyntax,
die wir in eine UDF umwandeln und auf die Token-Spalte anwenden. Der Code dazu sieht folgendermaßen aus:
"""
import re
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType

def remove_numbers(s):
    return list(word for word in s if not re.compile(r'^\d+$').match(word))
remove_numbers_udf = udf(remove_numbers, ArrayType(StringType()))
nn_df = swr_df.withColumn("claimNoNumbers", remove_numbers_udf("claimNoStopWords"))

"""
Etwas komplizierter ist es, jedes Wort in eine Grundform zu überführen,
so dass etwa electronical, electronics und electronic als der gleiche Wortstamm erkannt werden.
Stemming: Stammformreduktion
Dafür verwenden wir einen Stemmer aus dem natural language toolkit nltk für Python.
Wie oben müssen wir wieder eine Pythonfunktion für das eigentliche Stemmen definieren und in eine UDF umwandeln.
Dann können wir unsere Funktion auf die inzwischen von Ziffern befreite Token-Spalte anwenden.
"""
from nltk.stem.porter import *

stemmer = PorterStemmer()

def stem(in_vec):
    out_vec = []
    for t in in_vec:
        t_stem = stemmer.stem(t)
        if len(t_stem) > 2:
            out_vec.append(t_stem)       
    return out_vec

stemmer_udf = udf(stem, ArrayType(StringType()))
stemmed_df = nn_df.withColumn("claimStemmed", stemmer_udf("claimNoNumbers"))

"""
An dieser Stelle können wir den Zwischenstand sichern und die aufbereiteten Patenttexte
auf die Festplatte schreiben.
Das geht ganz einfach, zum Beispiel können wir den DataFrame mit allen relevanten Spalten
im Parquet-Format speichern.
Parquet ist dabei das Standardformat für das Schreiben von Dateien.
Andere Optionen wie JSON, plain text oder auch JDBC stehen natürlich ebenso zur Verfügung.
Das Speichern ist natürlich auch eine Aktion, d. h. hier wird die komplette Berechnung
(Entstehungsgeschichte) durchgeführt und das Ergebnis "materialisiert"
"""
tosave_df=stemmed_df.select(["id", "claim_txt", "claimStemmed"])
#tosave_df.write.mode("overwrite").save("data/stemmeddataframe.parquet")

"""
Das Wiedereinlesen geht danach genauso einfach.
Mit df.show() überprüfen wir noch einmal, dass auch das Schema,
also die Spaltennamen der Spalten, wieder hergestellt wurden.
Operationen auf diesem neu eingelesenen DataFrame müssen nicht mehr die ursprüngliche
Lineage abarbeiten, sind also deutlich performanter.
"""

df=tosave_df

"""
Text Mining Basics – IDF und TF-IDF
Wir haben nun also jedem Patent eine Liste der darin vorkommenden gestemmten Worte
(der "Terme") zugeordnet. Der noch verbleibende Schritt ist,
ein Ähnlichkeitsmaß zwischen zwei Patenttexten zu definieren.
Ein häufiges Vorgehen beim Definieren eines Ähnlichkeitsmaßes besteht darin,
die Ausgangsobjekte in einen Euklidischen Vektorraum abzubilden,
da es in einem solchen viele Möglichkeiten gibt, Distanzen bzw. Ähnlichkeiten zu berechnen
(z. B. die Euklidische Distanz).
"""

from pyspark.ml.feature import CountVectorizer
from pyspark.ml.feature import Normalizer
from pyspark.ml.feature import IDF
vSize=1000 # Max size of the vocabulary.

cv = CountVectorizer(inputCol="claimStemmed", outputCol="claimTF", vocabSize=vSize)
cvModel = cv.fit(df)
tf_df = cvModel.transform(df)

normalizer = Normalizer(inputCol="claimTF", outputCol="claimTFN")
tfn_df = normalizer.transform(tf_df)

idf = IDF(inputCol="claimTFN", outputCol="IDF")

idfModel = idf.fit(tfn_df)
tfidf_df = idfModel.transform(tfn_df)

"""
Kosinus-Ähnlichkeit
"""
from pyspark.sql.types import FloatType

# Berechne die cosine-simliarity: dot product / product der L2-Norms
def csim(vec1, vec2):
    return vec1.dot(vec2)/(vec1.norm(2)*vec2.norm(2))

# Berechne die Ähnlichkeiten zu einem gegebenen Patent
def getSimilarities(df, id):
    patent = df.where("id == "+id)
    my_tfidf = patent.select("IDF").first().IDF
    csim_udf = udf(lambda x: round(float(csim(my_tfidf, x)),2))
    sim_df = df.withColumn("similarity", csim_udf("IDF"))
    return sim_df

"""
Suche nach ähnlichen Patenten
"""
from pyspark.sql.functions import desc

getSimilarities(tfidf_df, "10") \
    .select(["id", "similarity", "claim_txt"]) \
    .orderBy(desc("similarity")) \
    .show(4, truncate=100)

spark.stop()