# Server

Root directory for all code that will be ran on infrastructure servers.

## Makefile

Check [Makefile](Makefile) for more extensive comments on targets. Below will show you how to start the services. Watch the `qlogd` logs and send test data to broker.

```bash
$ make build # will pull base images and build defined services
$ make up # will start all services defined in docker-compose.yml
$ make watchq # will follow the log file for qlogd

# In another terminal
$ make test # Sends test message to broker
$ make ps # use this to find container name for the watchq target
$ docker kill CONTAINER # to kill container watching qlogd logs
$ make down # stops all services
```
