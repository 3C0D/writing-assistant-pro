#!/usr/bin/env python3
"""
Update translations using Babel (gettext)

Usage:
    uv run python scripts/translation_management/update_translations.py
    
This script automates the complete translation workflow:
1. Extract translatable strings from source code
2. Update/initialize translation files (.po)
3. Compile to binary format (.mo)
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Execute a command and handle errors"""
    print(f"\n{'='*70}")
    print(f"▶️  {description}")
    print(f"{'='*70}\n")
    
    result = subprocess.run(cmd, shell=True, cwd=str(Path(__file__).parent.parent.parent))
    
    if result.returncode != 0:
        print(f"\n❌ Erreur lors de : {description}")
        sys.exit(1)
    
    print(f"\n✅ {description} - OK\n")


def main():
    """Main workflow"""
    project_root = Path(__file__).parent.parent.parent
    translations_dir = project_root / "translations"
    src_dir = project_root / "src"
    
    print("\n" + "="*70)
    print("🌐 MISE À JOUR DES TRADUCTIONS AVEC BABEL")
    print("="*70 + "\n")
    
    # Step 1: Extract
    extract_cmd = f'uv run pybabel extract -F babel.cfg -k _ -o "{translations_dir}/template.pot" "{src_dir}"'
    run_command(
        extract_cmd,
        "🔍 Extraction des textes translatable"
    )
    
    # Step 2: Update/Initialize languages
    languages = ["en", "fr", "it"]
    domain = "writing_assistant"
    
    for lang in languages:
        po_file = translations_dir / lang / "LC_MESSAGES" / f"{domain}.po"
        
        if po_file.exists():
            # Update existing language
            update_cmd = f'uv run pybabel update -d "{translations_dir}" -i "{translations_dir}/template.pot" -l {lang} -D {domain}'
            run_command(
                update_cmd,
                f"🔄 Mise à jour des traductions {lang.upper()}"
            )
        else:
            # Initialize new language
            init_cmd = f'uv run pybabel init -d "{translations_dir}" -i "{translations_dir}/template.pot" -l {lang} -D {domain}'
            run_command(
                init_cmd,
                f"✨ Initialisation de la langue {lang.upper()}"
            )
    
    # Step 3: Compile
    compile_cmd = f'uv run pybabel compile -d "{translations_dir}" -D writing_assistant'
    run_command(
        compile_cmd,
        "⚙️  Compilation des traductions (.po → .mo)"
    )
    
    print("\n" + "="*70)
    print("✅ TRADUCTIONS MISES À JOUR AVEC SUCCÈS !")
    print("="*70)
    print(f"\nFichiers générés dans : {translations_dir}/")
    print("\nProchaines étapes :")
    print("1. Éditer les fichiers .po pour ajouter les traductions")
    print("2. Relancer ce script pour compiler")
    print("3. Relancer l'application\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Opération annulée par l'utilisateur")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
