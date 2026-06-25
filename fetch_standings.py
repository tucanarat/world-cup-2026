import requests
import json
import os
from datetime import datetime, timezone

API_KEY = os.environ.get("SPORTRADAR_API_KEY", "afb8a78ed067402d8b19d6d5b29518d5")

# SportRadar Soccer API - FIFA World Cup 2026
API_URL = (
    f"https://api.sportradar.com/soccer/trial/v4/en/tournaments/"
    f"sr:tournament:17/seasons/sr:season:138490/standings.json?api_key={API_KEY}"
)

# Türkçe takım adları
TR_NAMES = {
    "Mexico": "Meksika", "South Africa": "Güney Afrika", "Korea Republic": "Güney Kore",
    "Czechia": "Çekya", "Switzerland": "İsviçre", "Canada": "Kanada",
    "Bosnia and Herzegovina": "Bosna Hersek", "Qatar": "Katar", "Brazil": "Brezilya",
    "Morocco": "Fas", "Scotland": "İskoçya", "Haiti": "Haiti", "USA": "ABD",
    "Australia": "Avustralya", "Paraguay": "Paraguay", "Turkiye": "Türkiye",
    "Germany": "Almanya", "Ivory Coast": "Fildişi Sahili", "Ecuador": "Ekvador",
    "Curacao": "Curaçao", "Netherlands": "Hollanda", "Japan": "Japonya",
    "Sweden": "İsveç", "Tunisia": "Tunus", "Egypt": "Mısır", "IR Iran": "İran",
    "Belgium": "Belçika", "New Zealand": "Yeni Zelanda", "Spain": "İspanya",
    "Uruguay": "Uruguay", "Cape Verde": "Cape Verde", "Saudi Arabia": "Suudi Arabistan",
    "France": "Fransa", "Norway": "Norveç", "Senegal": "Senegal", "Iraq": "Irak",
    "Argentina": "Arjantin", "Austria": "Avusturya", "Algeria": "Cezayir",
    "Jordan": "Ürdün", "Colombia": "Kolombiya", "Portugal": "Portekiz",
    "Congo DR": "Kongo DR", "Uzbekistan": "Özbekistan", "England": "İngiltere",
    "Ghana": "Gana", "Croatia": "Hırvatistan", "Panama": "Panama",
}

# Bayrak emoji haritası (kısaltma → emoji)
FLAGS = {
    "MEX": "🇲🇽", "RSA": "🇿🇦", "KOR": "🇰🇷", "CZE": "🇨🇿",
    "SUI": "🇨🇭", "CAN": "🇨🇦", "BIH": "🇧🇦", "QAT": "🇶🇦",
    "BRA": "🇧🇷", "MAR": "🇲🇦", "SCO": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "HTI": "🇭🇹",
    "USA": "🇺🇸", "AUS": "🇦🇺", "PAR": "🇵🇾", "TUR": "🇹🇷",
    "GER": "🇩🇪", "CIV": "🇨🇮", "ECU": "🇪🇨", "CUW": "🇨🇼",
    "NED": "🇳🇱", "JPN": "🇯🇵", "SWE": "🇸🇪", "TUN": "🇹🇳",
    "EGY": "🇪🇬", "IRN": "🇮🇷", "BEL": "🇧🇪", "NZL": "🇳🇿",
    "ESP": "🇪🇸", "URU": "🇺🇾", "CPV": "🇨🇻", "KSA": "🇸🇦",
    "FRA": "🇫🇷", "NOR": "🇳🇴", "SEN": "🇸🇳", "IRQ": "🇮🇶",
    "ARG": "🇦🇷", "AUT": "🇦🇹", "DZA": "🇩🇿", "JOR": "🇯🇴",
    "COL": "🇨🇴", "POR": "🇵🇹", "COD": "🇨🇩", "UZB": "🇺🇿",
    "ENG": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "GHA": "🇬🇭", "CRO": "🇭🇷", "PAN": "🇵🇦",
}

