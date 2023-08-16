docker-compose run --rm test
docker-compose down
docker-compose -f docker-compose-sentinel.yml run --rm test
docker-compose -f docker-compose-sentinel.yml down