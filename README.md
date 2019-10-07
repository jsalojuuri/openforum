# Open Forum - Keskustelufoorumi aiheelle kuin aiheelle

Open Forumille rekisteröityneet ja kirjautuneet käyttäjät voivat julkaista kirjoituksia ja kommentoida omia ja toisten kirjoituksia erilaisilla foorumeilla. Omia kirjoituksia, kommentteja ja käyttäjätietoja voi muokata jälkikäteen. Vain pääkäyttäjät voivat luoda ja muokata foorumeita. Katso tarkemmin [käyttötapausten dokumentaatiosta](./documentation/usecases.txt).


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


## Sovelluksen rajoitteet ja jatkokehitys

Sovellus on kehitetty Helsingin Yliopiston kurssin Tietokantasovellus projektina syys-lokakuussa 2019. Kurssin aikana toteutettiin suurin osa kurssin alussa suunnitelluista käyttötapauksista ja sovellus on jo sellaisenaan toimiva pienen ryhmän keskustelufoorumiksi. Sovelluksesta puuttuu toistaiseksi työkalut foorumien ja kirjoitusten hakemiseen, eikä tietokantahakujen listauksia ole sivutettu sovelluksessa mitenkään. Haku- ja sivutustoiminnallisuuksien kehitys on lisätty [käyttötapauslistauksen jatkokehitysideoihin](./documentation/usecases.txt), jonka lisäksi käyn tässä vielä lyhyesti läpi ajatuksia näiden toteuttamiseksi:

