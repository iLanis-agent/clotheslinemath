import json, math

def jsnum(x):
    return int(x) if isinstance(x, float) and x == int(x) else x
def plural(n, word, form=None): return str(jsnum(n)) + " " + (word if n == 1 else (form or word + "s"))
def fmt(x): return str(jsnum(x))
def round1(x): return jsnum(math.floor(x * 10 + 0.5) / 10)

def line_plan(items, cmPerItem, availableCm):
    if not (items > 0) or not (cmPerItem > 0) or not (availableCm > 0):
        return {"error": "items, spacing and line must be positive"}
    needed = items * cmPerItem
    slack = availableCm - needed
    if slack < 0: verdict = "short on the labeled spacing - a second line earns its hooks"
    elif slack < needed * 0.2: verdict = "a tight fit on the labeled spacing"
    else: verdict = "comfortable on the labeled spacing"
    return {"needed": needed, "slack": slack, "verdict": verdict}

def pin_plan(items, pinsPerItem):
    if not (items > 0) or not (pinsPerItem > 0):
        return {"error": "items and pins must be positive"}
    pins = items * pinsPerItem
    spares = math.ceil(pins * 0.1)
    return {"pins": pins, "spares": spares, "total": pins + spares}

def dry_plan(tempC, humidityPct):
    if not (tempC > 0) or not (humidityPct > 0):
        return {"error": "temperature and humidity must be positive"}
    hours = round1(6 * 20 / tempC * humidityPct / 50)
    if hours < 3: verdict = "quick on the labeled scale"
    elif hours < 6: verdict = "same-day on the labeled scale"
    else: verdict = "an overnight job on the labeled scale"
    return {"hours": hours, "verdict": verdict}

def render_line(r, items, cmPerItem, availableCm):
    return (plural(items, "item") + " at a labeled " + fmt(cmPerItem) + " cm each needs " + fmt(r["needed"])
            + " cm of line; " + fmt(availableCm) + " cm available leaves " + fmt(r["slack"]) + " cm - "
            + r["verdict"] + ".")

def render_pin(r, items, pinsPerItem):
    return (plural(items, "item") + " at " + plural(pinsPerItem, "pin") + " each: " + plural(r["pins"], "pin")
            + ", plus " + plural(r["spares"], "spare") + " for the ones that vanish - " + plural(r["total"], "pin")
            + " in the basket.")

def render_dry(r, tempC, humidityPct):
    return ("At " + fmt(tempC) + " C and " + fmt(humidityPct) + "% humidity, a load dries in about "
            + plural(r["hours"], "hour") + " on the labeled scale - " + r["verdict"] + ".")

cases = []
for a in [(20, 12, 300), (20, 12, 250), (20, 12, 230), (0, 12, 300)]:
    r = line_plan(*a)
    cases.append({"fn": "linePlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_line(r, *a)})
for a in [(20, 2), (7, 3), (12, 2), (0, 2)]:
    r = pin_plan(*a)
    cases.append({"fn": "pinPlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_pin(r, *a)})
for a in [(25, 40), (15, 80), (30, 30), (0, 40)]:
    r = dry_plan(*a)
    cases.append({"fn": "dryPlan", "args": list(a), "result": r,
                  "render": None if "error" in r else render_dry(r, *a)})

with open("expected.json", "w") as f:
    f.write(json.dumps(cases, separators=(",", ":")) + "\n")
print("wrote", len(cases), "cases")
