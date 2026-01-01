export function scoreGift(gift, profile) {
  let score = 0;
  gift.tags.forEach(tag => {
    if (profile.interests.includes(tag)) score += 2;
  });
  if (profile.occasion === "romantic" && gift.tags.includes("aesthetic")) {
    score += 3;
  }
  return score;
}
