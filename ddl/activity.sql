CREATE TABLE "ltt_activity_stage" (
  "id" varchar(45) NOT NULL,
  "username" varchar(64) DEFAULT NULL,
  "name" varchar(64) NOT NULL,
  "created" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "user_id" int DEFAULT NULL,
  "category_id" varchar(64) DEFAULT NULL,
  PRIMARY KEY ("id"),
  KEY "activity_category_fk_idx" ("category_id"),
  CONSTRAINT "activity_category_fk" FOREIGN KEY ("category_id") REFERENCES "ltt_category_stage" ("id")
)