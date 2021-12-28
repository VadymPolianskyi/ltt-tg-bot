CREATE TABLE "ltt_event" (
  "id" varchar(64) NOT NULL,
  "activity_id" varchar(64) NOT NULL,
  "type" varchar(45) NOT NULL,
  "time" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "last" varchar(64) DEFAULT NULL,
  "username" varchar(64) NOT NULL,
  PRIMARY KEY ("id"),
  KEY "fk_activity_id" ("activity_id"),
  CONSTRAINT "fk_activity_id" FOREIGN KEY ("activity_id") REFERENCES "ltt_activity" ("id")
)