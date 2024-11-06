CREATE TABLE IF NOT EXISTS ranking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guildID INT,
    userID INT,
    level INT,
    xp INT
);
CREATE TABLE IF NOT EXISTS economy (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guildID INT,
    userID INT,
    coins INT,
    cooldown INT
);
CREATE TABLE IF NOT EXISTS guilds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guild_id INT,
    ticket_category INT,
    support_role INT,
    welcome_channel INT,
    leave_channel INT
);