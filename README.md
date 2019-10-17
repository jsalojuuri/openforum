# Open Forum - Keskustelufoorumi aiheelle kuin aiheelle

Open Forumille rekisteröityneet ja kirjautuneet käyttäjät voivat julkaista kirjoituksia ja kommentoida omia ja toisten kirjoituksia erilaisilla foorumeilla. Omia kirjoituksia, kommentteja ja käyttäjätietoja voi muokata jälkikäteen. Vain pääkäyttäjät voivat luoda ja muokata foorumeita. Katso tarkemmin [käyttötapausten dokumentaatiosta](./documentation/usecases.MD).


## Asennusohje

### Asentaminen omalle koneelle

1. Kloonaa repositorio koneellesi komennolla `git clone git@github.com:jsalojuuri/openforum.git` tai lataa [.zip-tiedosto](https://github.com/jsalojuuri/openforum/archive/master.zip).
2. Sovellus on toteutettu Python 3:lla. Voit tarvittaessa ladata sen [täältä](https://www.python.org/downloads/).
3. Siirry sovelluskansioon ja asenna Python-virtuaaliympäristö komennolla `python3 -m venv venv`
4. Aktivoi seuraavaksi virtuaaliympäristö komennolla `source venv/bin/activate`.
5. Asenna virtuaaliympäristöön vaadittavat lisäosat komennolla `pip install -r requirements.txt`.
6. Käynnistä sovellus komennolla `python3 run.py`  
7. Avaa sovellus selaimessasi komennolla `localhost:5000`

### Asentaminen Herokun pilvipalveluun Git:n avulla

Huom! Tässä ohjeessa oletetaan, että käytät versiohallintaan Git:ä, jonka voit tarvittaessa ladata [täältä](https://git-scm.com/downloads). 
Huom! Sovellus on konfiguroitu tiedostossa `__init__.py` käyttämään Heroku-ympäristössä PostgreSQL-tietokantaa kehitysympäristön SQLite-tietokannan sijaan. Voit huoletta asentaa sovelluksen nykyisen version Herokuun, mutta ota huomioon sovellusta mahdollisesti kehittäessäsi, että joudut testaamaan tietokantakyselyiden toimivuuden kehitysympäristön lisäksi myös Herokussa.

1. Luo ensin ilmainen tili Herokuun [täältä](https://signup.heroku.com/) ja lataa käyttöösi [Herokun työvälineet komentoriville](https://devcenter.heroku.com/articles/heroku-cli)
2. Aktivoi virtuaaliympäristö komennolla `source venv/bin/activate` 
3. Tarkista projektin riippuvuudet komennolla `cat requirements.txt`. Tarkista, että riippuvuuksien joukosta löytyy Herokun vaatima web-palvelin Gunicorn, tarvittaessa asenna se sovellukseen komennolla `pip install gunicorn`. Listalta ei saisi löytyä riippuvuutta pkg-resources, poista se tarvittaessa listalta muokkaamalla resources.txt tiedostoa. Jäädytä lopuksi sovelluksen riippuvuudet komennolla `pip freeze`
4. Projektille on luotu Herokun vaatima Procfile sovelluskansion juureen, jonka oletusasetuksena on `web: gunicorn --preload --workers 1 run:app`. Procfile sisältää Herokun tarvitsemat ohjeet sovelluksen käynnistämiseen. Muokkaa tiedostoa, jos haluat muuttaa sovelluksen käynnistyslogiikkaa Herokussa, ohjeita muokkaamiseen löydät [Herokun ohjesivuilta](https://devcenter.heroku.com/articles/procfile)
5. Luo sovellukselle paikka Herokuun komennolla `heroku create sovelluksen-nimi`, vaihda *sovelluksen-nimi* haluamaksesi nimeksi. Voit myös käyttää komentoa `heroku create`, jolloin Heroku antaa sovellukselle satunnaisen nimen.
6. Lisää versionhallintaan tieto Herokusta komennolla `git remote add heroku https://git.heroku.com/sovelluksen-nimi.git`, vaihda *sovelluksen-nimi* edellisessä kohdassa luomaasi nimeen.
7. Lisää muutokset versionhallintaan komennolla `git add .`, tee muutoksista commit esim. komennolla `git commit -m "Sovellus Herokuun"`ja puske lopuksi Git-repositoriosi Herokuun komennolla `git push heroku master`. Heroku asentaa automaattisesti puskemastasi repositoriosta sovelluksen palvelimelle, joka on tarkastelavissa osoitteessa https://sovelluksen-nimi.herokuapp.com.

Huom! Jos teet paikallisen sovelluksen tietokantatauluihin muutoksia ja viet muutokset versiohallinnan kautta Herokuun, joudut resetoimaan ensin PostgreSQL-tietokannan Herokusta ennen muutosten puskemista Herokuun komennolla `heroku restart; heroku pg:reset DATABASE`. Täältä löydät lisää ohjeita [Herokun tietokannan resetoimiseen](https://gist.github.com/zulhfreelancer/ea140d8ef9292fa9165e). Erityisesti ongelmatapauksissa Herokun logeja kannattaat tarkastella komentoriviltä komennolla `heroku logs -t`, jolla näet login loppupään (tail).

Huom! Sovelluksen riippuvuuksiin on asennettu psycopg2, jolla voit käyttää Herokun PostgreSQL:ää komentoriviltä. Sovellukselle on viety tieto Herokusta komennolla `heroku config:set HEROKU=1`. Voit tarkastella Herokun käyttämää tietokantaa kirjautumalla siihen komentoriviltä komennolla `heroku pg:psql`. Esim. komennolla `\dt` näet tietokannan käytössä olevat relaatiot. Tätä kautta voi myös lisätä tietokantaan käyttäjän, jolla on ylläpitäjän oikeudet esim. komennolla `INSERT INTO account (name, username, password, role) VALUES ('Ylläpitäjä', 'admin', 'admin', 'admin');`. Huomaa, että muuttujan `role` arvon on oltava `admin`, jotta käyttäjällä on ylläpitäjän oikeudet ja pääsy Open Forumin Ylläpito-paneeliin. Kaikki sovelluksen rekisteröitymislomakkeen avulla luotavat käyttäjät saavat automaattisesti roolikseen `user`, jonka voi muuttaa vain psycopg2:n avulla.

Huom! Jos käytät Githubia, voit halutessasi ottaa käyttöön [Herokun GitHub-integraation](https://devcenter.heroku.com/articles/github-integration). Tällöin sovellusta ei päivitetä itse Herokuun, vaan Heroku hakee käyttöön automaattisesti kaikki GitHubiin talletetut päivitykset. 

## Käyttöohje

* Helpoiten pääset liikkeelle rekisteröimällä uuden käyttäjän sovellukseen rekisteröintilomakkeen avulla ja kirjaumalla palveluun kirjautumislomakkeella. Linkit näihin löydät sovelluksen päänavigaatiosta. Vaihtoehtoisesti luo uusi käyttäjä suoraan sovelluksen tietokantaan tauluun Account. Jos käytät kehitysympäristönä VSCodea, suosittelen asentamaan SQLite Explorer lisäosan, jolla tietokannan muokkaus sujuu näppärästi. Admin-tason käyttäjän luominen onnistuu vain suoralla tietokantainjektiolla.
* Ylläpitäjän on luotava palveluun aluksi ainakin yksi foorumi. Siirry foorumeiden hallintaan päänavigaatiosta valitsemalla 'Ylläpito'. Kun foorumi on luotu, pääsevät kaikki käyttäjät valitsemaan sen palvelun sisäänkirjautumisen jälkeiseltä sivulta
* Valitse foorumi ja lisää kirjoitus tai kommentoi muita kirjoituksia. 
* Kaikki käyttäjät voivat siirtyä omalle sivulle päänavigaation linkillä 'Omat sivut'. Omilla sivuilla voi muokata omia käyttätietoja sekä poistaa tai muokata omia kirjoituksia ja kommentteja.
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

* [Sovelluksen käyttötapaukset, rajoitteet ja jatkokehitys](./documentation/usecases.MD)
* [Tietokantakaavio](./documentation/database_schema.JPG)
* [Tietokannan CREATE TABLE komennot](./documentation/database_create_table_commands.MD)
* [Projekti Herokussa](http://tsoha-open-forum.herokuapp.com)







