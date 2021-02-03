CREATE VIEW GAMES_BY_USER AS
SELECT
    g.id,
    g.title,
    g.maker,
    g.game_type_id,
    g.number_of_players,
    g.skill_level,
    u.id user_id,
    u.first_name || ' ' || u.last_name AS full_name
FROM
    levelupapi_game g
JOIN
    levelupapi_gamer gr ON g.gamer_id = gr.id
JOIN
    auth_user u ON gr.user_id = u.id
;

DROP VIEW GAMES_BY_USER
DROP VIEW EVENTS_BY_USER

CREATE VIEW EVENTS_BY_USER AS
SELECT
    e.id,
    e.description,
    e.date,
    e.time,
    g.title,
    u.id user_id,
    u.first_name || ' ' || u.last_name AS full_name
FROM
    levelupapi_event e
JOIN
    levelupapi_eventgamers ge ON e.id = ge.event_id
JOIN
    levelupapi_gamer gr ON ge.gamer_id = gr.id
JOIN
    levelupapi_game g ON e.game_id = g.id
JOIN
    auth_user u ON gr.user_id = u.id
