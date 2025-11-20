# Optimisations de la Mémoire - Writing Assistant Pro

## Vue d'ensemble

Ce document détaille les stratégies d'optimisation mémoire pour Writing Assistant Pro, particulièrement après l'intégration des modèles de langage (LLM).

## État actuel de la consommation mémoire

### Analyse actuelle (sans LLM)

- **Total observé** : ~200 Mo
- **Répartition** :
  - NiceGUI + Pywebview : 50-80 Mo
  - Système de traduction : 10-20 Mo
  - Bibliothèques Python : 30-50 Mo
  - Python runtime : 30-50 Mo

### Projections futures (avec LLM)

- **Estimation totale** : 300-400 Mo
- **Ajout LLM** : 100-200 Mo selon le modèle

## Comparaisons avec applications similaires

| Application | Mémoire (Mo) | Type |
|-------------|--------------|------|
| VS Code | 200-500 | Éditeur de code |
| Navigateur web simple | 100-300 | Web browser |
| App desktop Python | 50-150 | Desktop app |
| **Writing Assistant Pro (avec LLM)** | **300-400** | **AI Text Editor** |
| ChatGPT web | 500+ | AI Service |

## Stratégies d'optimisation

### 1. Chargement intelligent (Lazy Loading)

**Principe :** Charger les modèles à la demande plutôt qu'au démarrage.

```python
# Exemple d'implémentation
class LLMManager:
    def __init__(self):
        self.model = None
        self.is_loaded = False

    def load_model_on_demand(self):
        if not self.is_loaded:
            self.model = load_model()
            self.is_loaded = True

    def unload_if_inactive(self):
        # Décharger après période d'inactivité
        pass
```

**Avantages :**

- Démarrage plus rapide
- Utilisation mémoire conditionnelle
- Meilleure réactivité utilisateur

### 2. Choix de modèles optimaux

#### Modèles recommandés par taille

| Modèle | Paramètres | Disque (Mo) | RAM (Mo) | Qualité |
|--------|------------|-------------|----------|---------|
| **TinyLlama** | 1.1B | 500 | 200 | ⭐⭐⭐ |
| **GPT-2 small** | 117M | 500 | 200 | ⭐⭐ |
| **Phi-2 mini** | 2.7B | 1300 | 600 | ⭐⭐⭐⭐ |

#### Critères de sélection

- **Qualité requise** : Évaluer le niveau de sophistication nécessaire
- **Contraintes matérielles** : RAM disponible sur les machines cibles
- **Latence acceptable** : Temps de réponse requis
- **Taille du modèle** : Compromis qualité/mémoire

### 3. Optimisations techniques

#### PyTorch Optimizations

```python
# Utilisation du mode inférence
with torch.inference_mode():
    output = model(input_text)

# Quantization 8-bit
from transformers import BitsAndBytesConfig
quantization_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_threshold=6.0
)
```

#### Streaming des réponses

- Éviter de charger tout le texte en mémoire
- Traiter les tokens au fur et à mesure
- Réduire l'empreinte mémoire temporaire

#### Gestion intelligente du cache

```python
class ModelCache:
    def __init__(self, max_size=2):
        self.cache = OrderedDict()
        self.max_size = max_size

    def get_model(self, model_name):
        if model_name not in self.cache:
            if len(self.cache) >= self.max_size:
                # Décharger le modèle le plus ancien
                self.cache.popitem(last=False)
            self.cache[model_name] = load_model(model_name)
        return self.cache[model_name]
```

## Architecture d'optimisation recommandée

### 1. Modèle de chargement progressif

```python
# Dans src/core/llm_manager.py
class OptimizedLLMManager:
    def __init__(self):
        self.light_model = None  # Chargé au démarrage
        self.heavy_model = None  # Chargé à la demande
        self.memory_monitor = MemoryMonitor()

    def initialize_lightweight(self):
        """Charge un modèle léger au démarrage"""
        self.light_model = load_tiny_model()

    def load_heavy_model_if_needed(self, use_case):
        if use_case == 'advanced':
            if not self.heavy_model:
                self.heavy_model = load_advanced_model()
        else:
            # Décharger le modèle lourd si pas nécessaire
            if self.heavy_model:
                del self.heavy_model
                self.heavy_model = None
                gc.collect()
```

