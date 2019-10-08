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

Sovellus on kehitetty Helsingin Yliopiston kurssin Tietokantasovellus projektina syys-lokakuussa 2019. Kurssin aikana toteutettiin suurin osa kurssin alussa suunnitelluista käyttötapauksista ja sovellus on jo sellaisenaan toimiva pienen ryhmän keskustelufoorumiksi. Sovelluksesta puuttuu toistaiseksi työkalut foorumien ja kirjoitusten hakemiseen, tietokantahakujen listauksia ole sivutettu sovelluksessa mitenkään eikä salasanoja ole salattu tietokannassa. Nämä on lisätty [käyttötapauslistauksen jatkokehitysideoihin](./documentation/usecases.txt), jonka lisäksi käyn tässä vielä lyhyesti läpi ajatuksia näiden toteuttamiseksi:

* Hakutoiminnallisuus: tämän hetkisen tiedon perusteella toteutus kannattaisi tehdä Pythonin [Whoosh-kirjaston](https://whoosh.readthedocs.io/en/latest/intro.html) avulla. Whooshiin on olemassa myös [SQLAlchemy integraatio](https://flask-whooshee.readthedocs.io/en/latest/), joka oletettavasti nopeuttaisi toteutusta.
* Listausten sivutus: listauksia, kuten Open Forumiin luotuja foorumeita, foorumin kirjoituksia tai kirjoituksen kommentteja voi niputtaa esim. kymmenen esiintymän ryhmiin per sivu, mikä parantaisi sovelluksen käytettävyyttä sisällön määrän kasvaessa. Sivutuksen toteutukseen Flask-ympäristössä voi tutustua esim. [Miguel Grinbergin blogin avulla](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ix-pagination).
* Salasanojen salaaminen: yksi varteenotettava salasanojen suojaamiseen käytettävä kirjasto Pythonilla on [Passlib](https://passlib.readthedocs.io/en/stable/), josta löytyy yli 30 erilaista salasanojen salausalgoritmia. 


## Keskeisimmät käyttötapaukset ja niihin liittyvät SQL-kyselyt

Sovelluksen keskeisimmät käyttötapaukset ja jatkokehitysideat on listattu lyhyesti [täällä](./documentation/usecases.txt). Ohessa vielä SQL-kyselyt näkymäkohtaisesti:


### Rekisteröityminen ja kirjautuminen

* Rekisteröitymislomakkeen tietojen haku käyttäjätunnuksen tarkistusta ja lomakkeen tietojen validointia varten. Jo käytössä olevaa tai tyhjää käyttäjätunnusta ei voi luoda (? = syötetty käyttäjätunnus)
```
SELECT
    * FROM Account
    WHERE Account.username = ?
    ;
```
* Rekisteröitymistietojen tallennus tietokantaan (? = Käyttäjän syöttämät tiedot)
```
INSERT INTO
    Account (date_created, date_modified, name, username, password, role)
    VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?, 'user')
    ;
```
* Kirjautumislomakkeen tietojen haku lomakkeen tietojen validointia varten (? = käyttäjän syöttämät tiedot)
```
SELECT
    * FROM Account
    WHERE Account.username = ? AND Account.password = ?
    ;
```

### Autorisoinnin tarkistus kaikissa näkymissä onnistuneen kirjautumisen jälkeen

* Haetaan käyttäjän tiedot autorisointia varten. Tämä tieto haetaan kirjautumisen jälkeen jokaisella sivulatauksella, jotta luvaton pääsy ylläpitopaneeliin estetään (? = aktiivisen käyttäjän account.id)
```
SELECT 
    * FROM Account
    WHERE Account.id = ?
    ;
```

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
* Yksittäisen foorumin tietojen haku lomakkeen validointia tai tietojen muokkausta varten (? = Haettavan foorumin nimi)
```
SELECT 
    * FROM Forum
    WHERE Forum.name = ?
    ;
```
* Uuden foorumin luominen (? = lomakkeella annetut foorumin nimi ja kuvaus)
```
INSERT INTO 
    Forum (date_created, date_modified, name, description)
    VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?)
    ;
```
* Luodun foorumin tietojen päivittäminen (? = lomakkeella annetut foorumin uusi nimi ja kuvaus sekä päivitettävän foorumin id)
```
UPDATE 
    Forum
    SET date_modified=CURRENT_TIMESTAMP, name=?, description=?
    WHERE Forum.id = ?
    ;
```
* Luodun foorumin poistaminen (? = poistettavan foorumin id)
```
DELETE 
    FROM Forum
    WHERE Forum.id = ?
    ;
```

### Foorumien listaus kirjautumisen jälkeen

* Listaus ja tilastointia palvelun kirjoituksista foorumeittain
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

### Valitun foorumin etusivu

* Tarkasteltavan foorumin tiedot (? = tarkasteltavan foorumin id)
```
SELECT 
    Forum.id AS forum_id, 
    Forum.date_created AS forum_date_created, 
    Forum.date_modified AS forum_date_modified, 
    Forum.name AS forum_name, 
    Forum.description AS forum_description FROM forum 
    WHERE forum.id = ?
    ;
```
* Foorumin kirjoitusten tiedot (? = tarkasteltava foorumi ja Topicaccount taulusta vain creator=True rivit)
```
SELECT 
    Topic.id, 
    Topic.title, 
    Topic.bodytxt, 
    Topic.date_modified, 
    Topic.forum_id, 
    Account.name, 
    Account.id, 
    COUNT(DISTINCT Comment.id) FROM Topic 
    LEFT JOIN Topicaccount ON Topicaccount.topic_id = Topic.id 
    LEFT JOIN Account ON Account.id = Topicaccount.account_id 
    LEFT JOIN Comment ON Topic.id = Comment.topic_id 
    WHERE (Topic.forum_id = ? AND Topicaccount.creator = ?) 
    GROUP BY Topic.id, Account.id
    ;
```
* Uuden kirjoituksen luominen (? = lomakkeella annetut kirjoituksen otsikko ja leipäteksti sekä parametrina annettu foorumin id; ? = creator=True, viever=False, parametreina saadut account_id ja topic_id)
```
INSERT INTO 
    Topic (date_created, date_modified, title, bodytxt, forum_id)
    VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?)
    ;

INSERT INTO 
    Topicaccount (date_created, creator, viewer, account_id, topic_id) 
    VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)
    ;
```

### Valitun kirjoituksen näkymä

* Kirjoituksen lukukerta, lisätään aina sivulatauksen yhteydessä. Ennen lisäystä haetaan kirjoituksen tiedot, jotta voidaan tietää onko kirjoituksen lukija sama kuin kirjoittaja (? = parametreina saatavat tiedot; ? = creator=True, jos kirjoittaja sama kuin lukija, muuten creator=False, muut parametreina saatavia tietoja)
```
SELECT 
    * FROM Topicaccount 
    WHERE Topicaccount.topic_id = ? AND topicaccount.creator = 1
    ;

INSERT INTO 
    Topicaccount (date_created, creator, viewer, account_id, topic_id) 
    VALUES (CURRENT_TIMESTAMP, ?, 1, ?, ?)
    ;
```
* Tarkasteltavan kirjoituksen tiedot (? = valitun kirjoituksen id parametrina, creator=True)
```
SELECT 
    Topic.title, 
    Topic.bodytxt, 
    Topic.date_modified, 
    Account.name, 
    Topic.id, 
    Topic.forum_id FROM Topic 
    LEFT JOIN Topicaccount ON Topic.id = Topicaccount.topic_id 
    LEFT JOIN Account ON Topicaccount.account_id = Account.id 
    WHERE (Topic.id = ? AND Topicaccount.creator = ?) 
    GROUP BY Topic.id, Account.name
    ;
```
* Tilastoja kirjoitukseen liittyen (? = tarkasteltavan kirjoituksen id, viewer=True)
```
SELECT 
    COUNT(DISTINCT Topicaccount.account_id), 
    COUNT(Topicaccount.account_id) FROM Topicaccount 
    WHERE (Topicaccount.topic_id = ? AND Topicaccount.viewer = ?)
    ;
```
* Tarkasteltavan kirjoituksen kommenttien tiedot (? = tarkasteltavan aiheen id parametrina)
```
SELECT 
    Account.name, 
    Comment.bodytxt, 
    Comment.date_modified FROM Comment 
    LEFT JOIN Account ON Comment.account_id = Account.id 
    WHERE (Comment.topic_id = ?)
    ;
```
* Uuden kommentin luominen (? = kommentin leipäteksti, account_id ja topic_id parametreina)
```
INSERT INTO 
    Comment (date_created, date_modified, bodytxt, account_id, topic_id) 
    VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?)
    ;
```

### Käyttäjän oma sivu

* Haetaan käyttäjän tiedot tietojen muokkausta varten valmiiksi lomakkeelle (? = aktiivisen käyttäjän account.id)
```
SELECT 
    * FROM Account
    WHERE Account.id = ?
    ;
```
* Haetaan tilasto käyttäjän kirjoituksista ja tehdyt kirjoitukset listausta varten (? = käyttäjän account_id ja creator=True) 
```
SELECT 
    COUNT(DISTINCT Topic.id) FROM Topic 
    LEFT JOIN Topicaccount ON Topic.id = Topicaccount.topic_id 
    WHERE Topicaccount.account_id = ? AND Topicaccount.creator = ?
    ;

SELECT 
    Topic.id, 
    Topic.title, 
    Topic.bodytxt, 
    Topic.date_modified, 
    Topic.forum_id FROM Topic 
    LEFT JOIN Topicaccount ON Topic.id = Topicaccount.topic_id 
    WHERE (Topicaccount.account_id = ? AND Topicaccount.creator = ?) 
    GROUP BY Topic.id 
    ORDER BY Topic.id
    ;
```
* Haetaan tilasto käyttäjän kommenteista ja tehdyt kommentit listausta varten (? = käyttäjän account_id) 
```
SELECT 
    COUNT(Comment.id) FROM Comment 
    WHERE Comment.account_id = ?
    ;

SELECT 
    Topic.forum_id,
    Topic.id, 
    Topic.title, 
    Comment.bodytxt, 
    Comment.date_modified, 
    Comment.id FROM Comment 
    LEFT JOIN Topic ON Comment.topic_id = Topic.id 
    WHERE (Comment.account_id = ?) 
    GROUP BY Topic.id, Comment.id ORDER BY Topic.id
    ;
```
* Käyttäjätietojen päivittäminen. Tarkistetaan ennen päivitystä, ettei käyttäjänimi ole jo käytössä toisella käyttäjällä (? = käyttäjän antamat syötteet. Kaikkia käyttäjätietojen kenttiä ei tarvitse muokata)
```
SELECT 
    * FROM Account
    WHERE Account.username = ?
    ;

UPDATE 
    Account 
    SET date_modified=CURRENT_TIMESTAMP, name=?, username=?, password=? 
    WHERE account.id = ?
    ;
```
* Kirjoituksen tietojen päivittäminen (Topic_id parametrina. Kaikkia kirjoituksen kenttiä ei tarvitse muokata)
```
SELECT 
    * FROM Topic
    WHERE Topic.id = ?
    ;

UPDATE 
    Topic 
    SET date_modified=CURRENT_TIMESTAMP, title=?, bodytxt=? 
    WHERE Topic.id = ?
    ;
```
* Kirjoituksen poistaminen. Tietoja on poistettava kahdesta eri taulusta. (? = tiedot tulevat parametreina taustalla)
```
DELETE 
    FROM Topicaccount 
    WHERE Topicaccount.id = ?

DELETE 
    FROM Topic 
    WHERE Topic.id = ?
```
* Kommentin tietojen päivittäminen (Comment_id parametrina. Kaikkia kirjoituksen kenttiä ei tarvitse muokata)
```
SELECT 
    * FROM Comment
    WHERE Comment.id = ?
    ;

UPDATE 
    Comment 
    SET date_modified=CURRENT_TIMESTAMP, bodytxt=? 
    WHERE Comment.id = ?
    ;
```
* Kommentin poistaminen (? = tiedot tulevat parametreina taustalla)
```
DELETE 
    FROM Comment 
    WHERE Comment.id = ?
```


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







