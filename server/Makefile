DC=docker-compose
DK=docker
DLS=$(shell docker ps -aq)

# Build images
build:
	$(DC) pull
	$(DC) build

# Run services
up:
	$(DC) up -d

# Stop services
down:
	$(DC) down

# List containers running
ps:
	$(DC) ps

# List images
img:
	$(DK) images

# Remove all containers
rm:
	docker stop $(DLS)
	$(DK) rm $(DLS)

# Remove untagged images
rmn:
	$(DK) rmi $(shell $(DK) images -a | grep "^<none>" | awk '{print $3}')

# Run test command on CLI
test:
	$(DC) run --rm cli python app.py test

# Run qlogd services
runq:
	$(DC) run --rm qlogd

# Watch qlogd log file
# This requires "docker kill CONTAINER_NAME" from another terminal to exit
watchq:
	$(DC) run --rm qlogd tail -f /var/app/qlogd.log

# Logs for qlogd
logq:
	$(DC) logs qlogd

# Watch logs for qlogd
wlogq:
	$(DC) logs -f qlogd

# Logs for db
logdb:
	$(DC) logs db

# Watch logs for db
wlogdb:
	$(DC) logs -f db

# Logs for broker
logb:
	$(DC) logs broker

# Watch broker logs
wlogb:
	$(DC) logs -f broker

# Check logs for web
logweb:
	$(DC) logs web

# Watch logs for web
wlogweb:
	$(DC) logs -f web

# Enter web container
bashweb:
	$(DC) exec web bash

# Run tests on web container
testroutes:
	$(DC) exec web python test_routes.py

sql:
	$(DC) exec db mysql -u root -p
