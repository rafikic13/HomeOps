# HomeOps
# Home Server Lab

A complete homelab built around pfSense, Ubuntu Server, Docker, monitoring, security, remote access, and custom Python automation.

## Project Overview

This project combines network infrastructure, firewalling, self-hosted services, monitoring, alerting, and custom automation into one integrated home server environment.

The main components are:

- pfSense firewall and router
- Managed network switch
- Wireless access point
- Ubuntu Server
- Docker-based services
- Prometheus and Grafana monitoring
- Uptime Kuma alerts
- Suricata intrusion detection
- Tailscale remote access
- HomeOps Python control plane

## High-Level Topology

```text
Internet
   |
ISP Modem
   |
pfSense Firewall
   |
Managed Switch
   |
   +-- Ubuntu Server
   +-- Wireless Access Point
   +-- Other LAN Devices
