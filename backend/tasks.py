from pathlib import Path
from invoke import task

# define projects directories
app_dir = Path('.')


@task
def dev(ctx):
    """Run the application (use when developing)."""
    ctx.run("pipenv install --dev")
    ctx.run("python application.py")
