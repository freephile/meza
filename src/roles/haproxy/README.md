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
| `haproxy_stats_allowed_networks` | (unset) | List of additional CIDRs allowed to reach the stats port, e.g. `["203.0.113.0/24"]`. Localhost and all RFC-1918 ranges are always permitted. |
| `m_install_netdata` | — | When true, adds a Netdata frontend on port 20000 |
| `m_private_networking_zone` | `public` | firewalld zone used for inter-server firewall rules |
| `wiki_app_fqdn` | — | FQDN used in the self-signed cert CN and `$wgServer` |
| `haproxy_rate_limit_table_size` | `100k` | Stick table capacity — number of source IPs to track simultaneously |
| `haproxy_rate_limit_window` | `10s` | Sliding window duration for all rate counters and record expiry |
| `haproxy_rate_limit_requests` | `900` | Max HTTP requests per IP per window before deny |
| `haproxy_rate_limit_errors` | `20` | Max HTTP error responses (4xx/5xx) per IP per window before deny |
| `haproxy_rate_limit_bytes_out` | (unset) | Max bytes sent to a single IP per window before deny. **Disabled by default** — MediaWiki category pages easily exceed conservative thresholds. Set as a plain integer (bytes) to enable, e.g. `104857600` = 100 MiB. HAProxy 1.8 does not accept `k`/`m` shorthand. |
| `haproxy_blocked_bots` | (see `defaults/main.yml`) | List of User-Agent substrings to block. Defined in `defaults/main.yml`; override the entire list in `public.yml` if needed. To **add** bots without replacing the defaults, use `haproxy_extra_blocked_bots` instead. |
| `haproxy_extra_blocked_bots` | (unset) | Additional User-Agent substrings to block, merged with `haproxy_blocked_bots`. Entries containing spaces are automatically single-quoted by the template. |

## Rate limiting and bot blocking

The `www-https` frontend applies two layers of protection before a request
reaches Apache:

1. **User-Agent blocking** — a static ACL matches known AI scrapers, SEO
   crawlers, and other abusive bots by User-Agent substring and denies them
   immediately, before any stick-table overhead.
2. **Stick-table rate limiting** — an in-memory table tracks three per-IP
   counters over a sliding window and denies requests that exceed any threshold.

### Bot blocking

The default bot list is defined in `defaults/main.yml` as `haproxy_blocked_bots`.
The following User-Agent substrings are blocked out of the box:

`AhrefsBot`, `Amazonbot`, `anthropic-ai`, `Aranet`, `BaiduSpider`, `BLEXBot`,
`Bytespider`, `CCBot`, `ChatGPT`, `ClaudeBot`, `DataForSeoBot`, `DotBot`,
`DuckAssistBot`, `GenomeCrawlerd`, `Google-Extended`, `GPTBot`,
`meta-externalagent`, `meta-webindexer`, `MJ12bot`, `PerplexityBot`, `PetalBot`,
`Quantbot`, `SemrushBot`, `SERankingBacklinksBot`, `SeznamBot`, `Sogou`,
`TikTokSpider`, `YandexBot`, `YisouSpider`

To **add** bots without replacing the default list, set `haproxy_extra_blocked_bots`
in `public.yml`:

```yaml
haproxy_extra_blocked_bots:
  - MyBadBot
  - Sogou web spider   # spaces are safe — the template wraps them in single quotes
```

To **replace** the default list entirely, override `haproxy_blocked_bots` in `public.yml`.

> **Important:** All entries are single-quoted in the rendered haproxy.cfg
> (e.g. `'GPTBot'`, `'Sogou web spider'`). YAML quotes (`"MyBadBot"` or
> `'MyBadBot'`) are stripped by the YAML parser before Jinja2 sees the value,
> so there is no risk of double-quoting. The single quotes in the HAProxy config
> ensure multi-word strings are matched as a complete substring rather than
> having each space-separated word treated as a separate OR pattern.

> **Note:** Bot UA blocking only works against crawlers that honestly
> self-identify. Sophisticated scrapers that spoof common browser UAs will
> not be caught here — the rate-limit layer handles those.

### Stick-table rate limiting

Three counters are stored per IP over the configured window:

| Counter | Directive | Default threshold | Notes |
|---|---|---|---|
| Request rate | `sc_http_req_rate(0)` | `900` req / window | Catches volumetric floods |
| Error rate | `sc_http_err_rate(0)` | `20` err / window | Catches scanners probing for 404s/403s |
| Bytes out | `sc_bytes_out_rate(0)` | `10485760` bytes / window | Catches bandwidth-heavy scrapers; value must be a plain integer (bytes) — HAProxy 1.8 does not accept `k`/`m` shorthand |

> **HAProxy 1.8 compatibility notes:**
> - `glitch_rate` is **not** available until HAProxy 2.x — do not add it.
> - `bytes_out_rate` thresholds must be plain integer bytes, not `1m`/`10m`.

### Generated HAProxy directives (defaults)

```
stick-table type ip size 100k expire 10s store http_req_rate(10s),http_err_rate(10s),bytes_out_rate(10s)
http-request track-sc0 src
http-request deny if { sc_http_req_rate(0) gt 900 }
http-request deny if { sc_http_err_rate(0) gt 20 }
http-request deny if { sc_bytes_out_rate(0) gt 10485760 }
```

### Tuning

```yaml
# Tighten for a low-traffic wiki; loosen for a busy public site.
# Note: Some Category or Special pages can generate ~100 requests per page view.
haproxy_rate_limit_requests: 600
haproxy_rate_limit_errors: 10
haproxy_rate_limit_bytes_out: 52428800   # 50 MiB per 10s
haproxy_rate_limit_window: "10s"
haproxy_rate_limit_table_size: "100k"
```

### Accessing the stats dashboard

The stats port uses SSL. Use `https://` and `-k` (or supply your cert):

```bash
curl -k -u 'admin:password' 'https://127.0.0.1:1936/haproxy?stats'
```
Forward the port so you can access it in your browser, and still use https://

> **Note:** The stick table lives only in HAProxy's process memory. It is not
> shared between multiple load balancer nodes — each node tracks IPs
> independently. For multi-LB deployments consider a shared peer table or an
> upstream rate-limiting layer.

## SSL certificate hierarchy

1. If `use_certbot: true` — Let's Encrypt cert managed by
   `ansible-role-certbot-meza`; ACME challenge proxied to localhost:54321.
2. Otherwise — self-signed cert generated on the controller and stored
   (Vault-encrypted) in `conf-meza/secret/<env>/ssl/meza.{crt,key}`.

The assembled PEM file is always placed at `/etc/haproxy/certs/meza.pem` with
`0600` permissions.
