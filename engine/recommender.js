import { matchGifts } from "./matcher.js";
import { scoreGift } from "./scorer.js";

export function recommend(profile, gifts) {
  return matchGifts(profile, gifts)
    .map(g => ({ ...g, score: scoreGift(g, profile) }))
    .sort((a, b) => b.score - a.score)
    .slice(0, 5);
}
