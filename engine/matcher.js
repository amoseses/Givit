export function matchGifts(profile, gifts) {
  return gifts.filter(gift =>
    profile.budget >= gift.price_min &&
    profile.budget <= gift.price_max &&
    gift.age_range[0] <= profile.age &&
    gift.age_range[1] >= profile.age &&
    gift.tags.some(tag => profile.interests.includes(tag))
  );
}
