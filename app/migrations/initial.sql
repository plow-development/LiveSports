CREATE TABLE users
(
    id              serial PRIMARY KEY,
    username        text      not null,
    hashed_password text      not null,
    email           text      not null,
    avatar          text      not null,
    firstname       text      not null,
    lastname        text      not null,
    birthday        timestamp not null,
    type            text      not null,
    money           integer   not null
);
CREATE TABLE sports
(
    id          serial PRIMARY KEY,
    name        text not null,
    description text not null,
    type        text not null
);
CREATE TABLE teams
(
    id        serial PRIMARY KEY,
    name      text    not null,
    master_id integer not null references users (id) on delete set null,
    sport_id  integer not null references sports (id) on delete set null
);
CREATE TABLE news
(
    id         serial PRIMARY KEY,
    title      text      not null,
    content    text      not null,
    preview    text      not null,
    publictime timestamp not null,
    author_id  integer   not null references users (id) on delete set null
);

CREATE TABLE events
(
    id        serial PRIMARY KEY,
    name      text  not null,
    starttime DATE  not null,
    latitude  FLOAT not null,
    longitude FLOAT not null
);

CREATE TABLE broadcasts
(
    id          serial PRIMARY KEY,
    title       text    not null,
    description text    not null,
    preview     text    not null,
    event_id    integer not null references events (id) on delete set null,
    link        text    not null
);

CREATE TABLE teams_users
(
    team_id integer not null references teams (id) on delete cascade,
    user_id integer not null references users (id) on delete cascade
);

CREATE TABLE user_sports
(
    user_id  integer not null references users (id) on delete cascade,
    sport_id integer not null references sports (id) on delete cascade
);

CREATE TABLE users_to_events
(
    user_id   integer not null references users (id) on delete cascade,
    event_id  integer not null references events (id) on delete cascade,
    user_type text    not null
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
