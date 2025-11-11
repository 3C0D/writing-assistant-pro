"""
Configuration centralisée du logging pour l'application.
"""

import logging
import sys


def setup_logger(debug: bool, name: str = "WritingAssistant") -> logging.Logger:
    """
    Configure et retourne un logger pour l'application.
    
    Args:
        debug: True pour activer le mode DEBUG (logs détaillés), False pour logs minimalistes
        name: Nom du logger
    
    Returns:
        Logger configuré
    """
    logger = logging.getLogger(name)
    
    # Éviter les handlers dupliqués
    if logger.handlers:
        return logger
    
    if debug:
        # Mode DEBUG : logs détaillés avec timestamp et niveau
        log_level = logging.DEBUG
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    else:
        # Mode production : logs simples
        log_level = logging.INFO
        log_format = "%(levelname)s - %(message)s"
    
    # Créer un handler pour afficher les logs dans la console
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    
    # Créer un formateur
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    
    # Configurer le logger
    logger.setLevel(log_level)
    logger.addHandler(handler)
    
    if debug:
        logger.debug("DEBUG Mode enabled - Detailed logging")
    
    return logger