# Kısaltma haritası (takım adı → kısaltma)
ABBR_BY_NAME = {
    "Mexico": "MEX", "South Africa": "RSA", "Korea Republic": "KOR", "Czechia": "CZE",
    "Switzerland": "SUI", "Canada": "CAN", "Bosnia and Herzegovina": "BIH", "Qatar": "QAT",
    "Brazil": "BRA", "Morocco": "MAR", "Scotland": "SCO", "Haiti": "HTI",
    "USA": "USA", "Australia": "AUS", "Paraguay": "PAR", "Turkiye": "TUR",
    "Germany": "GER", "Ivory Coast": "CIV", "Ecuador": "ECU", "Curacao": "CUW",
    "Netherlands": "NED", "Japan": "JPN", "Sweden": "SWE", "Tunisia": "TUN",
    "Egypt": "EGY", "IR Iran": "IRN", "Belgium": "BEL", "New Zealand": "NZL",
    "Spain": "ESP", "Uruguay": "URU", "Cape Verde": "CPV", "Saudi Arabia": "KSA",
    "France": "FRA", "Norway": "NOR", "Senegal": "SEN", "Iraq": "IRQ",
    "Argentina": "ARG", "Austria": "AUT", "Algeria": "DZA", "Jordan": "JOR",
    "Colombia": "COL", "Portugal": "POR", "Congo DR": "COD", "Uzbekistan": "UZB",
    "England": "ENG", "Ghana": "GHA", "Croatia": "CRO", "Panama": "PAN",
}

