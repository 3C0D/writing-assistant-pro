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

## Alternatives Considérées

### Utility-First pour Flutter

Des packages tentent d'apporter une approche Tailwind à Flutter :

- **Mix** : Inspiré de Tailwind, réduit la verbosité
- **wind** : Utility-first avec class names, dark mode, breakpoints
- **tailwind_cli/tailwind_standards** : Wrappers des concepts Tailwind

> **Limitation** : Flutter n'a pas de support CSS natif, ces packages
> sont des traductions/wrappers

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
