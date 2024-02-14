docker run --rm -i \
--gpus all \
--env DISPLAY=unix$DISPLAY  \
--privileged --volume $XAUTH:/root/.Xauthority \
--volume /tmp/.X11-unix:/tmp/.X11-unix \
\
-v $PWD:/src \
-t pytorch:dev \
bash