# Fallback verisi (API çalışmazsa)
FALLBACK = [
    {"group": "A", "teams": [
        {"rank": 1, "abbr": "MEX", "name": "Meksika", "flag": "🇲🇽", "played": 3, "w": 3, "d": 0, "l": 0, "pts": 9, "qualified": True, "eliminated": False},
        {"rank": 2, "abbr": "RSA", "name": "Güney Afrika", "flag": "🇿🇦", "played": 3, "w": 1, "d": 1, "l": 1, "pts": 4, "qualified": True, "eliminated": False},
        {"rank": 3, "abbr": "KOR", "name": "Güney Kore", "flag": "🇰🇷", "played": 3, "w": 1, "d": 0, "l": 2, "pts": 3, "qualified": False, "eliminated": True},
        {"rank": 4, "abbr": "CZE", "name": "Çekya", "flag": "🇨🇿", "played": 3, "w": 0, "d": 1, "l": 2, "pts": 1, "qualified": False, "eliminated": True},
    ]},
    {"group": "B", "teams": [
        {"rank": 1, "abbr": "SUI", "name": "İsviçre", "flag": "🇨🇭", "played": 3, "w": 2, "d": 1, "l": 0, "pts": 7, "qualified": True, "eliminated": False},
        {"rank": 2, "abbr": "CAN", "name": "Kanada", "flag": "🇨🇦", "played": 3, "w": 1, "d": 1, "l": 1, "pts": 4, "qualified": True, "eliminated": False},
        {"rank": 3, "abbr": "BIH", "name": "Bosna Hersek", "flag": "🇧🇦", "played": 3, "w": 1, "d": 1, "l": 1, "pts": 4, "qualified": False, "eliminated": True},
        {"rank": 4, "abbr": "QAT", "name": "Katar", "flag": "🇶🇦", "played": 3, "w": 0, "d": 1, "l": 2, "pts": 1, "qualified": False, "eliminated": True},
    ]},
    {"group": "C", "teams": [
        {"rank": 1, "abbr": "BRA", "name": "Brezilya", "flag": "🇧🇷", "played": 3, "w": 2, "d": 1, "l": 0, "pts": 7, "qualified": True, "eliminated": False},
        {"rank": 2, "abbr": "MAR", "name": "Fas", "flag": "🇲🇦", "played": 3, "w": 2, "d": 1, "l": 0, "pts": 7, "qualified": True, "eliminated": False},
        {"rank": 3, "abbr": "SCO", "name": "İskoçya", "flag": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "played": 3, "w": 1, "d": 0, "l": 2, "pts": 3, "qualified": False, "eliminated": True},
        {"rank": 4, "abbr": "HTI", "name": "Haiti", "flag": "🇭🇹", "played": 3, "w": 0, "d": 0, "l": 3, "pts": 0, "qualified": False, "eliminated": True},
    ]},
    {"group": "D", "teams": [
        {"rank": 1, "abbr": "USA", "name": "ABD", "flag": "🇺🇸", "played": 2, "w": 2, "d": 0, "l": 0, "pts": 6, "qualified": False, "eliminated": False},
        {"rank": 2, "abbr": "AUS", "name": "Avustralya", "flag": "🇦🇺", "played": 2, "w": 1, "d": 0, "l": 1, "pts": 3, "qualified": False, "eliminated": False},
        {"rank": 3, "abbr": "PAR", "name": "Paraguay", "flag": "🇵🇾", "played": 2, "w": 1, "d": 0, "l": 1, "pts": 3, "qualified": False, "eliminated": False},
        {"rank": 4, "abbr": "TUR", "name": "Türkiye", "flag": "🇹🇷", "played": 2, "w": 0, "d": 0, "l": 2, "pts": 0, "qualified": False, "eliminated": True},
    ]},
    {"group": "E", "teams": [
        {"rank": 1, "abbr": "GER", "name": "Almanya", "flag": "🇩🇪", "played": 3, "w": 2, "d": 0, "l": 1, "pts": 6, "qualified": True, "eliminated": False},
        {"rank": 2, "abbr": "CIV", "name": "Fildişi Sahili", "flag": "🇨🇮", "played": 3, "w": 2, "d": 0, "l": 1, "pts": 6, "qualified": True, "eliminated": False},
        {"rank": 3, "abbr": "ECU", "name": "Ekvador", "flag": "🇪🇨", "played": 3, "w": 1, "d": 1, "l": 1, "pts": 4, "qualified": False, "eliminated": True},
        {"rank": 4, "abbr": "CUW", "name": "Curaçao", "flag": "🇨🇼", "played": 3, "w": 0, "d": 1, "l": 2, "pts": 1, "qualified": False, "eliminated": True},
    ]},
    {"group": "F", "teams": [
        {"rank": 1, "abbr": "NED", "name": "Hollanda", "flag": "🇳🇱", "played": 2, "w": 1, "d": 1, "l": 0, "pts": 4, "qualified": False, "eliminated": False},
        {"rank": 2, "abbr": "JPN", "name": "Japonya", "flag": "🇯🇵", "played": 2, "w": 1, "d": 1, "l": 0, "pts": 4, "qualified": False, "eliminated": False},
        {"rank": 3, "abbr": "SWE", "name": "İsveç", "flag": "🇸🇪", "played": 2, "w": 1, "d": 0, "l": 1, "pts": 3, "qualified": False, "eliminated": False},
        {"rank": 4, "abbr": "TUN", "name": "Tunus", "flag": "🇹🇳", "played": 2, "w": 0, "d": 0, "l": 2, "pts": 0, "qualified": False, "eliminated": True},
    ]},
    {"group": "G", "teams": [
        {"rank": 1, "abbr": "EGY", "name": "Mısır", "flag": "🇪🇬", "played": 2, "w": 1, "d": 1, "l": 0, "pts": 4, "qualified": False, "eliminated": False},
        {"rank": 2, "abbr": "IRN", "name": "İran", "flag": "🇮🇷", "played": 2, "w": 0, "d": 2, "l": 0, "pts": 2, "qualified": False, "eliminated": False},
        {"rank": 3, "abbr": "BEL", "name": "Belçika", "flag": "🇧🇪", "played": 2, "w": 0, "d": 2, "l": 0, "pts": 2, "qualified": False, "eliminated": False},
        {"rank": 4, "abbr": "NZL", "name": "Yeni Zelanda", "flag": "🇳🇿", "played": 2, "w": 0, "d": 1, "l": 1, "pts": 1, "qualified": False, "eliminated": False},
    ]},
    {"group": "H", "teams": [
        {"rank": 1, "abbr": "ESP", "name": "İspanya", "flag": "🇪🇸", "played": 2, "w": 1, "d": 1, "l": 0, "pts": 4, "qualified": False, "eliminated": False},
        {"rank": 2, "abbr": "URU", "name": "Uruguay", "flag": "🇺🇾", "played": 2, "w": 0, "d": 2, "l": 0, "pts": 2, "qualified": False, "eliminated": False},
        {"rank": 3, "abbr": "CPV", "name": "Cape Verde", "flag": "🇨🇻", "played": 2, "w": 0, "d": 2, "l": 0, "pts": 2, "qualified": False, "eliminated": False},
        {"rank": 4, "abbr": "KSA", "name": "Suudi Arabistan", "flag": "🇸🇦", "played": 2, "w": 0, "d": 1, "l": 1, "pts": 1, "qualified": False, "eliminated": False},
    ]},
    {"group": "I", "teams": [
        {"rank": 1, "abbr": "FRA", "name": "Fransa", "flag": "🇫🇷", "played": 2, "w": 2, "d": 0, "l": 0, "pts": 6, "qualified": False, "eliminated": False},
        {"rank": 2, "abbr": "NOR", "name": "Norveç", "flag": "🇳🇴", "played": 2, "w": 2, "d": 0, "l": 0, "pts": 6, "qualified": False, "eliminated": False},
        {"rank": 3, "abbr": "SEN", "name": "Senegal", "flag": "🇸🇳", "played": 2, "w": 0, "d": 0, "l": 2, "pts": 0, "qualified": False, "eliminated": True},
        {"rank": 4, "abbr": "IRQ", "name": "Irak", "flag": "🇮🇶", "played": 2, "w": 0, "d": 0, "l": 2, "pts": 0, "qualified": False, "eliminated": True},
    ]},
    {"group": "J", "teams": [
        {"rank": 1, "abbr": "ARG", "name": "Arjantin", "flag": "🇦🇷", "played": 2, "w": 2, "d": 0, "l": 0, "pts": 6, "qualified": False, "eliminated": False},
        {"rank": 2, "abbr": "AUT", "name": "Avusturya", "flag": "🇦🇹", "played": 2, "w": 1, "d": 0, "l": 1, "pts": 3, "qualified": False, "eliminated": False},
        {"rank": 3, "abbr": "DZA", "name": "Cezayir", "flag": "🇩🇿", "played": 2, "w": 1, "d": 0, "l": 1, "pts": 3, "qualified": False, "eliminated": False},
        {"rank": 4, "abbr": "JOR", "name": "Ürdün", "flag": "🇯🇴", "played": 2, "w": 0, "d": 0, "l": 2, "pts": 0, "qualified": False, "eliminated": True},
    ]},
    {"group": "K", "teams": [
        {"rank": 1, "abbr": "COL", "name": "Kolombiya", "flag": "🇨🇴", "played": 2, "w": 2, "d": 0, "l": 0, "pts": 6, "qualified": False, "eliminated": False},
        {"rank": 2, "abbr": "POR", "name": "Portekiz", "flag": "🇵🇹", "played": 2, "w": 1, "d": 1, "l": 0, "pts": 4, "qualified": False, "eliminated": False},
        {"rank": 3, "abbr": "COD", "name": "Kongo DR", "flag": "🇨🇩", "played": 2, "w": 0, "d": 1, "l": 1, "pts": 1, "qualified": False, "eliminated": False},
        {"rank": 4, "abbr": "UZB", "name": "Özbekistan", "flag": "🇺🇿", "played": 2, "w": 0, "d": 0, "l": 2, "pts": 0, "qualified": False, "eliminated": True},
    ]},
    {"group": "L", "teams": [
        {"rank": 1, "abbr": "ENG", "name": "İngiltere", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "played": 2, "w": 1, "d": 1, "l": 0, "pts": 4, "qualified": False, "eliminated": False},
        {"rank": 2, "abbr": "GHA", "name": "Gana", "flag": "🇬🇭", "played": 2, "w": 1, "d": 1, "l": 0, "pts": 4, "qualified": False, "eliminated": False},
        {"rank": 3, "abbr": "CRO", "name": "Hırvatistan", "flag": "🇭🇷", "played": 2, "w": 1, "d": 0, "l": 1, "pts": 3, "qualified": False, "eliminated": False},
        {"rank": 4, "abbr": "PAN", "name": "Panama", "flag": "🇵🇦", "played": 2, "w": 0, "d": 0, "l": 2, "pts": 0, "qualified": False, "eliminated": True},
    ]},
]


