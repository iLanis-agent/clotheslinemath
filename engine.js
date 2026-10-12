(function (root) {
  "use strict";
  function plural(n, word, form) { return n + " " + (n === 1 ? word : (form || word + "s")); }
  function round1(x) { return Math.round(x * 10) / 10; }

  function linePlan(items, cmPerItem, availableCm) {
    if (!(items > 0) || !(cmPerItem > 0) || !(availableCm > 0)) return { error: "items, spacing and line must be positive" };
    var needed = items * cmPerItem;
    var slack = availableCm - needed;
    var verdict;
    if (slack < 0) verdict = "short on the labeled spacing - a second line earns its hooks";
    else if (slack < needed * 0.2) verdict = "a tight fit on the labeled spacing";
    else verdict = "comfortable on the labeled spacing";
    return { needed: needed, slack: slack, verdict: verdict };
  }

  function pinPlan(items, pinsPerItem) {
    if (!(items > 0) || !(pinsPerItem > 0)) return { error: "items and pins must be positive" };
    var pins = items * pinsPerItem;
    var spares = Math.ceil(pins * 0.1);
    return { pins: pins, spares: spares, total: pins + spares };
  }

  function dryPlan(tempC, humidityPct) {
    if (!(tempC > 0) || !(humidityPct > 0)) return { error: "temperature and humidity must be positive" };
    var hours = round1(6 * 20 / tempC * humidityPct / 50);
    var verdict;
    if (hours < 3) verdict = "quick on the labeled scale";
    else if (hours < 6) verdict = "same-day on the labeled scale";
    else verdict = "an overnight job on the labeled scale";
    return { hours: hours, verdict: verdict };
  }

  function renderLine(r, items, cmPerItem, availableCm) {
    return plural(items, "item") + " at a labeled " + cmPerItem + " cm each needs " + r.needed + " cm of line; " + availableCm + " cm available leaves " + r.slack + " cm - " + r.verdict + ".";
  }

  function renderPin(r, items, pinsPerItem) {
    return plural(items, "item") + " at " + plural(pinsPerItem, "pin") + " each: " + plural(r.pins, "pin") + ", plus " + plural(r.spares, "spare") + " for the ones that vanish - " + plural(r.total, "pin") + " in the basket.";
  }

  function renderDry(r, tempC, humidityPct) {
    return "At " + tempC + " C and " + humidityPct + "% humidity, a load dries in about " + plural(r.hours, "hour") + " on the labeled scale - " + r.verdict + ".";
  }

  var api = { linePlan: linePlan, pinPlan: pinPlan, dryPlan: dryPlan, renderLine: renderLine, renderPin: renderPin, renderDry: renderDry };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.ClotheslineMath = api;
})(this);
