"""
Theme and style management for the application.
Flet uses native theming, so this module is largely simplified.
"""

from loguru import logger

log = logger.bind(name="WritingAssistant.Styles")

# Flet handles theming directly via page.theme_mode
# This file is kept for potential future custom style logic