def is_qualified(rank, pts, played):
    if played >= 3 and rank <= 2:
        return True
    if pts >= 9:
        return True
    return False


def is_eliminated(rank, pts, played, max_can_get, second_pts):
    if played >= 3 and rank > 2:
        return True
    if played < 3 and max_can_get < second_pts - 3:
        return True
    return False


def parse_response(data):
    standings_arr = data.get("standings", [])
    group_map = {}

    for standing in standings_arr:
        if standing.get("type") and standing["type"] != "total":
            continue

        groups = standing.get("groups", [standing])
        for g in groups:
            group_name = g.get("name") or g.get("group_name") or standing.get("name") or "?"
            letter = group_name.replace("Group ", "").replace("GROUP_", "").strip().upper()
            if not letter:
                continue

            if letter not in group_map:
                group_map[letter] = []

            team_standings = g.get("team_standings") or g.get("standings") or []
            for ts in team_standings:
                team_obj = ts.get("team") or {}
                team_name = team_obj.get("name") or ts.get("name") or "?"
                abbr = team_obj.get("abbreviation") or ABBR_BY_NAME.get(team_name, "")
                w = ts.get("won") or ts.get("win") or 0
                d = ts.get("draw") or ts.get("drawn") or 0
                l = ts.get("lost") or ts.get("loss") or 0
                pts = ts.get("points") or 0
                rank = ts.get("rank") or 0
                played = w + d + l
                max_can_get = pts + (3 - played) * 3

                group_map[letter].append({
                    "rank": rank,
                    "abbr": abbr,
                    "name": TR_NAMES.get(team_name, team_name),
                    "flag": FLAGS.get(abbr, "🏳"),
                    "played": played,
                    "w": w,
                    "d": d,
                    "l": l,
                    "pts": pts,
                    "qualified": is_qualified(rank, pts, played),
                    "eliminated": False,  # sonradan doldurulacak
                })

    groups = []
    for letter in sorted(group_map.keys()):
        teams = sorted(group_map[letter], key=lambda t: t["rank"])
        second_pts = teams[1]["pts"] if len(teams) > 1 else 0
        for t in teams:
            max_can_get = t["pts"] + (3 - t["played"]) * 3
            if not t["qualified"]:
                t["eliminated"] = is_eliminated(t["rank"], t["pts"], t["played"], max_can_get, second_pts)
        groups.append({"group": letter, "teams": teams})

    return groups if groups else None


def main():
    print("SportRadar API'den veri çekiliyor...")
    groups = None

    try:
        resp = requests.get(API_URL, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        groups = parse_response(data)
        if groups:
            print(f"✓ API'den {len(groups)} grup verisi alındı.")
        else:
            print("⚠ API yanıtı boş, fallback kullanılıyor.")
    except Exception as e:
        print(f"⚠ API hatası: {e} — fallback kullanılıyor.")

    if not groups:
        groups = FALLBACK

    output = {
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "groups": groups,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("✓ data.json oluşturuldu.")


if __name__ == "__main__":
    main()
