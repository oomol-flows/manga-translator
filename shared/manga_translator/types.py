from typing import Literal

TargetLanguage = Literal[
    "CHS", "CHT", "CSY", "NLD", "ENG", "FRA", "DEU", "HUN", "ITA", "JPN",
    "KOR", "PLK", "PTB", "ROM", "RUS", "ESP", "TRK", "UKR", "VIN", "CNR",
    "SRP", "HRV", "ARA", "THA", "IND",
]

SourceLanguage = Literal["auto"] | TargetLanguage