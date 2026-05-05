# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A small Python agent that runs in Docker and reports liveness to an Uptime Kuma "Push" monitor. Each interval it pings a configured IP, parses the average RTT, and sends a GET to the Uptime Kuma push URL with `?status=up&msg=OK&ping=<rtt>`. The agent is the *client* — Uptime Kuma is the server and is not part of this repo.

## Architecture

The whole agent is `app/app.py` (~85 lines). Key flow:

1. Reads `PUSH_URL`, `PUSH_INTERVAL`, `PING_IP` from env (overridable via CLI flags `--push_url`, `--push_interval`, `--isp`).
2. Uses `pingparsing.PingTransmitter` (count=1) to ping the target and `PingParsing` to extract `rtt_avg`.
3. Appends `?status=up&msg=OK&ping=<rtt>` to `PUSH_URL` and issues a `requests.get`. On ping failure, sends `ping=N/A` (status is still `up` — the push itself is the heartbeat).
4. Scheduling is done via the `schedule` library in a `while True: run_pending(); sleep(1)` loop. `main()` is called once at startup, then on each interval.

`PUSH_URL` must be the bare push endpoint up to the alphanumeric token — query params are appended by the agent. `PING_IP` should *not* be the host being monitored (you'd be pinging yourself); default is `8.8.8.8`.

## Common commands

Runtime is Docker Compose. From the repo root:

```
make up      # docker-compose up -d
make down    # docker-compose down
make pull    # pull latest ripl/uptimekuma-push-agent from Docker Hub
make update  # pull + down + remove + up
make help    # list targets
```

Image build/release (multi-arch arm64 + amd64 via buildx):

```
make build   # local build, both platforms
make release # build + push to docker.io/ripl/uptimekuma-push-agent
```

## Configuration

`config.env` (gitignored) supplies env vars to the container via `docker-compose.yaml`. Required keys: `PUSH_URL`, `PUSH_INTERVAL`, `PING_IP`. The committed `config.env` in history is an example — real deployments must create their own. There is no test suite, lint config, or CI in this repo.

`systemd/uptimekuma-push-agent.service` is a template unit for auto-starting on Ubuntu hosts. It's `Type=oneshot` + `RemainAfterExit=yes` wrapping `make up` / `make down` — operators must edit `WorkingDirectory=` to match their clone path before installing. README has the install steps.
