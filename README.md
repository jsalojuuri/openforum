# Open Forum - Keskustelufoorumi aiheelle kuin aiheelle

Open Forumille rekisteröityneet ja kirjautuneet käyttäjät voivat julkaista kirjoituksia ja kommentoida omia ja toisten kirjoituksia erilaisilla foorumeilla. Omia kirjoituksia, kommentteja ja käyttäjätietoja voi muokata jälkikäteen. Vain pääkäyttäjät voivat luoda ja muokata foorumeita. Katso tarkemmin [käyttötapausten dokumentaatiosta](./documentation/usecases.txt).


## Asennusohje

1. Kloonaa repositorio koneellesi komennolla `git clone git@github.com:jsalojuuri/openforum.git` tai lataa [.zip-tiedosto](https://github.com/jsalojuuri/openforum/archive/master.zip).
2. Sovellus on toteutettu Python 3:lla. Voit tarvittaessa ladata sen [täältä](https://www.python.org/downloads/).
3. Siirry sovelluskansioon ja asenna Python-virtuaaliympäristö komennolla `python3 -m venv venv`
4. Aktivoi seuraavaksi virtuaaliympäristö komennolla `source venv/bin/activate`.
5. Asenna virtuaaliympäristöön vaadittavat lisäosat komennolla `pip install -r requirements.txt`.
6. Käynnistä sovellus komennolla `python3 run.py`  
7. Avaa sovellus selaimessasi komennolla `localhost:5000`


## Käyttöohje

* Helpoiten pääset liikkeelle rekisteröimällä uuden käyttäjän sovellukseen rekisteröintilomakkeen avulla ja kirjaumalla palveluun kirjautumislomakkeella. Linkit näihin löydät sovelluksen päänavigaatiosta. Vaihtoehtoisesti luo uusi käyttäjä suoraan sovelluksen tietokantaan tauluun Account. Jos käytät kehitysympäristönä VSCodea, suosittelen asentamaan SQLite Explorer lisäosan, jolla tietokannan muokkaus sujuu näppärästi. Admin-tason käytäjän luominen onnistuu vain suoralla tietokantainjektiolla.
* Ylläpitäjän on luotava palveluun aluksi ainakin yksi foorumi. Siirry foorumeiden hallintaan päänavigaatiosta valitsemalla 'Ylläpito'. Kun foorumi on luotu, pääsevät kaikki käyttäjät valitsemaan sen palvelun sisäänkirjautumisen jälkeiseltä sivulta
* Valitse foorumi ja lisää kirjoitus tai kommentoi muita kirjoituksia. Voit muokata ja poistaa omia kirjoituksiasi ja kommenttejasi. 
* Kaikki käyttäjät voivat siirtyä omille sivuille päänavigaation linkillä 'Omat sivut'. Omilla sivuilla voi muokata omia käyttätietoja sekä poistaa tai muokata omia kirjoituksia ja kommentteja.
* Kirjaudu palvelusta ulos päänavigaation 'Kirjaudu ulos' linkillä.  


## Testisovellus Herokussa

Voit testata sovellusta [Herokussa](http://tsoha-open-forum.herokuapp.com) joko käyttämällä oheisia testitunnuksia tai luomalla oman käyttäjän. Voit vapaasti lisätä, poistaa ja muokata sovelluksen sisältöä.

Kalle Käyttäjä (peruskäyttäjän oikeudet):
* käyttäjätunnus: user
* salasana: user

Peruskäyttäjänä voit lisätä, poistaa ja muokata kirjoituksia ja kommentteja esiluoduille foorumeille ja päivittää omia käyttäjätietojasi.

Ylläpitäjä (ylläpitäjän oikeudet):
* käyttäjätunnus: admin
* salasana: admin

Ylläpitäjänä voit edellisten lisäksi luoda, poistaa ja muokata foorumeita.


## Linkit

* [Projekti Herokussa](http://tsoha-open-forum.herokuapp.com)
* [Kuvaus keskeisimmistä käyttötapauksista](./documentation/usecases.txt)
* [Tietokantakaavio](./documentation/database_schema.JPG)







