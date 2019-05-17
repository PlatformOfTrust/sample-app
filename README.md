# Sample App

Note: This setup is only meant for running in minikube and for demo purposes only, not production ready.

## Quick overview

This is the main repository for sample-app app.
Follow this README to setup sample app and view basic features of Platform Of Trust.

    / - Root directory, contains README for setting up local development,
        Python invoke tasks
    /backend/* - Contains sample-app backend
    /frontend/* - Contains sample-app frontend

### Step 1: Install requirements 

- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Minikube](https://kubernetes.io/docs/setup/minikube/)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [Docker](https://docs.docker.com/get-started/)
- Pipenv `pip install pipenv`

### Step 2: Run sample app

#### Start Minikube:
```
minikube start --mount-string .:/src/sample-app --mount --memory=4096 --cpus=4
```

#### Set environment:
```
# Unix   
eval $(minikube docker-env)

# Windows:
# @FOR /f "tokens=*" %i IN ('minikube docker-env') DO @%i
```


Update `/etc/hosts` or `C:\Windows\System32\Drivers\etc\hosts`:
```
192.168.99.100 sample-app.local
```

Install the environment for running the local tools: 
```
pipenv install --dev
```

Configure `backend/setting.py`. You can get these values by registering your application in the [World application](https://world-sandbox.oftrust.net).

```
ACCESS_TOKEN = 'b739612b-29d8-4b4f-af3e-caf9d1528387'
CLIENT_SECRET = ‘bdMeUM-e3wuCAQ-ZDiZvGUs0OCSnrMXZWBxEyC2Xz4k’
CLIENT_ID = ‘c186a963-6eeb-44de-8bd6-01a8c600c757’
```

#### Run the app:
```
pipenv run invoke init
``` 

and hit 

`http://sample-app.local:32600/` in your browser.

That's it!

### Troubleshooting

### Minikube
Your minikube IP can be something else than `192.168.99.100`. You can check it with:
`minikube ip`.


#### Python
You might need to install Python 3.6.0. You can use `pyenv` to install version of python and set it as default.
