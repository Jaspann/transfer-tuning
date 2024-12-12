#### Docker 

Create the Docker image with:

``` sh
docker build -t transfer-tuning/tvm:latest -f docker/Dockerfile . 
```

Run the shell for the container in the directory above this:

``` sh
sudo docker run \
    --gpus all \
    --ipc=host \
    -e NVIDIA_VISIBLE_DEVICES=1 \
    -v ${PWD}/:/workspace \
    -p 8888:8888 -p 9190:9190 \
    -ti transfer-tuning/tvm:latest bash -i
```
