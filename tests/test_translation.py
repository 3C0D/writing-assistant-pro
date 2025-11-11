#!/usr/bin/env python3
"""
Test script for the translation system.
This script tests the basic functionality of the language management system.
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.translation import init_translation, _, change_language, get_current_language
from src.core.translation import get_language_manager


def test_translation_system():
    """Test the translation system functionality."""
    print("=" * 60)
    print("TESTING TRANSLATION SYSTEM")
    print("=" * 60)
    
    # Initialize the translation system
    print("\n1. Initializing translation system...")
    try:
        language_manager = init_translation("writing_assistant", "translations", "en")
        print("[OK] Translation system initialized successfully")
    except Exception as e:
        print(f"[ERROR] Error initializing translation system: {e}")
        return False
    
    # Test basic translation functionality
    print("\n2. Testing basic translation functionality...")
    test_strings = [
        "My Application",
        "My Application (DEV MODE)",
        "Hello, this is a real desktop app!",
        "Click me",
        "Clicked!!!",
        "Language",
        "Select Language",
        "English",
        "Francais",
        "Italiano",
        "Configuration: DEBUG=",
        "Interface created successfully",
        "Error",
        "Success",
        "Warning",
        "Information"
    ]
    
    for test_string in test_strings:
        translated = _(test_string)
        print(f"'{test_string}' -> '{translated}'")
    
    # Test language switching
    print("\n3. Testing language switching...")
    languages = ["en", "fr", "it"]
    
    for lang in languages:
        print(f"\n--- Switching to {lang} ({get_language_manager().get_language_name(lang)}) ---")
        try:
            change_language(lang)
            current = get_current_language()
            print(f"Current language: {current}")
            
            # Test some key translations
            key_translations = [
                "My Application",
                "Click me",
                "Language",
                "Error"
            ]
            
            for key in key_translations:
                translated = _(key)
                print(f"  '{key}' -> '{translated}'")
                
        except Exception as e:
            print(f"[ERROR] Error switching to {lang}: {e}")
            return False
    
    print("\n4. Testing edge cases...")
    try:
        # Test invalid language (should fallback to default)
        print("Testing invalid language...")
        change_language("invalid_lang")
        current = get_current_language()
        print(f"Current language after invalid: {current}")
        
        # Test getting language name for invalid language
        invalid_name = get_language_manager().get_language_name("invalid_lang")
        print(f"Name for invalid language: '{invalid_name}'")
        
    except Exception as e:
        print(f"[WARN] Warning in edge case testing: {e}")
    
    print("\n" + "=" * 60)
    print("TRANSLATION SYSTEM TEST COMPLETED")
    print("=" * 60)
    return True


def test_locale_files():
    """Test that locale files exist and are accessible."""
    print("\n" + "=" * 60)
    print("TESTING LOCALE FILES")
    print("=" * 60)
    
    locales_dir = Path("translations")
    expected_files = [
        "en/LC_MESSAGES/writing_assistant.po",
        "fr/LC_MESSAGES/writing_assistant.po",
        "it/LC_MESSAGES/writing_assistant.po"
    ]
    
    for file_path in expected_files:
        full_path = locales_dir / file_path
        if full_path.exists():
            print(f"[OK] {file_path} exists")
            # Basic file size check
            size = full_path.stat().st_size
            if size > 100:  # Should be more than 100 bytes
                print(f"   File size: {size} bytes (good)")
            else:
                print(f"   [WARN] File size: {size} bytes (might be too small)")
        else:
            print(f"[ERROR] {file_path} NOT FOUND")
            return False
    
    print("\n" + "=" * 60)
    print("LOCALE FILES TEST COMPLETED")
    print("=" * 60)
    return True


def main():
    """Main test function."""
    print("Starting translation system tests...")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python version: {sys.version}")
    
    # Test locale files first
    locale_test_passed = test_locale_files()
    
    if not locale_test_passed:
        print("\n[ERROR] Locale files test failed. Please check your locale files.")
        return False
    
    # Test translation system
    translation_test_passed = test_translation_system()
    
    if translation_test_passed:
        print("\n[SUCCESS] All tests passed! The translation system is working correctly.")
        return True
    else:
        print("\n[ERROR] Some tests failed. Please check the translation system.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)