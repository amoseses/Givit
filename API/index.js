import express from "express";
import fs from "fs";
import gifts from "../data/gift_taxonomy.json" assert { type: "json" };
import { recommend } from "../engine/recommender.js";

const app = express();
app.use(express.json());

app.post("/recommend", (req, res) => {
  const profile = req.body;
  const results = recommend(profile, gifts);
  res.json(results);
});

app.post("/feedback", (req, res) => {
  const record = {
    timestamp: new Date().toISOString(),
    ...req.body
  };

  fs.appendFileSync(
    "./feedback_log.jsonl",
    JSON.stringify(record) + "\n"
  );

  res.sendStatus(200);
});

app.listen(3000, () => console.log("GiftBrain v2 running on :3000"));
