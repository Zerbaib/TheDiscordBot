CREATE TABLE IF NOT EXISTS ranking (
    id INT AUTO_INCREMENT PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS economy (
    id INT AUTO_INCREMENT PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS guilds (
    id INT AUTO_INCREMENT PRIMARY KEY
);

ALTER TABLE ranking ADD COLUMN IF NOT EXISTS guildID INT(30);
ALTER TABLE ranking ADD COLUMN IF NOT EXISTS userID INT(30);
ALTER TABLE ranking ADD COLUMN IF NOT EXISTS grade TEXT;
ALTER TABLE ranking ADD COLUMN IF NOT EXISTS rate INT;
ALTER TABLE ranking ADD COLUMN IF NOT EXISTS level INT;
ALTER TABLE ranking ADD COLUMN IF NOT EXISTS xp INT;
ALTER TABLE ranking MODIFY COLUMN guildID BIGINT UNSIGNED;
ALTER TABLE ranking MODIFY COLUMN userID BIGINT UNSIGNED;

ALTER TABLE economy ADD COLUMN IF NOT EXISTS guildID INT(30);
ALTER TABLE economy ADD COLUMN IF NOT EXISTS userID INT(30);
ALTER TABLE economy ADD COLUMN IF NOT EXISTS coins INT;
ALTER TABLE economy ADD COLUMN IF NOT EXISTS cooldown INT(40);
ALTER TABLE economy MODIFY COLUMN guildID BIGINT UNSIGNED;
ALTER TABLE economy MODIFY COLUMN userID BIGINT UNSIGNED;

ALTER TABLE guilds ADD COLUMN IF NOT EXISTS guild_id INT(30);
ALTER TABLE guilds ADD COLUMN IF NOT EXISTS ticket_category INT(30);
ALTER TABLE guilds ADD COLUMN IF NOT EXISTS support_role INT(30);
ALTER TABLE guilds ADD COLUMN IF NOT EXISTS welcome_channel INT(30);
ALTER TABLE guilds ADD COLUMN IF NOT EXISTS leave_channel INT(30);
ALTER TABLE guilds ADD COLUMN IF NOT EXISTS voice_table_channel INT(30);
ALTER TABLE guilds MODIFY COLUMN guild_id BIGINT UNSIGNED;
ALTER TABLE guilds MODIFY COLUMN ticket_category BIGINT UNSIGNED;
ALTER TABLE guilds MODIFY COLUMN support_role BIGINT UNSIGNED;
ALTER TABLE guilds MODIFY COLUMN welcome_channel BIGINT UNSIGNED;
ALTER TABLE guilds MODIFY COLUMN leave_channel BIGINT UNSIGNED;
ALTER TABLE guilds MODIFY COLUMN voice_table_channel BIGINT UNSIGNED;
