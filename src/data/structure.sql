CREATE TABLE IF NOT EXISTS ranking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guildID INTEGER,
    userID INTEGER,
    level INTEGER,
    xp INTEGER
);
CREATE TABLE IF NOT EXISTS economy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guildID INTEGER,
    userID INTEGER,
    coins INTEGER,
    cooldown INTEGER
);
CREATE TABLE IF NOT EXISTS guilds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id INTEGER,
    ticket_category INTEGER,
    support_role INTEGER,
    welcome_channel INTEGER,
    leave_channel INTEGER
);
CREATE TABLE IF NOT EXISTS servers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userID INTEGER,
    server_name TEXT,
    server_ip INTEGER,
    server_port INTEGER,
    service_name TEXT
);