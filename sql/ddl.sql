create table daily_checkins
(
    id        serial,
    username  varchar(100),
    project   varchar(100),
    hours     float,
    timestamp timestamp,
    primary key (id)
);