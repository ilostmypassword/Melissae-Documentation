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

Screenshots
-----------

.. image:: https://github.com/user-attachments/assets/cb5ee4c9-2710-4165-b9cb-f520ab26f814
   :width: 400
   :alt: Overview Dashboard

.. image:: https://github.com/user-attachments/assets/e22d8471-272a-4336-9584-714227eb5cbc
   :width: 400
   :alt: Statistics & Charts

.. image:: https://github.com/user-attachments/assets/2b738ee8-3032-4a17-87ae-c8ae0c66859f
   :width: 400
   :alt: Agents Management

.. image:: https://github.com/user-attachments/assets/fe45fbeb-29dc-452e-ab4d-63d7b2b71750
   :width: 400
   :alt: GeoIP Attack Map

.. image:: https://github.com/user-attachments/assets/9ffaaf3d-7195-422c-b4aa-60bf2772285c
   :width: 400
   :alt: GeoIP Attack Map (detail)

.. image:: https://github.com/user-attachments/assets/146e7fab-bdd7-46f2-b52d-cd5d22ba1764
   :width: 400
   :alt: Search Engine

.. image:: https://github.com/user-attachments/assets/a5ba43c9-e668-404c-bf7f-631c290e9aeb
   :width: 400
   :alt: Threat Intelligence

.. image:: https://github.com/user-attachments/assets/09ed8e3c-9baa-47fc-821f-b92d5cac41c9
   :width: 400
   :alt: Threat Intelligence (detail)
