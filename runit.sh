docker run -it --rm  --network host \
    -v `pwd`/example-srv:/srv \
    -v `pwd`/src/:/app/ \
    -v /run:/run \
    --env-file ./.env \
    power_grader_publish_server