# Uptime Kuma Push Agent

**[Uptime Kuma](https://github.com/louislam/uptime-kuma)** is an open-source status monitoring tool designed to keep an eye on various services and systems. It provides a web-based interface for visualizing the status of monitored services, making it easier for administrators and users to check the health and performance of their systems.

## Key features of Uptime Kuma:

* **Web Interface:** Uptime Kuma typically offers a user-friendly web interface where you can view the status of monitored services.

* **Service Monitoring:** It allows you to monitor the status of different services, servers, or websites.

* **Alerts:** Uptime Kuma often comes with alerting capabilities, notifying administrators or users when there's a service disruption or downtime

* **Historical Data:** The tool may also store historical data, allowing you to review the performance of your services over time.

* **Customization:** Depending on the version and updates, Uptime Kuma might offer customization options for configuring monitoring parameters.


## Uptime Kuma push agent 

A "push" monitor in Uptime Kuma typically refers to a monitoring mechanism where the monitored service actively pushes its status updates to the Uptime Kuma server. This is in contrast to the more traditional "Pull" method, where the monitoring system periodically checks the status of services by making requests.

In a "Push" monitoring setup with Uptime Kuma:

* **Monitored Service:** The service being monitored actively sends status updates to the Uptime Kuma server.

* **Uptime Kuma Server:** Uptime Kuma receives and processes these status updates from the monitored services.

* **Real-time Monitoring:** With the "Push" method, Uptime Kuma can receive real-time updates about the status of services, enabling quicker detection of issues or outages. In addition to providing an indication as to whether the service is up, the agent is configured to provide the time associated with pinging a specified IP from the agent.

* **Reduced Polling Load:** Unlike the "Pull" method, where the monitoring system repeatedly polls services for their status, the "Push" method reduces the need for frequent requests, potentially lowering the overall load on both the monitoring system and the monitored services.

## Using the Uptime Kuma push agent via Docker

1. Create a new push monitor in Uptime Kuma by clicking on '+ Add New Monitor' in the upper-left of the screen and configure it as follows:

* **Monitor Type:** Choose "Push"
* **Friendly Name:** Choose a name for that identifies the monitor (e.g., the hostname of the machine you would like to monitor)
* **Push URL:** This auto-populated field contains the URL that needs to be configured in the remote agent as described below.
* **Heartbeat Interval:** The time interval Uptime Kuma will expect to pass between interactions with the agent. The default for Uptime Kuma and this push agent is 60s.

Click on 'Save' at the bottom of the screen to save the settings.

2. Clone this repo on the client
3. Within the `uptimekuma-push-agent` folder on the client, create a `config.env` file that defines the following environment variables

```make
PUSH_URL=<YOUR_URL_HERE> 
PUSH_INTERVAL=<YOUR_INTERVAL_HERE> # Interval between pings in seconds. Default is set to 60 seconds.
PING_IP=<YOUR_IP_TO_PING_HERE> # Default is 8.8.8.8
```
where 

* `PUSH_URL` should be set to the "Push URL" created by Uptime Kuma when you created the monitor above **only up to and including the unique alphanumeric identifier** (i.e., do not include `?status=up...` since this gets appended automatically by the push agent)
* `PUSH_INTERVAL` should be set to the "Heartbeat Interval" configured in the Uptime Kuma monitor
* `PING_IP` (optional) can be set to the IP address that you would like the push agent to ping. **It should not be set to the IP of the machine being monitored**

4. At this point, you can run the push agent by calling `make up` within the `uptimekuma-push-agent` folder.
   

**Note**: The `Makefile` includes targets for things like updating the image, bringing down the container, etc. To see the list of available targets, run `make help`

## Running automatically on boot (Ubuntu / systemd)

To have the agent come up on every boot without running `make up` by hand, install the systemd unit included in `systemd/uptimekuma-push-agent.service`:

1. Make sure Docker itself starts at boot:
   ```
   sudo systemctl enable --now docker
   ```
2. Edit `systemd/uptimekuma-push-agent.service` and set `WorkingDirectory=` to the absolute path where you cloned this repo (e.g. `/opt/uptimekuma-push-agent` or `/home/<user>/uptimekuma-push-agent`). Make sure `config.env` exists in that directory.
3. Install and enable the unit:
   ```
   sudo cp systemd/uptimekuma-push-agent.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now uptimekuma-push-agent
   ```

Useful commands afterwards:

* `systemctl status uptimekuma-push-agent` — check whether the unit is active
* `journalctl -u uptimekuma-push-agent` — view start/stop logs from the unit itself
* `docker logs -f uptimekuma-push-agent` — follow live logs from the running container
* `sudo systemctl stop uptimekuma-push-agent` — equivalent to `make down`

## Acknowledgements

This repo was forked from [t0mer/uptimekuma-agent](https://github.com/t0mer/uptimekuma-agent) and was updated to use ping based on the Uptime Kuma push agent of [carlbomsdata/uptime-kuma-agent](https://github.com/carlbomsdata/uptime-kuma-agent/tree/main).
