# Keskeisimmät käyttötapaukset

Sovellus on kehitetty Helsingin Yliopiston kurssin Tietokantasovellus projektina syys-lokakuussa 2019. Kurssin aikana toteutettiin suurin osa kurssin alussa suunnitelluista käyttötapauksista ja sovellus on jo sellaisenaan toimiva pienen ryhmän keskustelufoorumiksi. Ohessa on ensin lyhyesti kuvaukset toteutetuista käyttötapauksista, jonka jälkeen on huomioita sovelluksen rajoituksista ja ajatuksia toteuttamatta jääneiden käyttötapausten jatkokehityksestä. Lopuksi on vielä kattavampi kuvaus toteutettujen käyttötapausten SQL-kyselyistä näkymäkohtaisesti. 


## Sovellukseen toteutetut käyttötapaukset:

* *Rekisteröityminen ja kirjautuminen palveluun:* Käyttäjä löytää palvelun etusivulta helposti linkit rekisteröitymis- ja kirjautumislomakkeelle. Rekisteröitymislomakkeen täytettyään käyttäjä siirretään automaattisesti kirjautumislomakkeelle. Kirjautumisen jälkeen käyttäjä siirretään automaattisesti foorumeiden listaussivulle.
* *Listaus foorumeista:* Kirjautumisen jälkeen käyttäjälle listataan palvelun foorumit ja olennaista tilastotietoa foorumien käytöstä. Valittua foorumia klikkaamalla pääsee foorumin etusivulle 
* *Foorumin etusivu:* Valitun foorumin etusivulla listataan foorumille laaditut kirjoitukset ja näytetään olennaisia tilastoja kirjoituksista, kuten kirjoituskohtaisten kommenttien määrät.
* *Kirjoitusten lisääminen ja niiden kommentointi:* Kirjoituksia voi lisätä foorumin etusivulta lomakkeella. Lisätyt kirjoitukset listataan lyhyesti foorumin etusivulla ja niiden ohessa olevaa nappia painamalla pääsee siirtymään kirjoituskohtaiseen näkymään. Kaikki käyttäjät voivat kommentoida kirjoituksia kirjoituskohtaisesta näkymästä, josta näkee myös kuinka moni käyttäjä on nähnyt kirjoituksen ja montako kertaa kirjoitussivu on ladattu.
* *Käyttäjän omat sivut:* Käyttäjä pääsee navigaation kautta omalle sivulle, jossa tämä pystyy muuttamaan omia käyttäjätietojaan (nimi, käyttäjänimi ja salasana). Käyttäjälle listataan tämän laatimat kirjoitukset ja kommentit olennaisten tilastojen kanssa ja annetaan mahdollisuus niiden muokkaamiseen ja poistamiseen.
* *Ylläpitäjän paneeli:* Vain ylläpitäjä pääsee navigaation kautta näkymään, jossa pystyy lisäämään, muokkaamaan ja poistamaan foorumeita. Näkymään tilastoidaan lisäksi olennaisia tunnuslukuja foorumeittain ja koko palvelun osalta. 


## Sovelluksen rajoitteet ja jatkokehitysprojektille siirrettävät käyttötapaukset:

Sovelluksesta puuttuu toistaiseksi työkalut foorumien ja kirjoitusten hakemiseen, tietokantahakujen listauksia ei ole sivutettu sovelluksessa mitenkään eikä salasanoja ole salattu tietokannassa. Ohessa ajatuksia näiden jatkokehityksestä.

### Hakutoiminnallisuus, jolla mahdollista etsiä hakusanalla fooremeita, kirjoituksia ja kommentteja

* Hakutoiminallisuuden toteutus on käytettävyyden kannalta välttämätöntä, jotta foorumi olisi toimiva sisällön määrän kasvaessa. Tämän hetkisen tiedon perusteella toteutus kannattaisi tehdä Pythonin [Whoosh-kirjaston](https://whoosh.readthedocs.io/en/latest/intro.html) avulla. Whooshiin on olemassa myös [SQLAlchemy integraatio](https://flask-whooshee.readthedocs.io/en/latest/), joka oletettavasti nopeuttaisi toteutusta.

### Listausten sivutus

* Listauksia, kuten Open Forumiin luotuja foorumeita, foorumin kirjoituksia tai kirjoituksen kommentteja voi niputtaa esim. kymmenen esiintymän ryhmiin per sivu, mikä parantaisi sovelluksen käytettävyyttä sisällön määrän kasvaessa. Sivutuksen toteutukseen Flask-ympäristössä voi tutustua esim. [Miguel Grinbergin blogin avulla](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ix-pagination).

### Salasanojen salaaminen tietokannassa

* Salaamisella parannetaan sovelluksen tietoturvallisuutta. Salasanojen saluksella estetään käyttäjien salasanojen vuotaminen niin ylläpitäjille kuin pahantahtoisille henkilöille mahdollisen tietomurron yhteydessä. Salauksella tietokantaan tallennetut salasanat ovat normaalisti käytettävissä sovelluksen tarpeisiin, mutta näyttävät tunnistamattomilta merkkijonoilta salausalgoritmin käsittelyn jälkeen. Yksi varteenotettava salasanojen suojaamiseen käytettävä kirjasto Pythonilla on [Passlib](https://passlib.readthedocs.io/en/stable/), josta löytyy yli 30 erilaista salasanojen salausalgoritmia. 


## Käyttötapauksiin liittyvät SQL-kyselyt näkymäkohtaisesti

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
    ;

DELETE 
    FROM Topic 
    WHERE Topic.id = ?
    ;
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
    ;
```