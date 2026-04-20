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

.. image:: https://github.com/user-attachments/assets/24b1101b-5360-4166-9c74-b13c459568aa
   :width: 400
   :alt: Dashboard overview

.. image:: https://github.com/user-attachments/assets/2eda0491-d2b4-4ffc-bc5f-0060878f03d3
   :width: 400
   :alt: Dashboard statistics

.. image:: https://github.com/user-attachments/assets/ee49fa9a-bafb-4885-9e69-c7fafc7b121d
   :width: 400
   :alt: Dashboard charts

.. image:: https://github.com/user-attachments/assets/c7d6bc68-8f2f-43bf-8bda-0c33e50d95ea
   :width: 400
   :alt: Agents page

.. image:: https://github.com/user-attachments/assets/7032151e-829c-428c-a9ff-621cb7fdc41b
   :width: 400
   :alt: GeoIP map

.. image:: https://github.com/user-attachments/assets/88e8264a-9316-4cbe-8680-5d145729c5a1
   :width: 400
   :alt: Search engine

.. image:: https://github.com/user-attachments/assets/71742a97-e00b-4cbb-b938-8578c7612f49
   :width: 400
   :alt: Threat intelligence

.. image:: https://github.com/user-attachments/assets/2a833ee5-7c64-4219-aee3-3fa98dab090c
   :width: 400
   :alt: Scoring details
