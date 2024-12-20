#!/usr/bin/env python
"""FastTower's command-line utility for administrative tasks."""
import os


def main():
    """Run administrative tasks."""
    os.environ.setdefault("FASTTOWER_SETTINGS_MODULE", "example.settings")
    try:
        from fasttower.cli import app
        app()
    except ImportError as exc:
        raise ImportError(
            "Couldn't import FastTower. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc


if __name__ == '__main__':
    main()