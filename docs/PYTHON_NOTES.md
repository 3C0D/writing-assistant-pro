# 🐍 Notes & Astuces Python

Base de connaissances personnelle pour le projet.

## 📏 Règles du Projet

### 1. Imports du Futur

Tous les fichiers Python du dossier `src/` doivent commencer par :

```python
from __future__ import annotations
```

Ceci est obligatoire pour garantir la cohérence du typage et le support des références futures.

## Typage Moderne (Type Hinting)

### `from __future__ import annotations`

Cette ligne magique, souvent placée au tout début des fichiers, permet d'activer le comportement de **postponed evaluation of annotations** (PEP 563).

**Pourquoi l'utiliser ?**

1.  **Forward References** : Elle permet d'utiliser une classe comme type à l'intérieur d'elle-même ou avant qu'elle ne soit définie, sans avoir à mettre le nom entre guillemets.

    _Sans l'import :_

    ```python
    class Node:
        def add_child(self, child: "Node") -> None:  # Obligé d'utiliser des guillemets
            pass
    ```

    _Avec l'import :_

    ```python
    from __future__ import annotations

    class Node:
        def add_child(self, child: Node) -> None:  # Plus propre !
            pass
    ```

2.  **Performance** : Les annotations ne sont pas évaluées au moment de l'exécution du module, ce qui accélère le temps de chargement, surtout si vous avez des imports lourds uniquement pour le typage.

3.  **Standard** : C'est le comportement par défaut prévu pour les futures versions de Python, donc c'est une bonne pratique de l'activer dès maintenant.
