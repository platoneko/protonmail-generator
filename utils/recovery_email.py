from dataclasses import dataclass

@dataclass(frozen=True)
class EmailData:
    email: str
    password: str
