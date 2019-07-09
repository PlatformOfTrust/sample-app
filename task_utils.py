"""
Invoke task helper utilities.
"""
import sys
import tasks


def ensure_context(ctx, context=None) -> bool:
    """Make sure the user is running under the minikube context for dev!

    :param ctx: The invoke context.
    :type ctx: invoke.Context
    :param context: Kubernetes context.
    :type context: invoke.Context
    :return: True if we're in the correct context. If not, exit with 1.
    :rtype: bool
    """
    result = ctx.run('kubectl config current-context', hide=True)

    if context is None:
        context = tasks.CONTEXT

    if result.ok:
        if str(result.stdout).strip() == context:
            return True

    print(f'''
    WARNING: You are NOT running kubectl under the "{context}" context!
    Please be sure to set the context correctly!
    `kubectl config use-context {context}`
    ''')
    sys.exit(1)
