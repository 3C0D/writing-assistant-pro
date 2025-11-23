# Système de Systray (Barre des Tâches)

## 📋 Vue d'ensemble

Le gestionnaire de Systray (`SystrayManager`) permet à l'application de s'exécuter en arrière-plan avec une icône dans la zone de notification (barre des tâches). Il fournit un menu contextuel pour les actions rapides et gère le cycle de vie de l'application.

## 🎯 Objectifs

- Icône persistante dans la barre des tâches
- Menu contextuel (Clic droit)
- Contrôle de l'application (Afficher/Masquer, Quitter)
- Intégration avec le démarrage automatique
- Fonctionnement en thread séparé (non-bloquant)

## 🏗️ Architecture

### Fichier Principal

- [`src/core/systray_manager.py`](../src/core/systray_manager.py)

### Dépendances

- **pystray** : Librairie pour créer l'icône système
- **Pillow (PIL)** : Manipulation d'images pour l'icône

### Classe `SystrayManager`

La classe gère l'initialisation, l'affichage et les événements de l'icône.

```python
class SystrayManager:
    def __init__(self, page: ft.Page, on_about: Callable, app: Any):
        # ...
```

## 🔧 Fonctionnalités

### 1. Gestion de l'Icône

Le gestionnaire cherche l'icône de l'application (`app_icon.png`) à plusieurs endroits pour supporter les modes développement et production (frozen).

**Chemins vérifiés :**

1. `assets/icons/app_icon.png` (Mode Dev)
2. `app_icon.png` (Mode Frozen/Flat)

Si aucune icône n'est trouvée, une icône par défaut (carré vert) est générée dynamiquement.

### 2. Menu Contextuel

Le menu propose les options suivantes :

- **About** : Affiche les informations sur l'application via un callback.
- **Run on Startup** : Case à cocher synchronisée avec l'état du démarrage automatique.
- **Quit** : Ferme proprement l'application.

### 3. Exécution Asynchrone

L'icône tourne dans son propre thread pour ne pas bloquer l'interface utilisateur principale (Flet).

```python
def run_async(self) -> None:
    """Lance l'icône dans un thread séparé"""
    self._icon_thread = threading.Thread(target=self.run, daemon=True)
    self._icon_thread.start()
```

## 🚀 Utilisation

### Initialisation

Le `SystrayManager` est généralement initialisé dans la classe principale de l'application (`WritingAssistantFletApp`).

```python
# Dans src/ui/app_flet.py

self.systray_manager = SystrayManager(
    page=self.page,
    on_about=self.show_about_dialog,
    app=self
)
self.systray_manager.run_async()
```

### Arrêt Propre

Lors de la fermeture de l'application, il est crucial d'arrêter l'icône pour éviter les processus fantômes.

```python
def on_window_event(self, e):
    if e.data == "close":
        # Arrêt du systray
        if self.systray_manager:
            self.systray_manager.stop()
        # ...
```

## ⚙️ Détails Techniques

### Interaction avec Autostart

Le menu "Run on Startup" interagit directement avec `AutostartManager`. L'état de la case à cocher est déterminé dynamiquement :

```python
checked=lambda item: AutostartManager.check_autostart()
```

Le clic déclenche une mise à jour synchronisée :

```python
AutostartManager.set_autostart_with_sync(new_state, self.app.config)
```

### Nettoyage (Cleanup)

L'action "Quit" effectue un nettoyage complet avant de terminer le processus :

1. Nettoyage du gestionnaire de raccourcis (`hotkey_manager`)
2. Masquage de la fenêtre Flet
3. Arrêt de l'icône Systray
4. Terminaison forcée du processus (`os._exit(0)`)

## ⚠️ Points d'Attention

### Threading

`pystray` nécessite de tourner dans un thread si l'application principale a sa propre boucle d'événements (comme Flet). C'est pourquoi `run_async()` est utilisé.

### Icône Manquante

Si l'icône ne s'affiche pas, vérifiez que le fichier `app_icon.png` est bien présent dans `assets/icons/` et qu'il est correctement copié lors du build (voir [Système de Build](./03_BUILD_SYSTEM.md)).

### Fermeture de Fenêtre

Sur Windows, fermer la fenêtre principale ne doit pas nécessairement quitter l'application si le systray est actif. L'application peut simplement se masquer (comportement "Minimize to Tray").

## 🔗 Références

### Code Source

- [`src/core/systray_manager.py`](../src/core/systray_manager.py)

### Documentation Externe

- [pystray Documentation](https://pystray.readthedocs.io/en/latest/)
