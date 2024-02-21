docker run -it --rm  --network power_grader_architecture \
    -v `pwd`/example-srv:/srv \
    -v `pwd`/src/:/app/ \
    -v /run:/run \
    --env-file ./.env \
    power_grader_publish_server