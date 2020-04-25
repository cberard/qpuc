# qpuc
Des questions, plein de questions, rien que des questions ;)


## Deploy with Docker 

### Build 

```
docker build -t yourImageName .
```


### Run 

```
docker run -it --name yourContainerName -p 80:80 yourImageName:latest
```

### Preview

Si tout s'est bien passé, la console devrait afficher le message suivant : `[INFO] Listening at: http://0.0.0.0:80 ` (80 étant le port défini lors de la commande `docker run`.

In your navigator go to http://0.0.0.0/
