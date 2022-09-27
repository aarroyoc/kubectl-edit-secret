#!/usr/bin/env python3
import argparse
import base64
import json
import os
import subprocess
import tempfile

def main():
    parser = argparse.ArgumentParser(description="Edit k8s secrets")
    parser.add_argument("secret_name", help="The name of the secret")
    parser.add_argument("-n", dest="namespace", action="store", required=True, help="Namespace of the secret")
    args = parser.parse_args()

    secret = download_secret(args.secret_name, args.namespace)
    print("Data sections found:")
    keys = secret["data"].keys()
    while True:
        for i,label in enumerate(keys):
            print(f"{i} - {label}")
        print("Select file to edit [Ctrl-D to exit]: ")

        try:
            selection = int(input())
            key = list(keys)[selection]
            decoded_text = base64.b64decode(secret["data"][key])
            edited_text = edit_section(decoded_text)
            encoded_text = base64.b64encode(edited_text).decode("utf8")
            patch_secret(args.secret_name, args.namespace, key, encoded_text)
            return
        except IndexError:
            print("Invalid selection, try again")
        except ValueError:
            print("Invalid selection, try again")
        except EOFError:
            return

def download_secret(secret_name, secret_namespace):
    secret_json = subprocess.run(["kubectl", "get", "secret", secret_name, "-n", secret_namespace, "-o", "json"], capture_output=True)
    return json.loads(secret_json.stdout)

def edit_section(text):
    editor = os.environ.get("EDITOR", "vim")
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(text)
        tf.flush()
        subprocess.call([editor, tf.name])
        tf.seek(0)
        edited_text = tf.read()
    return edited_text

def patch_secret(secret_name, secret_namespace, data_key, data_value):
    patch = f'{{"data": {{"{data_key}": "{data_value}"}}}}'
    subprocess.run(["kubectl", "patch", "secret", secret_name, "-n", secret_namespace, "-p", patch])
    
if __name__ == "__main__":
    main()
