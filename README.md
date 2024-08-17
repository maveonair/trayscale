# Trayscale

A simple Tailscale systray utility for KDE Plasma:

![plasma-panel-with-trayscale](docs/plasma-panel.png)

## Requirements

Tailscale must be started with the current user:

```bash
$ sudo tailscale set --operator=$USER
```
## Developer Setup

```
python3 -m venv --system-site-packages .venv/
source env/bin/activate
```
