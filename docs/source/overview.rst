Overview
========

Melissae is a distributed, modular honeypot framework built to emulate real-world network services. It uses a **manager/agent architecture** secured by **mTLS (mutual TLS)** to deploy honeypot sensors across multiple machines while centralizing analysis, threat scoring, and visualization on a single manager.

Each service module runs in its own container, allowing flexible deployment and isolated execution. Agents parse logs locally and push normalized JSON to the manager via encrypted channels. The manager centralizes data in MongoDB, runs threat intelligence scoring, and exposes everything through a dashboard.

The project includes a fully functional dashboard offering real-time visibility into attacker behavior, threat scoring, agent health monitoring, and IOC export, making Melissae not just a honeypot, but a lightweight distributed threat intelligence platform.

Key Features
------------

**Distributed Architecture**
   Deploy honeypot agents across multiple machines. Each agent runs honeypot modules, parses logs locally, and pushes normalized data to a central manager over mTLS-secured channels.

**Mutual TLS Security**
   All communications between agents and manager are authenticated using mutual TLS with an internal PKI (ECDSA P-384 certificates, auto-signed CA). Agent enrollment is handled via one-time tokens.

**Modular Service Support**
   Configure each agent to expose between 1 and 6+ services simultaneously. In addition to native honeypot modules, Melissae supports **CVE-specific modules**, purpose-built containers that reproduce real vulnerabilities. See :doc:`contributing` for developing new modules.

**Centralized Management Dashboard**
   Monitor and manage your honeypot fleet through a modern dashboard:

   - **Agent Health Monitoring** — Real-time status of all agents with module states, buffer status, and last push time.
   - **Auto-Refresh** — Dashboard and agents pages auto-refresh (30s / 15s) with live indicators.
   - **Statistical Analysis** — Visualize attack patterns with interactive charts: multi-day timelines, hourly activity, protocol doughnut, agent bar charts, and a day×hour heatmap.
   - **Trend Detection** — Stat cards show percentage change vs previous 24h with directional arrows.
   - **Top Credentials** — See the most attempted usernames across SSH/FTP/Telnet.
   - **Log Search** — Use the Melissae Query Language (MQL) to search within captured logs, with sortable columns, pagination, and agent filter.
   - **Logs Export** — Export logs in JSON format, filtered by time, service, IP, or agent.
   - **Threat Scoring** — Continuous 0-100 scoring engine with multi-factor confidence assessment and per-agent tracking.
   - **GeoIP Attack Map** — Interactive world map showing attack origins with threat markers colored by verdict and sized by score.
   - **GeoIP Enrichment** — Automatic geolocation of public IPs via ip-api.com batch API, cached in MongoDB, with country flags in the dashboard.
   - **STIX 2 Export** — Export Threat Intelligence IOCs as STIX 2.1 indicators directly from the dashboard.
   - **Killchain View** — Click any IP in Threat Intelligence to open an attack killchain timeline grouped by protocol.
   - **Automated Hygiene** — A purge removes benign IoCs unseen for 1h and their associated logs.


