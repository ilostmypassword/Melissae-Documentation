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

Configure each agent to expose up to 7 services simultaneously (Web, SSH, FTP, Telnet, Modbus/ICS, MQTT, plus a CVE category). Alongside standard honeypot modules, Melissae supports **CVE-specific modules** — purpose-built containers reproducing real vulnerabilities to detect targeted exploitation attempts. See :doc:`contributing` for guidance on writing new modules.

.. rubric:: Centralized Management Dashboard

Monitor and manage your honeypot fleet through a modern React dashboard:

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **Real-time Overview**
     - Auto-refreshing stat cards, charts and topology with trend indicators vs the previous 24h.
   * - **Agent Fleet Monitoring**
     - Per-agent health, module states, buffer occupancy and last push time.
   * - **Rule-Based Alerting**
     - Declarative YAML rule engine (12 built-in rules) feeding a dedicated Alerts page with grouping, severity/status filters and bulk actions.
   * - **Threat Intelligence**
     - Per-IP 0–100 verdicts, killchain timeline grouped by protocol and STIX 2.1 export.
   * - **Inspektor AI Threat Analyst**
     - Optional **Inspektor** agent (AWS Bedrock + LangChain) for on-demand chat and exportable threat briefings, grounded strictly in retrieved data.
   * - **GeoIP Attack Map**
     - Interactive world map of attack origins with country breakdown, automatically adapting to private vs public IP mixes.
   * - **Log Search (MQL)**
     - Melissae Query Language with logical operators, sortable / paginated tables and JSON export.
   * - **Activity & Attacker Statistics**
     - Dedicated pages for traffic patterns and per-attacker breakdowns (top IPs, credentials, user-agents).
   * - **Automated Hygiene**
     - Non-destructive scheduled purge: recycles idle benign threat documents (rebuilt automatically from the logs on the next run) and trims logs older than the retention window (30 days by default).

See :doc:`dashboard` for the full per-page breakdown.

.. rubric:: Inspektor AI Threat Analyst

An optional AI analyst, **Inspektor**, runs on the manager on demand. Built on AWS
Bedrock and LangChain, it investigates the live honeypot data through read-only
tools, answers questions in a built-in chat, and produces SOC-ready threat
briefings exportable to PDF. It loads task-specific *skills* only when needed and
answers strictly from retrieved data. See :doc:`inspektor`.


