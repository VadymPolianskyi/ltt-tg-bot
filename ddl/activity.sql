CREATE TABLE `ltt_activity` (
  `id` VARCHAR(45) NOT NULL,
  `username` VARCHAR(64) NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`));