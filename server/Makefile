DC=docker-compose
DK=docker

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

# Run test command on CLI
test:
	$(DC) run cli python app.py test

# List containers running
ps:
	$(DC) ps

# Run qlogd services
runq:
	$(DC) run qlogd

# Watch qlogd log file
# This requires "docker kill CONTAINER_NAME" from another terminal to exit
watchq:
	$(DC) run qlogd tail -f /var/app/qlogd.log

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
