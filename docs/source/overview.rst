Overview
========

Melissae is a distributed, modular honeypot framework built to emulate real-world network services. It uses a **manager/agent architecture** secured by **mTLS (mutual TLS)** to deploy honeypot sensors across multiple machines, while centralizing analysis, rule-based alerting, and visualization on a single manager node.

Each service module runs in its own container, enabling flexible deployment and isolated execution. Agents parse logs locally and push normalized JSON to the manager over encrypted channels. The manager stores data in MongoDB, runs a **rule-based alerting engine** that evaluates declarative YAML detection rules against ingested logs, and serves a React dashboard.

----

Key Features
------------

.. rubric:: Distributed Architecture

Deploy honeypot agents across multiple machines. Each agent runs honeypot modules, parses logs locally, and pushes normalized data to a central manager over mTLS-secured channels.

.. rubric:: Mutual TLS Security

All agent-to-manager communications are authenticated with mutual TLS using an internal PKI (ECDSA P-384, auto-signed CA). Agent enrollment is handled through one-time tokens with a 10-minute TTL.

.. rubric:: Modular Service Support

Configure each agent to expose up to 6+ services simultaneously. Alongside standard honeypot modules, Melissae supports **CVE-specific modules** — purpose-built containers reproducing real vulnerabilities to detect targeted exploitation attempts. See :doc:`contributing` for guidance on writing new modules.

.. rubric:: Centralized Management Dashboard

Monitor and manage your honeypot fleet through a modern React dashboard:

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Agent Health**
     - Real-time status of all agents: module states, buffer occupancy, and last push time.
   * - **Auto-Refresh**
     - Dashboard and agents pages refresh every 30s / 15s with live indicators.
   * - **Statistical Analysis**
     - Interactive charts: multi-day timelines, hourly activity, protocol doughnut, agent bar charts, day×hour heatmap.
   * - **Trend Detection**
     - Stat cards display percentage change vs the previous 24h with directional arrows.
   * - **Top Credentials**
     - Most attempted usernames across SSH, FTP, and Telnet.
   * - **Log Search (MQL)**
     - Melissae Query Language with logical operators, sortable columns, pagination, and per-agent filtering.
   * - **Log Export**
     - Export logs as JSON, filtered by time range, service, IP, or agent.
   * - **Rule-Based Alerting**
     - Declarative YAML rule engine (12 built-in rules: brute-force, CVE exploitation, ICS writes, recon scans, …). Each rule contributes its score to the per-IP 0–100 verdict.
   * - **Alerts Page**
     - Dedicated view with grouped/flat modes, severity & status filters and bulk actions (acknowledge, resolve).
   * - **Agent Topology**
     - Interactive manager ↔ agents ↔ modules canvas with drag, zoom and persisted layout.
   * - **Activity & Attacker Stats**
     - Dedicated statistics pages for traffic patterns and per-attacker breakdowns.
   * - **GeoIP Attack Map**
     - Interactive world map showing attack origins; markers colored by verdict and sized by score.
   * - **GeoIP Enrichment**
     - Automatic geolocation via ip-api.com batch API, cached in MongoDB, with country flags in the UI.
   * - **STIX 2.1 Export**
     - Export IOCs as STIX 2.1 indicators directly from the Threat Intelligence page.
   * - **Killchain View**
     - Click any IP to open a full attack timeline grouped by protocol.
   * - **Automated Hygiene**
     - Scheduled purge removes benign IoCs unseen for 1h and their associated logs.


