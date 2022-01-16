CREATE TABLE "ltt_user" (
  "id" int NOT NULL,
  "username" varchar(64) DEFAULT NULL,
  "time_zone" varchar(64) NOT NULL DEFAULT 'UTC',
  "created" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY ("id")
)