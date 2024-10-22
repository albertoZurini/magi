docker run --rm -i \
--gpus all \
--env DISPLAY=unix$DISPLAY  \
-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
-v $PWD:/src \
-v /usr/lib/dri:/usr/lib/dri \
-p 5678:5678 \
--privileged \
-t pytorch:dev \
python run_model.py
#python -m debugpy --listen 0.0.0.0:5678 --wait-for-client run_model.py

#--privileged --volume $XAUTH:/root/.Xauthority \
#--volume /tmp/.X11-unix:/tmp/.X11-unix \

# --volume="$HOME/.Xauthority:/root/.Xauthority:rw" \
# --device /dev/dri \
