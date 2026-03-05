# haproxy role

Installs and configures HAProxy as the TLS-terminating load balancer for Meza
MediaWiki deployments.

## Purpose

HAProxy sits in front of all app servers and:

- Terminates SSL/TLS (port 443) using either a self-signed cert or a Let's
  Encrypt cert managed by `ansible-role-certbot-meza`.
- Redirects all HTTP (port 80) to HTTPS.
- Distributes requests to Apache on each app server (port 8080).
- Optionally serves an internal-only MediaWiki listener (port 8081) for
  server-to-server requests that should bypass the public load balancer.
- Optionally exposes a statistics dashboard (port 1936, SSL).
- Optionally proxies Netdata dashboards (port 20000, SSL).

## Role responsibilities

1. **SSL certificate management** — Checks for an existing cert/key in the
   controller's secret config (`conf-meza/secret/<env>/ssl/`). If none exists,
   generates a self-signed cert. Encrypts both with Ansible Vault and assembles
   them into `/etc/haproxy/certs/meza.pem`.
2. **HAProxy config** — Renders `/etc/haproxy/haproxy.cfg` from
   `templates/haproxy.cfg.j2`, conditioned on whether this node handles
   external and/or internal connections.
3. **Firewalld rules** — Opens ports 80 and 443 to the world on external load
   balancers. Opens/closes port 1936 for stats based on `enable_haproxy_stats`.
   Firewalld service definition XML files are written to
   `/etc/firewalld/services/` for RedHat systems.
4. **Logging** — Configures rsyslog to accept UDP on 514 and writes
   `/etc/rsyslog.d/haproxy.conf` so HAProxy log traffic is captured.
5. **Custom error pages** — Deploys templated error pages under
   `/etc/haproxy/errors/`.

## Ports

| Port  | Protocol | Condition | Description |
|-------|----------|-----------|-------------|
| 80    | TCP      | External LB only | HTTP — immediately redirected to HTTPS |
| 443   | TCP      | External LB only | HTTPS — TLS termination, proxies to app servers on :8080 |
| 8081  | TCP      | Internal LB only | Internal MediaWiki listener — proxies to app servers on :8080 without external exposure |
| 1936  | TCP      | `enable_haproxy_stats: true` | HAProxy statistics dashboard (SSL) |
| 20000 | TCP      | `m_install_netdata: true` | Netdata reverse proxy (SSL) |
| 54321 | TCP      | localhost only | Let's Encrypt ACME challenge backend |
| random high | UDP | Always | Internal syslog logging socket (see note below) |

### Note on the random high UDP port

When inspecting open ports with:

```bash
sudo netstat -tulnp | grep haproxy
# or
sudo ss -tulnp | grep haproxy
```

You will see a UDP entry on a random high-numbered port similar to:

```
udp  0  0  0.0.0.0:47161  0.0.0.0:*  969715/haproxy
```

This is **not a listening service**. HAProxy opens an ephemeral UDP socket to
forward its internal log stream to the local syslog daemon (`127.0.0.1 local2`
in `haproxy.cfg`). The port number is assigned by the kernel at startup and
changes on each restart. It is not an attack surface and cannot be removed
without disabling HAProxy logging entirely.

## Integration in Meza

HAProxy is invoked from `src/playbooks/site.yml` in the
`Configure load balancers` play, which targets the `load_balancers`,
`load_balancers_meza_internal`, and `load_balancers_meza_external` inventory
groups.

**Load balancer types:**

| Inventory group | External (80/443) | Internal (8081) |
|-----------------|:-----------------:|:---------------:|
| `load_balancers` | Yes | Yes |
| `load_balancers_meza_external` | Yes | No |
| `load_balancers_meza_internal` | No | Yes |
| `load_balancers_nonmeza` | — (unmanaged) | — |
| `load_balancers_nonmeza_external` | — (unmanaged) | — |

App servers listen on port 8080. The firewall on each app server is opened to
allow connections from the load balancer group on that port (configured in
`site.yml` via the `firewall_port` role before the `mediawiki` role runs).

## Key configuration variables

| Variable | Default | Description |
|----------|---------|-------------|
| `use_certbot` | `false` | Use Let's Encrypt instead of self-signed cert |
| `enable_haproxy_stats` | `false` | Enable stats dashboard on port 1936 |
| `haproxy_stats_user` | `admin` | Stats dashboard username |
| `haproxy_stats_password` | `password` | Stats dashboard password — override in `secret.yml` |
| `m_install_netdata` | — | When true, adds a Netdata frontend on port 20000 |
| `m_private_networking_zone` | `public` | firewalld zone used for inter-server firewall rules |
| `wiki_app_fqdn` | — | FQDN used in the self-signed cert CN and `$wgServer` |

## SSL certificate hierarchy

1. If `use_certbot: true` — Let's Encrypt cert managed by
   `ansible-role-certbot-meza`; ACME challenge proxied to localhost:54321.
2. Otherwise — self-signed cert generated on the controller and stored
   (Vault-encrypted) in `conf-meza/secret/<env>/ssl/meza.{crt,key}`.

The assembled PEM file is always placed at `/etc/haproxy/certs/meza.pem` with
`0600` permissions.
