# uploooadit

Author Walkthrough: https://youtu.be/F4khES7KBR4

## Current Building Instructions

Build and deploy

```sh
docker build . -t uploooadit
docker run -it -p 8080:8080 --name uploooadit --rm uploooadit
```

## Run attack script

```sh
scripts/attack.py
```
