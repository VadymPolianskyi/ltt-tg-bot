CREATE TABLE "ltt_activity" (
  "id" varchar(45) NOT NULL,
  "username" varchar(64) DEFAULT NULL,
  "name" varchar(64) NOT NULL,
  "created" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "user_id" int DEFAULT NULL,
  PRIMARY KEY ("id")
)