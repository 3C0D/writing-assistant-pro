# Structure datas

## Format: SQLite + JSON

```
project/
├── data/
│   ├── app.db              # conversations, messages, rag, users
│   ├── config.json         # app config(thème, settings UI), user prefs, API keys
│   └── prompts.json        # templates, system prompts
├── cache/
│   └── llm_responses.db    # cache LLM
└── exports/
    └── *.json              # user exports
```

**Cache:** Stocke les réponses LLM déjà générées pour éviter de re-appeler l'API si même prompt → économie coûts/temps.

**Exports:** Fichiers JSON générés quand l'user exporte ses conversations/documents pour backup ou utilisation externe.

### Détails data

100% json. Recommendé pour appli locale

```
data/
├── config.json          # Committé sur GitHub (settings par défaut)
└── config.local.json    # .gitignore (API keys)
```

App charge : `config.json` puis override avec `config.local.json` si existe. voir après.

Alternativement, pour config (serveur, cloud) :
.env                     # .gitignore (API keys)
config.json             # Committé (settings app)

#### Exemple 100% json avec override

```python
import json
from pathlib import Path

# Load default config
with open('data/config.json') as f:
    config = json.load(f)

# Override with local config if exists
local_config_path = Path('data/config.local.json')
if local_config_path.exists():
    with open(local_config_path) as f:
        local_config = json.load(f)
        config.update(local_config)  # Merge/override

# config contient maintenant les valeurs fusionnées
```

**Exemple fichiers :**

`config.json` (committé) :

```json
{"theme": "dark", "api_key": ""}
```

`config.local.json` (gitignore) :

```json
{"api_key": "sk-xxx"}
```

**Résultat :** `config = {"theme": "dark", "api_key": "sk-xxx"}`

### Libs

sqlite3 ou sqlalchemy + json

### Tables SQLite (brain storming...)

- conversations (id, title, created_at)
- messages (id, conv_id, role, content, timestamp)
- users / settings (id, theme, prefs)
- rag_documents (id, title, content, metadata)
- rag_embeddings (id, doc_id, embedding)
- llm_cache (id, prompt_hash, response, timestamp)
- api_keys (id, service, key_encrypted)
- prompts (id, name, template, description)
- tags (id, name)
- conversation_tags (conv_id, tag_id)
- attachments (id, message_id, file_path, metadata)
- sessions (id, user_id, token, expires_at)
- audit_logs (id, user_id, action, timestamp, details)
- notifications (id, user_id, message, is_read, created_at)
- user_preferences (id, user_id, pref_key, pref_value)
- rate_limits (id, user_id, limit_type, limit_value, period)
- billing_info (id, user_id, plan, next_billing_date)
- feature_flags (id, feature_name, is_enabled)
- app_settings (id, setting_key, setting_value)
- system_logs (id, log_level, message, timestamp)
- performance_metrics (id, metric_name, metric_value, recorded_at)
- integration_settings (id, service_name, config_json)
- data_backups (id, backup_date, file_path)
- maintenance_schedule (id, task_name, scheduled_at, status)
- user_sessions (id, user_id, login_time, logout_time)
- api_usage_stats (id, user_id, endpoint, call_count, period)
- error_reports (id, user_id, error_message, reported_at)
- feedback_entries (id, user_id, feedback_text, submitted_at)
- update_history (id, update_version, applied_at)
- third_party_tokens (id, service_name, token_encrypted)
- custom_commands (id, user_id, command_name, command_script)
- data_imports (id, source_name, import_date, status)
- scheduled_tasks (id, task_name, run_at, status)
- user_roles (id, user_id, role_name)
- access_logs (id, user_id, access_time, resource_accessed)
- system_configurations (id, config_key, config_value)
- performance_tuning (id, parameter_name, parameter_value)
- data_retention_policies (id, policy_name, retention_period)
- security_settings (id, setting_name, setting_value)
- audit_trails (id, user_id, action_taken, action_time)
- notification_settings (id, user_id, setting_key, setting_value)
- api_endpoints (id, endpoint_name, endpoint_url)
- user_activities (id, user_id, activity_type, activity_time)
- data_synchronization (id, source_name, last_sync_time)
- system_health_checks (id, check_name, status, checked_at)
- performance_logs (id, log_name, log_value, logged_at)
- data_encryption_keys (id, key_name, key_value_encrypted)
- feature_usage_stats (id, feature_name, usage_count, period)
- user_feedback_responses (id, user_id, response_text, responded_at)
- app_themes (id, theme_name, theme_settings_json)
