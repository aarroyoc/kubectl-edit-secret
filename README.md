# kubectl-edit-secret

kubectl allows you to retrieve and modify the content of a secret, but it's a hassle because you need to decode base64, edit, recode again and modify the file. This tool allows you to do that for you, so you only need to edit the content of the secret.

## Usage

Instead of doing:
```
kubectl edit secret SECRET_NAME -n SECRET_NAMESPACE
```

Do:
```
./kubectl-edit-secret.py SECRET_NAME -n SECRET_NAMESPACE
```