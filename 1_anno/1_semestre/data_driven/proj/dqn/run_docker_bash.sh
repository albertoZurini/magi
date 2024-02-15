docker run --rm -i \
--gpus all \
--env DISPLAY=unix$DISPLAY  \
-v /tmp/.X11-unix:/tmp/.X11-unix:rw --privileged \
--volume="$HOME/.Xauthority:/root/.Xauthority:rw" \
-v $PWD:/src \
--device /dev/dri --privileged \
\
-p 5678:5678 \
-t pytorch:dev \
python -m debugpy --listen 0.0.0.0:5678 --wait-for-client train.py

#--privileged --volume $XAUTH:/root/.Xauthority \
#--volume /tmp/.X11-unix:/tmp/.X11-unix \
