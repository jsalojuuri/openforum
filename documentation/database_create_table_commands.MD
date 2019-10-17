## Tietokantarakenteen kuvaus

Sovelluksen tietokanta on normalisoitu ja sen lopullinen tietokantarakenne vastaa oheista [tietokantakaaviota](./database_schema.JPG). Tietokannan CREATE TABLE -lauseet:

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
);
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
);
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
);
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
);
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
);
```