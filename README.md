# labra-raspi
## Saunavahti
Tämän projektityön tarkoitus on rakentaa järjestelmä, jolla tarkkaillaan saunan lämpenemistä. Saunan
lämpenemistä tarkkaillaan digitaalisen lämpötilamittarin avulla, sekä videokuvaa hyödyntäen.
Tarkoituksena olisi, että ohjelmalle asetettaisiin tavoitelämpötila, jonka saunan halutaan saavuttavan.
Lämpötilamittarilla tarkkaillaan ennen kaikkea nykyistä lämpötilaa, mutta myös sitä, miten nopeasti
sauna lämpiää. Jos sauna lämpenee tietyllä nopeudella, voidaan laskea koska saavutetaan haluttu
lämpötila. Videokuvaa käytetään siksi, että järjestelmä helpottaisi puusaunan lämmittämistä. Kaikki jotka
ovat puusaunaa lämmittäneet, tietävät miten turhauttavaa on, jos pesästä on tuli hiipunut.
Raspberry Pille tehtäisiin siis ohjelma, joka tarkkailee lämpötilaa ja sen kehitystä, sekä laskee kehityksen
perustella kauanko menee tavoitelämpötilan saavuttamiseen. Aika ajoin, esim kerran sekunnissa,
Raspberry Pihin kytketty kameramoduuli ottaisi kuvan tulipesän tilasta. Kuvaan yhdistettäisi
informaatio lämpötilasta, että sen kehityksestä. Kielenä käytetään Pythonia.

## Toteutus
### saunavahti.py
Tarkoituksena oli luoda erillinen verkkosivu, jota käytettäisiin hallinnoimaan saunavahtia internetin yli, koska kaikkihan nykypäivänä
pitää olla internetissä (Internet of Things is real!), mutta ajanpuutteen vuoksi tämänlaista loppukäyttäjän käyttöliittymää ei ole toteutettu.

AM2302 lämpötila- ja kosteusanturia käytetään mittaamaan lämpötilaa.
JSON-rajapintaa (rivit 101-129) käyttämällä voidaan aloittaa "saunan lämmitys" asettamalla tavoite lämpötila.
Saunan tavoite lämpötilan saavuttaminen lasketaan yksinkertaisella lineaarisella arviointi funktiolla (rivit 52-72), jossa 
nykyisen ajanhetken lämpötilasta lasketaan edellisen ajanhetken lämpötilan kulmakerroin ja sen mukaan arvioidaan saunan tavoite lämpötilan
saavutus ajanhetki. Katsoin, että monimutkaisemman talon sisäilman lämpenemis funktion käyttäminen tässä työssä olisi liian työlästä.

### saunavahti.py rajapinta kuvaus
<b>/ GET</b>
Palauttaa lämpötilan ja viimeisimmän kuvan.
<b>/ POST application/json</b>

POST - {"whendone":""}
RETURNS - data in json format

POST - {"start":"","target":"targettemperature"}
RETURNS - {"result":"saunavahti started, target temperature is targettemperature"} or {"result":"sauna is already active"}

POST - {"settarget":"targettemperature"}
RETURNS - {"result":"target temperature is now targettemperature"}

POST - {"led":"on"}
RETURNS - {"result":"led is on"}

POST - {"led":"off"}
RETURNS - {"result":"led is off"}

POST - {"picture":"take"}
RETURNS - {"result":"Picture taken"}
