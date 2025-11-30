# Choix du Framework UI : Flet vs NiceGUI

## Contexte

Ce document explique pourquoi le projet Writing Assistant Pro utilise
**Flet** plutôt que **NiceGUI** pour son interface utilisateur, malgré
les avantages esthétiques de ce dernier.

## NiceGUI : Avantages et Limitations

### ✅ Avantages de NiceGUI

NiceGUI offre des styles modernes et riches grâce à sa stack
technologique :

- **Tailwind CSS** : Approche utility-first avec classes atomiques
  (`bg-blue-500`, `hover:bg-sky-700`)
- **Quasar Framework** : Composants Vue.js pré-stylés et élégants
- **Excellente expérience développeur** pour les applications web

### ❌ Limitations Critiques du Mode Natif

Malheureusement, le mode natif de NiceGUI présente des problèmes
majeurs qui le rendent **inadapté pour une application desktop
production** :

#### 1. Problèmes Multiprocessing Récurrents

- Erreurs `SemLock` avec fork vs spawn context (Ubuntu/Linux)
- Issues persistantes depuis 2023 non résolues
- Marquées comme "advanced difficulty" nécessitant l'intervention
  de la communauté

#### 2. Problèmes d'Affichage

- Fenêtres natives qui s'ouvrent vides (blank white canvas) sur
  Mac/Linux
- Le webview par défaut (mshtml/IE) incompatible avec NiceGUI sur
  Windows
- Nécessite configuration manuelle vers EdgeChromium ou Qt

#### 3. Limitations Architecture

- **Pas de tests automatiques** pour le mode natif (l'équipe n'a pas
  trouvé de solution)
- Erreurs Windows avec `os.getpgid` non supporté
- Dépendance directe à `pywebview` avec ses propres bugs (fenêtres
  frameless, minimisation taskbar)

#### 4. Bugs Versions Récentes

- Attribut `webview.settings` manquant selon versions de pywebview
- `app.main_window` undefined jusqu'en version 2.10.1
- Problèmes de persistance d'objets en mode natif

#### 5. Architecture Fondamentale

> NiceGUI reste un **serveur HTTP servant du HTML, même pour les
> fenêtres natives**. Ce n'est pas une véritable application native.

## Flet : La Solution Retenue

### ✅ Avantages de Flet

1. **Architecture Native** : Utilise Flutter directement, compilation
   en natif cross-platform
2. **Conversion Instantanée** : Desktop ↔ Web ↔ Mobile en changeant
   une ligne
3. **Stabilité** : Pas de problèmes de multiprocessing ou de webview
4. **Production Ready** : Framework mature pour applications standalone

### ⚠️ Compromis Accepté

- **Styles moins riches** : Material Design 3 au lieu de
  Tailwind/Quasar
- **Approche différente** : Pas de classes utility-first, mais
  thèmes Material
- **Verbosité** : Code plus verbeux qu'avec Tailwind

### Exemple de Différence de Style

**NiceGUI (Tailwind) :**

```python
ui.button(
    "Click",
    classes="bg-blue-500 hover:bg-blue-700 text-white"
)
```

**Flet (Material Design) :**

```python
ft.ElevatedButton(
    "Click",
    bgcolor=ft.Colors.BLUE_500,
    color=ft.Colors.WHITE
)
```

## Alternatives Utility-First pour Flutter

Des packages existent pour apporter l'approche utility-first de
Tailwind CSS à Flutter :

