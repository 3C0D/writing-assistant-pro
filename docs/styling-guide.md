# NiceGUI Styling Guide

## Overview

NiceGUI utilise **Quasar Framework** (basé sur Vue.js) et **Tailwind CSS**. Il est préférable d'utiliser ces outils natifs plutôt que du CSS custom pour un meilleur rendu et une meilleure maintenance.

## Stack Technique

- **Quasar** : Composants UI Material Design
- **Tailwind CSS** : Classes utilitaires pour le layout et le spacing
- **Vue.js** : Framework JavaScript sous-jacent

## Styling avec Quasar Props

### Syntaxe de base

```python
ui.button("Click me").props("flat dense color=primary")
```

### Props Quasar courantes

#### Boutons

```python
ui.button("Text")
    .props("flat")           # Bouton plat sans fond
    .props("outlined")       # Bouton avec bordure
    .props("round")          # Bouton rond
    .props("dense")          # Version compacte
    .props("color=primary")  # Couleur (primary, secondary, negative, positive, warning, info)
    .props("icon=home")      # Icône
```

#### Select / Dropdown

```python
ui.select(options={...})
    .props("outlined")       # Bordure visible
    .props("filled")         # Fond rempli
    .props("dense")          # Version compacte
    .props("dark")           # Force le mode dark
    .props("color=primary")  # Couleur d'accent
```

#### Input / TextField

```python
ui.input("Label")
    .props("outlined")       # Bordure visible
    .props("filled")         # Fond rempli
    .props("dense")          # Version compacte
    .props("clearable")      # Bouton pour effacer
```

## Styling avec Tailwind CSS

### Syntaxe de base

```python
ui.column().classes("gap-4 p-4 bg-gray-100")
```

### Classes Tailwind courantes

#### Layout & Spacing

```python
.classes("flex flex-col")        # Flexbox column
.classes("flex flex-row")        # Flexbox row
.classes("items-center")         # Align items center
.classes("justify-between")      # Space between
.classes("gap-4")                # Gap de 1rem (16px)
.classes("p-4")                  # Padding de 1rem
.classes("m-4")                  # Margin de 1rem
.classes("w-full")               # Width 100%
.classes("min-w-[150px]")        # Min width custom
```

#### Typography

```python
.classes("text-h6")              # Heading 6 (Quasar)
.classes("text-lg")              # Large text
.classes("font-bold")            # Bold
.classes("text-center")          # Center text
```

#### Colors

```python
.classes("bg-blue-500")          # Background blue
.classes("text-white")           # White text
.classes("border-gray-300")      # Gray border
```

## Gestion du Dark Mode

### Approche recommandée

Quasar gère automatiquement le dark mode pour ses composants. Utilisez les props natives :

```python
# ✅ Bon : Quasar gère le dark mode automatiquement
ui.select(options={...}).props("outlined dense")

# ❌ Éviter : CSS custom pour le dark mode
ui.select(options={...}).style("background-color: #2a2a2a")
```

### Force Dark Mode

Si nécessaire, vous pouvez forcer le dark mode sur un composant :

```python
ui.select(options={...}).props("outlined dense dark")
```

## Exemples Pratiques

### Header avec boutons

```python
with ui.header().classes("items-center justify-between bg-blue-600"):
    ui.label("App Title").classes("text-h6 text-white")

    with ui.row().classes("items-center gap-2"):
        ui.button(icon="settings").props("flat round dense color=white")
        ui.button("Hide").props("flat dense color=white")
```

### Formulaire avec inputs

```python
with ui.column().classes("gap-4 p-4 max-w-md"):
    ui.input("Name").props("outlined dense")
    ui.input("Email").props("outlined dense clearable")
    ui.select(
        options={"fr": "Français", "en": "English"}
    ).props("outlined dense").classes("min-w-[200px]")
    ui.button("Submit").props("color=primary")
```

### Card avec contenu

```python
with ui.card().classes("p-4 gap-2"):
    ui.label("Title").classes("text-lg font-bold")
    ui.label("Description text here")
    ui.button("Action").props("flat color=primary")
```

## Quand utiliser du CSS custom ?

Utilisez du CSS custom **uniquement** pour :

1. **Animations complexes** non disponibles dans Quasar/Tailwind
2. **Styles très spécifiques** à votre application
3. **Overrides globaux** (ex: police personnalisée)

### Exemple de CSS minimal

```css
/* styles/dark.css */
body {
  font-family: "Inter", sans-serif;
}

/* Animation custom */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.fade-in {
  animation: fadeIn 0.3s ease-in;
}
```

## Ressources

- [Quasar Components](https://quasar.dev/vue-components)
- [Quasar Props](https://quasar.dev/vue-components/button#qbtn-api)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [NiceGUI Documentation](https://nicegui.io/)

## Bonnes Pratiques

1. ✅ **Privilégier Quasar props** pour les composants UI
2. ✅ **Utiliser Tailwind** pour le layout et spacing
3. ✅ **Laisser Quasar gérer** le dark mode
4. ✅ **CSS custom minimal** pour les cas spécifiques
5. ❌ **Éviter** les styles inline excessifs
6. ❌ **Éviter** de surcharger les composants Quasar avec du CSS custom
