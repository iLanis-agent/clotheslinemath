# Clothesline math

Clothesline math preps the line before the load: items become centimeters of
line and a pin count with spares, and the day's weather becomes drying hours
on a labeled scale.

Live site: https://ilanis-agent.github.io/clotheslinemath/

## The three tools

- **Line plan** - items x a labeled spacing (cm each) becomes the line needed;
  slack under 20% of need reads tight, negative reads short.
- **Pin plan** - items x pins each, plus a labeled 10% of spares (ceiling),
  becomes the basket count.
- **Dry plan** - `6 * 20 / tempC * humidityPct / 50` hours, rounded to one
  decimal, read as quick, same-day or overnight on the labeled scale.

## Limits

Every norm is labeled and illustrative. Fabric weight, wind and shade move
the real numbers; trust the touch test, not the clock.

## Files

- `index.html` - landing page with the labeled norms
- `app.html` - the three calculators
- `engine.js` - shared calculation and render logic (browser + node)
- `oracle.py` - python mirror of the engine, writes `expected.json`
- `test.js` - runs the engine against `expected.json` (12 cases, 57 checks)

Run the tests: `python3 oracle.py && node test.js`
