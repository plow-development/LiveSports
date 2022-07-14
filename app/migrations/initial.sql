CREATE TABLE users
(
    id              serial PRIMARY KEY,
    username        TEXT    NOT NULL UNIQUE,
    hashed_password TEXT    NOT NULL,
    email           TEXT    NOT NULL,
    avatar          TEXT    NOT NULL,
    firstname       TEXT    NOT NULL,
    lastname        TEXT    NOT NULL,
    birthday        DATE    NOT NULL,
    money           integer NOT NULL
);



CREATE TABLE sports
(
    id          serial PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT NOT NULL,
    type        TEXT NOT NULL
);



CREATE TABLE teams
(
    id        serial PRIMARY KEY,
    name      TEXT    NOT NULL,
    master_id TEXT    NOT NULL references users (id) on delete set null,
    sport_id  integer NOT NULL references sports (id) on delete set null
);



CREATE TABLE news
(
    id         serial PRIMARY KEY,
    title      TEXT      NOT NULL,
    content    TEXT      NOT NULL,
    preview    TEXT      NOT NULL,
    publictime TIMESTAMP NOT NULL,
    author_id  integer   NOT NULL references users (id) on delete set null
);



CREATE TABLE events
(
    id        serial PRIMARY KEY,
    name      TEXT      NOT NULL,
    starttime TIMESTAMP NOT NULL,
    latitude  FLOAT     NOT NULL,
    longitude FLOAT     NOT NULL
);



CREATE TABLE broadcasts
(
    id          serial PRIMARY KEY,
    title       TEXT    NOT NULL,
    description TEXT    NOT NULL,
    preview     TEXT    NOT NULL,
    event_id    integer NOT NULL references events (id) on delete set null,
    link        TEXT    NOT NULL
);



CREATE TABLE teams_users
(
    team_id integer NOT NULL references teams (id) on delete cascade,
    user_id integer NOT NULL references users (id) on delete cascade
);



CREATE TABLE user_sports
(
    user_id  integer NOT NULL references users (id) on delete cascade,
    sport_id integer NOT NULL references sports (id) on delete cascade
);



CREATE TABLE users_to_events
(
    user_id   integer NOT NULL references users (id) on delete cascade,
    event_id  integer NOT NULL references events (id) on delete cascade,
    user_type TEXT    NOT NULL
);



ALTER TABLE teams
    ADD CONSTRAINT teams_fk0 FOREIGN KEY (master_id) REFERENCES users (id);
ALTER TABLE teams
    ADD CONSTRAINT teams_fk1 FOREIGN KEY (sport_id) REFERENCES sports (id);

ALTER TABLE news
    ADD CONSTRAINT news_fk0 FOREIGN KEY (author_id) REFERENCES users (id);


ALTER TABLE broadcasts
    ADD CONSTRAINT broadcasts_fk0 FOREIGN KEY (event_id) REFERENCES events (id);

ALTER TABLE teams_users
    ADD CONSTRAINT teams_users_fk0 FOREIGN KEY (team_id) REFERENCES teams (id);
ALTER TABLE teams_users
    ADD CONSTRAINT teams_users_fk1 FOREIGN KEY (user_id) REFERENCES users (id);

ALTER TABLE user_sports
    ADD CONSTRAINT user_sports_fk0 FOREIGN KEY (user_id) REFERENCES users (id);
ALTER TABLE user_sports
    ADD CONSTRAINT user_sports_fk1 FOREIGN KEY (sport_id) REFERENCES sports (id);

ALTER TABLE users_to_events
    ADD CONSTRAINT users_to_events_fk0 FOREIGN KEY (user_id) REFERENCES users (id);
ALTER TABLE users_to_events
    ADD CONSTRAINT users_to_events_fk1 FOREIGN KEY (event_id) REFERENCES events (id);
