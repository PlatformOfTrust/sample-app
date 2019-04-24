from pathlib import Path
from invoke import task
import task_utils as utils
from typing import List

CURRENT_PATH = Path('.')
KUBE_PATH = Path('./kube/')
CONTEXT = 'minikube'
NAMESPACE = 'sample-app'

ALL_BUILDS = ['backend', 'frontend', 'services']


def build_images(ctx, context=None) -> List[str]:
    """Builds the docker images for apis, services, apps.

    :param ctx: The invoke context.
    :type ctx: invoke.Context
    :return: None
    :rtype: None
    """
    utils.ensure_context(ctx, context)

    images = []

    for docker_path in ALL_BUILDS:

        docker_path = Path(docker_path)

        for docker_file in docker_path.rglob('Dockerfile'):
            # The path to the Dockerfile.
            path = docker_file.parent
            print(f'\nBuilding docker image in {path}.')

            # Get the parent folder name.
            image_name = f'{NAMESPACE}-{docker_file.parts[-2]}'
            ctx.run(f'docker build -t {image_name} {path}/')

            images.append(image_name)

    return images


def show_help() -> None:
    """Shows the help dialog.

    :return: None
    :rtype: None
    """
    print(f'''
    The host's path "{CURRENT_PATH.absolute()}/"
    is mounted on the minikube instance on path "/src/sample-app".

    Whenever you make changes in the code, the python application will
    automatically reload.

    Access to services:
        Minikube instance:  `minikube ssh`
        Sample-app:         http://sample-app.local:32600

    To see the logs for a pod, use `kubectl -n {NAMESPACE} get pods` and then
    `kubectl -n {NAMESPACE} logs <POD_NAME>`

    ''')


@task
def apply(ctx):
    """Applies kubernetes configurations.

    :param ctx: The invoke context.
    :type ctx: invoke.Context
    :return: None
    :rtype: None
    """
    print(f'Clean and apply kubernetes configuration')

    utils.ensure_context(ctx)

    files = [
        f'{KUBE_PATH}/namespace.yaml',
        f'{KUBE_PATH}/sample-app.yaml',
        f'{KUBE_PATH}/haproxy.yaml'
    ]

    for yaml_file in files:
        ctx.run(f'kubectl delete -f {yaml_file} --ignore-not-found=true')

    for yaml_file in files:
        ctx.run(f'kubectl apply -f {yaml_file}')


@task
def init(ctx):
    """Initialize the environment. Runs also invoke init on given app name.

    Deletes all k8s configurations, builds all images, applies the k8s
    configurations and runs the invoke init command on pods.

    :return: None
    :rtype: None
    """
    utils.ensure_context(ctx)

    build_images(ctx)
    apply(ctx)

    show_help()