* Hakutoiminnallisuus: tämän hetkisen tiedon perusteella toteutus kannattaisi tehdä Pythonin [Whoosh-kirjaston](https://whoosh.readthedocs.io/en/latest/intro.html) avulla. Whooshiin on olemassa myös [SQLAlchemy integraatio](https://flask-whooshee.readthedocs.io/en/latest/), joka oletettavasti nopeuttaisi toteutusta.
* Listausten sivutus: listauksia, kuten Open Forumiin luotuja foorumeita, foorumin kirjoituksia tai kirjoituksen kommentteja voi niputtaa esim. kymmenen esiintymän ryhmiin per sivu, mikä parantaisi sovelluksen käytettävyyttä sisällön määrän kasvaessa. Sivutuksen toteutukseen Flask-ympäristössä voi tutustua esim. [Miguel Grinbergin blogin avulla](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ix-pagination).


## Keskeisimmät käyttötapaukset ja niihin liittyvät SQL-kyselyt

Sovelluksen keskeisimmät käyttötapaukset ja jatkokehitysideat on listattu lyhyesti [täällä](./documentation/usecases.txt). Ohessa vielä SQL-kyselyt näkymäkohtaisesti:


### Rekisteröityminen ja kirjautuminen palveluun

* Rekisteröityminen



* Kirjautuminen



### Ylläpitäjän paneeli

* Tilastoja Open Forumista
```
SELECT 
    COUNT(DISTINCT Forum.id), 
    COUNT(DISTINCT Topic.id), 
    COUNT(DISTINCT Topicaccount.account_id), 
    COUNT(DISTINCT Comment.id) FROM Forum
    LEFT JOIN Topic ON Topic.forum_id = Forum.id
    LEFT JOIN Topicaccount ON Topicaccount.topic_id = Topic.id
    LEFT JOIN Comment ON Topic.id = Comment.topic_id
    ;
```
* Listaus ja tilastoja luoduista foorumeista
```
SELECT 
    Forum.id, 
    Forum.name, 
    Forum.description, 
    Forum.date_modified, 
    COUNT(DISTINCT Topic.id), 
    COUNT(DISTINCT Topicaccount.account_id), 
    COUNT(DISTINCT Comment.id) FROM Forum
    LEFT JOIN Topic ON Forum.id = Topic.forum_id
    LEFT JOIN Topicaccount ON Topic.id = Topicaccount.topic_id
    LEFT JOIN Comment ON Topic.id = Comment.topic_id
    GROUP BY Forum.id
    ;
```
* Yksittäisen foorumin tietojen haku lomakkeen validointia varten (? = Haettavan foorumin nimi)
```
SELECT 
    * FROM Forum
    WHERE Forum.name = ?
    ;
```
* Uuden foorumin luominen
```

```

### Listaus ja tilastointia palvelun kirjoituksista foorumeittain

### Kirjoitusten lisääminen, muokkaaminen ja poistaminen

### Käyttäjäprofiilin (käyttäjätietojen) muokkaus, omien kirjoitusten muokkaaminen ja poistaminen sekä käyttäjäkohtaisia tilastoja käyttäjän omilla sivuilla

### Foorumien lisääminen, muokkaus ja poistaminen sekä palvelun käytön tilastoja ylläpitäjän hallintapaneelissa

### Mahdollisuus kommentoida kirjoitusta

### Kommentin muokkaaminen ja poistaminen omalla sivulla

### Kirjoituskohtaisen tilastoinnin kehitys: kirjoituksen lukukerrat ja kuinka moni käyttäjä on nähnyt kirjoituksen


## Tietokantarakenteen kuvaus

Sovelluksen tietokanta on normalisoitu kolmanteen normaalimuotoon ja sen lopullinen tietokantarakenne vastaa oheista [tietokantakaaviota](./documentation/database_schema.JPG). Tietokannan CREATE TABLE -lauseet:

* Account-taulu

```
CREATE TABLE account (
        id INTEGER NOT NULL, 
        date_created DATETIME, 
        date_modified DATETIME, 
        name VARCHAR(144) NOT NULL, 
        username VARCHAR(144) NOT NULL, 
        password VARCHAR(144) NOT NULL, 
        role VARCHAR(10), 
        PRIMARY KEY (id)
)
```

* Forum-taulu

```
CREATE TABLE forum (
        id INTEGER NOT NULL, 
        date_created DATETIME, 
        date_modified DATETIME, 
        name VARCHAR(144) NOT NULL, 
        description VARCHAR(1000) NOT NULL, 
        PRIMARY KEY (id)
)
```

* Topic-taulu

```
CREATE TABLE topic (
        id INTEGER NOT NULL, 
        date_created DATETIME, 
        date_modified DATETIME, 
        title VARCHAR(144) NOT NULL, 
        bodytxt VARCHAR(1444) NOT NULL, 
        forum_id INTEGER NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(forum_id) REFERENCES forum (id)
)
```

* Comment-taulu

```
CREATE TABLE comment (
        id INTEGER NOT NULL, 
        date_created DATETIME, 
        date_modified DATETIME, 
        bodytxt VARCHAR(1444) NOT NULL, 
        account_id INTEGER NOT NULL, 
        topic_id INTEGER NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(account_id) REFERENCES account (id), 
        FOREIGN KEY(topic_id) REFERENCES topic (id)
)
```

* Topicaccount-taulu

```
CREATE TABLE topicaccount (
        id INTEGER NOT NULL, 
        date_created DATETIME, 
        creator BOOLEAN NOT NULL, 
        viewer BOOLEAN NOT NULL, 
        account_id INTEGER NOT NULL, 
        topic_id INTEGER NOT NULL, 
        PRIMARY KEY (id), 
        CHECK (creator IN (0, 1)), 
        CHECK (viewer IN (0, 1)), 
        FOREIGN KEY(account_id) REFERENCES account (id), 
        FOREIGN KEY(topic_id) REFERENCES topic (id)
)
```


## Linkit

* [Projekti Herokussa](http://tsoha-open-forum.herokuapp.com)
* [Lyhyt listaus keskeisimmistä käyttötapauksista](./documentation/usecases.txt)
* [Tietokantakaavio](./documentation/database_schema.JPG)







