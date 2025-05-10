import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pokemon_classifier.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?\n"
            "Did you forget to activate your virtual environment?\n"
            "(venv) is not shown in your terminal prompt."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()