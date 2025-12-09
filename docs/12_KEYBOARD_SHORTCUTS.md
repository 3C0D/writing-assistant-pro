# Raccourcis Clavier Globaux

## 📋 Vue d'ensemble

L'application utilise la librairie `keyboard` pour gérer des raccourcis clavier globaux, permettant de contrôler l'application même lorsqu'elle n'a pas le focus (ex: afficher/masquer la fenêtre).

## 🎯 Objectifs

- Contrôle global (System-wide)
- Afficher/Masquer la fenêtre rapidement
- Support multi-claviers (AZERTY, QWERTY)
- Détection des touches numpad via scancodes
- Interface de capture intuitive

## 🏗️ Architecture

### Fichiers Principaux

| Fichier                                                                         | Description                                |
| ------------------------------------------------------------------------------- | ------------------------------------------ |
| [`src/core/managers/hotkey.py`](../src/core/managers/hotkey.py)                 | Gestion de l'enregistrement des raccourcis |
| [`src/core/services/hotkey_capture.py`](../src/core/services/hotkey_capture.py) | Service de capture des touches             |
| [`src/ui/dialogs/hotkey_dialog.py`](../src/ui/dialogs/hotkey_dialog.py)         | Interface modale de configuration          |

### Dépendances

- **keyboard** : Librairie pour les hooks clavier système.

## 🔧 Fonctionnalités

### 1. Interface de Capture

Un dialog modal permet de capturer les raccourcis de manière intuitive :

- **Affichage en temps réel** des touches pressées
- **Boutons** : Save, Reset (défaut: `ctrl+space`), Delete (désactiver), Cancel
- **Tip affiché** : Pour les raccourcis avec Shift, appuyer sur la touche principale AVANT les modifiers

### 2. Support Multi-Claviers

Le système reconnaît les touches des claviers AZERTY et QWERTY :

| Clavier | Touche Shift          | Reconnaissance            |
| ------- | --------------------- | ------------------------- |
| QWERTY  | `shift`, `left shift` | ✅                        |
| AZERTY  | `maj`                 | ✅ (normalisé en `shift`) |

### 3. Détection Numpad via Scancodes

Les touches du pavé numérique sont détectées par leur scancode (code physique) pour éviter la confusion avec les touches principales :

| Scancode | Touche               |
| -------- | -------------------- |
| 83       | `Decimal` (numpad .) |
| 71-82    | `Num0` à `Num9`      |
| 78       | `NumAdd`             |
| 74       | `NumSubtract`        |

### 4. Enregistrement Différé (`register_delayed`)

Pour éviter les conflits au démarrage, l'enregistrement est effectué après un court délai (0.5s par défaut).

### 5. Gestion du Raccourci Désactivé

Le raccourci peut être défini sur `None` (désactivé). Dans ce cas :

- Le menu systray propose une entrée **Settings** pour accéder aux réglages
- Le `HotkeyManager` ignore l'enregistrement si le raccourci est vide

## 🚀 Utilisation

### Configuration via Interface

1. Ouvrir les **Settings** (icône engrenage ou menu systray)
2. Cliquer sur la zone du raccourci actuel
3. Appuyer sur la combinaison souhaitée
4. Cliquer sur **Save**

> **💡 Astuce Shift :** Si vous utilisez Shift avec une touche qui change de caractère (ex: `:` → `/`), appuyez sur la touche principale AVANT d'ajouter Shift.

### Configuration dans `config.json`

```json
{
  "hotkey_combination": "ctrl+space",
  "hotkey_setup_delay": 0.5
}
```

### Format des Raccourcis

- **Stockage** : `ctrl+shift+a` (minuscules, séparateur `+`)
- **Affichage** : `Ctrl + Shift + A` (capitalisé, espaces)
- **Désactivé** : `""` (chaîne vide)

## ⚠️ Dépannage

### Le raccourci ne fonctionne pas

1. **Permissions** : Sur certains systèmes, des droits administrateur peuvent être nécessaires.
2. **Conflits** : Une autre application utilise peut-être déjà ce raccourci.
3. **Logs** : Vérifiez `logs/run_dev.log` pour "Global hotkey registered".

### Shift modifie le caractère capturé

C'est normal pour les touches qui produisent un caractère différent avec Shift. Solution : appuyer sur la touche principale **avant** Shift.

### Accès aux réglages sans raccourci

Si le raccourci est désactivé (`None`), utilisez le menu contextuel du systray → **Settings**.

## 🔗 Références

### Code Source

- [`src/core/managers/hotkey.py`](../src/core/managers/hotkey.py)
- [`src/core/services/hotkey_capture.py`](../src/core/services/hotkey_capture.py)
- [`src/ui/dialogs/hotkey_dialog.py`](../src/ui/dialogs/hotkey_dialog.py)

### Documentation Externe

- [Keyboard Library](https://github.com/boppreh/keyboard)
