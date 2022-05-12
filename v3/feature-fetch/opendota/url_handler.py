def get_hero_stats_url():
    hero_stats_url = "https://api.opendota.com/api/heroStats"
    return hero_stats_url


def get_heroes_url() -> str:
    return "https://api.opendota.com/api/heroes"


def get_pro_players_url() -> str:
    return "https://api.opendota.com/api/proPlayers"


def get_player_profile_url(account_id: str) -> str:
    return f"https://api.opendota.com/api/players/{account_id}"


def get_counts_url(account_id: str) -> str:
    return f"https://api.opendota.com/api/players/{account_id}/counts?significant=1&game_mode=1"


def get_totals_url(account_id: str) -> str:
    return f"https://api.opendota.com/api/players/{account_id}/totals?significant=1&game_mode=1"


def get_heroes_played_with_url(account_id: str) -> str:
    return f"https://api.opendota.com/api/players/{account_id}/heroes?significant=1&game_mode=1"


def get_hero_totals_url(account_id: str, hero_id: str) -> str:
    return f"https://api.opendota.com/api/players/{account_id}/totals?significant=1&game_mode=1&hero_id={hero_id}"

