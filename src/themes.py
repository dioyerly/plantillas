from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class Theme:
    name: str
    background: str
    soft: str
    accent: str
    ink: str = '#363541'
    rule: str = '#CECCD3'
    paper: str = '#FFFFFF'
    secondary: str = '#F3EFF5'
    tab: str = '#E9E0F2'
    divider: str = '#796487'
    text_secondary: str = '#77727B'
    button: str = '#E9E0F2'
    highlight: str = '#F7F2FA'

THEMES = {
    'lavender': Theme('LAVENDER', '#FBF9FD', '#E9E0F2', '#796487'),
    'blush': Theme('BLUSH', '#FFF9F9', '#F4DFE4', '#956773'),
    'sage': Theme('SAGE', '#F8FBF8', '#DFEBDD', '#627A64'),
    'sky': Theme('SKY', '#F8FBFE', '#DFEAF5', '#607B96'),
    'sand': Theme('SAND', '#FDFBF6', '#EFE5D2', '#88724F'),
    'neutral': Theme('NEUTRAL', '#FBFAF8', '#E8E5E1', '#77716A'),
}

def theme_data():
    return {key: asdict(value) for key, value in THEMES.items()}
