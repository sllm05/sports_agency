with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Replace only the later 3 occurrences
parts = text.split("</div> <!-- End of scouting-subtab-real -->")
print("Occurrences count:", len(parts) - 1)

# We want to keep the FIRST occurrence (index 0 and index 1 joined by that string)
# and remove it from the rest
new_text = parts[0] + "</div> <!-- End of scouting-subtab-real -->" + "".join(parts[1:])

with open("src/sports_agency/api/static/index.html", "w", encoding="utf-8") as f:
    f.write(new_text)

print("Cleaned up! Check count now:")
with open("src/sports_agency/api/static/index.html", "r", encoding="utf-8") as f:
    t2 = f.read()
print("Count now:", t2.count("End of scouting-subtab-real"))