### 2. Surveillance mémoire en temps réel

```python
class MemoryMonitor:
    def __init__(self, threshold_mb=300):
        self.threshold = threshold_mb
        self.alert_callback = None

    def check_memory_usage(self):
        import psutil
        current_memory = psutil.Process().memory_info().rss / 1024 / 1024

        if current_memory > self.threshold:
            if self.alert_callback:
                self.alert_callback(current_memory)

            # Actions de nettoyage
            self.trigger_cleanup()

    def trigger_cleanup(self):
        # Nettoyage agressif si nécessaire
        gc.collect()
```

### 3. Configuration adaptative

```python
# Dans src/config/memory_config.py
class MemoryConfig:
    def __init__(self, total_ram_gb):
        self.total_ram_gb = total_ram_gb

        if total_ram_gb >= 16:
            self.model_strategy = "heavy"  # 8B parameters max
        elif total_ram_gb >= 8:
            self.model_strategy = "medium"  # 3B parameters max
        else:
            self.model_strategy = "light"  # 1B parameters max

    def get_recommended_model(self):
        return {
            "light": "TinyLlama-1.1B",
            "medium": "Phi-2-mini-2.7B",
            "heavy": "Llama-2-7B"
        }
```

## Métriques et surveillance

### KPIs mémoire à suivre

1. **Usage RAM au démarrage** : < 150 Mo
2. **Usage RAM en utilisation normale** : < 350 Mo
3. **Pic mémoire lors du chargement LLM** : < 600 Mo
4. **Temps de déchargement modèle** : < 2 secondes
5. **Latence de bascule modèle** : < 1 seconde

### Outils de monitoring

```python
# Monitoring intégré dans main.py
def setup_memory_monitoring(app):
    monitor = MemoryMonitor(threshold_mb=350)

    def memory_alert(current_usage):
        app.log.warning(f"Mémoire élevée: {current_usage:.1f} Mo")
        # Actions automatiques de nettoyage

    monitor.set_alert_callback(memory_alert)
    monitor.start_monitoring()
```

## Roadmap d'optimisation

### Phase 1 - Immédiat (sans LLM)

- [x] Architecture de base optimisée
- [x] Fenêtre cachée au démarrage
- [x] Lazy loading des composants UI

### Phase 2 - Léger (Avec LLM optimisé)

- [ ] Intégration TinyLlama (200 Mo)
- [ ] Chargement à la demande
- [ ] Système de cache intelligent
- [ ] Monitoring mémoire en temps réel

### Phase 3 - Avancé

- [ ] Support multiples modèles
- [ ] Quantization 8-bit/4-bit
- [ ] Détection automatique configuration système
- [ ] Interface de gestion mémoire utilisateur

## Considérations platformes

### Windows (principal)

- **Gestionnaire des tâches** : Outil principal de monitoring
- **Limites** : 4GB+ RAM disponibles sur machines modernes
- **Optimisations** : Processus séparés pour isolation

### Linux

- **Outils** : `htop`, `ps aux --sort=-%mem`
- **Limites** : Excellent support de la mémoire
- **Optimisations** : Memory overcommit

### macOS

- **Outils** : Activity Monitor
- **Limites** : Restrictions sandbox
- **Optimisations** : NSSystemMemoryPressure

## Conclusion

La consommation estimée de 300-400 Mo est **tout à fait acceptable** pour une application de cette catégorie. Les optimisations proposées permettront de maintenir des performances optimales tout en offrant une expérience utilisateur fluide.

**Priorités d'implémentation :**

1. Lazy loading des modèles (impact maximum)
2. Choix de modèles adaptés (équilibre qualité/mémoire)
3. Monitoring intégré (maintenabilité)
4. Configuration adaptive (flexibilité utilisateur)
