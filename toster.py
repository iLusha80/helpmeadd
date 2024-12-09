from parsers.parser_match_info import ParserMatchInfo

dt_str = '26.05. 22:00'
season = '2023-2024'

ParserMatchInfo.get_match_datetime(matchtime=dt_str, season=season)