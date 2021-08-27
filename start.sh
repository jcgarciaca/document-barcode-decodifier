
## docker creation
docker build  --network="host" -t milleinnovacion/barcode_decoding:latest .

xhost local:root

docker run  -it --rm \
    --name  barcode_decoding  \
    --net="host"  \
    -v "$PWD":/var/www \
    -e DISPLAY=unix$DISPLAY \
    milleinnovacion/barcode_decoding:latest \
    /bin/bash  # -l -c "yarn run serve"

