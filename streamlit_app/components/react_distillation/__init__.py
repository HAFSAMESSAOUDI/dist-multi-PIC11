"""
Streamlit Component pour l'interface React de distillation multicomposants
"""
import os
import streamlit.components.v1 as components

# Déclarer le composant
_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "react_distillation",
        url="http://localhost:3000",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        "react_distillation",
        path=build_dir
    )


def react_distillation(compounds_data, key=None):
    """
    Affiche le composant React de distillation multicomposants

    Parameters
    ----------
    compounds_data : dict
        Données des composés et configuration
    key : str or None
        Clé unique pour le composant

    Returns
    -------
    dict or None
        Données de simulation reçues du composant React
    """
    component_value = _component_func(
        compounds_data=compounds_data,
        key=key,
        default=None
    )

    return component_value