- **Mix** ([fluttermix.com](https://fluttermix.com)) : API composable
  style Tailwind avec builder pattern
- **Wind** ([fluttersdk/wind](https://github.com/fluttersdk/wind)) :
  Interprète des class names directement (syntaxe quasi-identique à
  Tailwind)
- **tailwind_cli/tailwind_standards** : Widgets pré-stylés avec
  conventions Tailwind

### ⚠️ Pourquoi Ces Alternatives Ne Sont Pas Adaptées

**Limitation fondamentale** : Tous ces packages nécessitent
**Flutter natif** (développement en Dart).

Flet est une **abstraction Python** au-dessus de Flutter qui ne donne
**pas accès aux widgets Flutter bruts**. Vous êtes limité à l'API Flet
qui encapsule Material Design.

**Verdict** : Ces solutions utility-first ne sont donc **pas
utilisables** dans Writing Assistant Pro. Pour bénéficier de
Tailwind-like styling, il faudrait réécrire l'application en
Flutter/Dart pur, ce qui contredirait la raison principale d'utiliser
Flet : le développement rapide en Python.

## Architecture Actuelle et Améliorations Possibles

### ✅ Ce Que L'Application Utilise Déjà

L'application implémente actuellement une approche **Flet + composants
custom** dans [`app.py`](file:///c:/Users/dd200/Documents/Mes_projets/WritingTools%20Related/writing-assistant-pro/src/ui/app.py) :

**Points forts existants :**

- ✅ **Dark/Light Mode** : `ft.ThemeMode.DARK` / `LIGHT` avec toggle
- ✅ **Composants réutilisables** : Méthodes comme
  `_create_navigation_rail()`, `_create_sidebar()`
- ✅ **Styling manuel** : Utilisation de `ft.Container` avec
  `bgcolor`, `border_radius`, `padding`
- ✅ **Couleurs conditionnelles** : Adaptation selon `DARK_MODE`

**Exemple existant (lignes 153-179) :**

```python
def _create_navigation_rail(self):
    return ft.Container(
        width=50,
        bgcolor="#3a3a3a" if self.config.DARK_MODE else "#e0e0e0",
        content=ft.Column([...])
    )
```

### 🎯 Améliorations Recommandées

Pour réduire la verbosité et améliorer la maintenabilité, voici les
évolutions à considérer :

#### 1. 📐 Design System Centralisé

**Problème actuel** : Couleurs hardcodées dispersées dans le code
(`#3a3a3a`, `#b0b0b0`, etc.)

**Solution** : Créer `src/ui/design_system.py` :

```python
"""Design System centralisé pour Writing Assistant Pro"""
import flet as ft

class AppColors:
    """Palette de couleurs de l'application"""
    # Dark Mode
    DARK_BG_PRIMARY = "#2b2b2b"
    DARK_BG_SECONDARY = "#2e2e2e"
    DARK_BG_RAIL = "#3a3a3a"
    DARK_TEXT_PRIMARY = "#b0b0b0"
    DARK_TEXT_SECONDARY = "#808080"

    # Light Mode
    LIGHT_BG_PRIMARY = "#fafafa"
    LIGHT_BG_SECONDARY = "#f5f5f5"
    LIGHT_BG_RAIL = "#e0e0e0"
    LIGHT_TEXT_PRIMARY = "#404040"
    LIGHT_TEXT_SECONDARY = "#707070"

    @staticmethod
    def get_bg_primary(dark_mode: bool) -> str:
        return (
            AppColors.DARK_BG_PRIMARY
            if dark_mode
            else AppColors.LIGHT_BG_PRIMARY
        )

class AppSpacing:
    """Espacements standardisés"""
    XS = 4
    SM = 8
    MD = 16
    LG = 24
    XL = 32

class AppTypography:
    """Styles de typographie"""
    HEADING_LARGE = ft.TextStyle(
        size=24, weight=ft.FontWeight.BOLD
    )
    HEADING_MEDIUM = ft.TextStyle(
        size=18, weight=ft.FontWeight.BOLD
    )
    BODY = ft.TextStyle(size=16)
```

**Utilisation :**

```python
# Avant
bgcolor="#2b2b2b" if self.config.DARK_MODE else "#fafafa"

# Après
bgcolor=AppColors.get_bg_primary(self.config.DARK_MODE)
```

#### 2. 🧩 Composants comme Classes (UserControl)

**Problème actuel** : Tout dans des méthodes de `WritingAssistantFletApp`

**Solution** : Créer `src/ui/components/navigation_rail.py` :

```python
"""Navigation Rail Component"""
import flet as ft
from src.ui.design_system import AppColors, AppSpacing

class NavigationRail(ft.UserControl):
    """Navigation rail réutilisable"""

    def __init__(
        self,
        dark_mode: bool,
        on_menu_click,
        on_settings_click
    ):
        super().__init__()
        self.dark_mode = dark_mode
        self.on_menu_click = on_menu_click
        self.on_settings_click = on_settings_click

    def build(self):
        return ft.Container(
            width=50,
            bgcolor=AppColors.get_bg_rail(self.dark_mode),
            content=ft.Column([
                ft.IconButton(
                    icon=ft.Icons.MENU,
                    on_click=self.on_menu_click,
                ),
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.Icons.SETTINGS,
                    on_click=self.on_settings_click,
                ),
            ])
        )
```

**Avantages :**

- ✅ Type-safe avec autocomplétion Python
- ✅ Réutilisable comme composants React
- ✅ Isolé et testable
- ✅ Réduit la taille de `app.py`

#### 3. 🏭 Factory Functions pour Patterns Répétitifs

**Solution** : Créer `src/ui/components/common.py` :

```python
"""Composants UI communs réutilisables"""
import flet as ft
from src.ui.design_system import AppColors, AppSpacing

def styled_card(
    content: ft.Control,
    dark_mode: bool,
    elevation: int = 2,
    padding: int = AppSpacing.MD
) -> ft.Container:
    """Card avec style uniforme"""
    return ft.Container(
        content=content,
        padding=ft.padding.all(padding),
        border_radius=ft.border_radius.all(12),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=elevation * 2,
            color=ft.Colors.with_opacity(
                0.1, ft.Colors.BLACK
            )
        ),
        bgcolor=AppColors.get_surface(dark_mode)
    )

def icon_button(
    icon: str,
    tooltip: str,
    dark_mode: bool,
    on_click
) -> ft.IconButton:
    """Icon button avec style cohérent"""
    return ft.IconButton(
        icon=icon,
        icon_color=AppColors.get_icon_color(dark_mode),
        tooltip=tooltip,
        on_click=on_click
    )
```

#### 4. 🎨 Exploiter Material Design 3

Flet permet d'utiliser les capacités natives de Material Design :

- **Gradients** : `ft.LinearGradient`, `ft.RadialGradient`
- **Animations** : `ft.AnimatedContainer` pour transitions fluides
- **Markdown** : `ft.Markdown()` avec syntax highlighting
- **Scrolling** : `ft.ListView()` ou `scroll=ft.ScrollMode.AUTO`

#### 5. 🎭 Inspiration de Projets Existants

Références pour des interfaces Flet avancées :

- [Flet Material Library](https://flet-material.vercel.app)
- [material_design_flet](https://github.com/LineIndent/material_design_flet)
- Galerie d'exemples Flet officielle

### 📊 Comparaison des Approches

| Aspect              | Actuel (app.py) | Design System         |
| ------------------- | --------------- | --------------------- |
| **Couleurs**        | Hardcodées      | Centralisées          |
| **Composants**      | Méthodes        | Classes `UserControl` |
| **Réutilisabilité** | Limitée         | Maximale              |
| **Maintenabilité**  | Moyenne         | Excellente            |
| **Verbosité**       | Élevée          | Réduite               |

> **Verdict** : Flet + design system bien architecturé = meilleur
> ratio rapidité/qualité/maintenabilité pour une application desktop
> Python, malgré l'absence de styling utility-first à la Tailwind.

## Conclusion

Le choix de **Flet** a été fait **à contrecœur** concernant
l'esthétique, mais est **nécessaire** pour la fiabilité et la
stabilité d'une application desktop native.

**NiceGUI** reste excellent pour des applications web, mais son mode
natif est **trop immature pour la production** au moment de cette
décision.

## Références

- [Discussion NiceGUI Production Ready](https://github.com/zauberzeug/nicegui/discussions/395)
- [Issue #1841 NiceGUI Native Mode](https://github.com/zauberzeug/nicegui/issues/1841)
- [Flet Documentation](https://flet.dev)
- Recherches utilisateur confirmant les limitations (Hacker News,
  GitHub Issues)

---

_Document créé le : 2025-11-24_
_Dernière mise à jour : 2025-11-24_
