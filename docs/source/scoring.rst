Scoring & Alerting
==================

Starting with **v2.2**, Melissae replaces the continuous weighted-signal scoring engine with a **rule-based alerting engine**. Detection logic now lives in declarative YAML rules under ``rules/``, and each observed IP's verdict is the **sum of the scores of every rule that matched its activity**, capped at 100.

Scale & Verdicts
-----------------

Scores still use a **0–100 scale**. Verdict thresholds are unchanged:

.. list-table::
   :header-rows: 1
   :widths: 15 20 65

   * - Range
     - Verdict
     - Description
   * - 0–29
     - Benign
     - Passive noise, single low-value connections
   * - 30–69
     - Suspicious
     - Active scanning, failed auth, reconnaissance
   * - 70–100
     - Malicious
     - Compromise, post-exploitation, ICS tampering, confirmed CVE exploitation

Rule Format
-----------

Each rule is a YAML file under ``rules/`` (one file per rule, named ``MLSxxx.yml``):

.. code-block:: yaml

   id: MLS008
   name: SSH brute-force attempt
   description: >
     Multiple SSH authentication failures from the same IP within a short
     window. Indicates credential-stuffing or brute-force activity.
   severity: high
   enabled: true
   schedule: "*/1 * * * *"
   lookback: 1m
   mql: 'protocol:ssh AND action:Failed'
   group_by: ip
   threshold: 3
   score: 40
   tags: [brute-force, credential-access]
   mitre: [T1110]

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Field
     - Meaning
   * - ``id``
     - Stable rule identifier (e.g. ``MLS008``).
   * - ``name`` / ``description``
     - Human-readable label and longer explanation surfaced in the dashboard.
   * - ``severity``
     - One of ``low``, ``medium``, ``high``, ``critical``. Drives UI styling and filtering.
   * - ``enabled``
     - Boolean; disabled rules are loaded but never evaluated.
   * - ``schedule``
     - Cron expression controlling how often the rule is re-evaluated by ``rule_engine.py``.
   * - ``lookback``
     - Time window scanned at each run (``s`` / ``m`` / ``h`` / ``d`` suffixes).
   * - ``mql``
     - Detection query in :ref:`Melissae Query Language <mql>` (the same DSL as the dashboard search bar).
   * - ``group_by``
     - Aggregation key (typically ``ip``).
   * - ``threshold``
     - Minimum number of matching events in the window required to emit an alert.
   * - ``score``
     - Points contributed to the per-IP verdict when the rule fires.
   * - ``tags`` / ``mitre``
     - Free-form tags and MITRE ATT&CK technique IDs for classification.

Built-in Rules
--------------

Twelve rules ship with v2.2, covering the signals previously hard-coded in the scoring engine:

.. list-table::
   :header-rows: 1
   :widths: 12 35 12 10 31

   * - ID
     - Detection
     - Severity
     - Score
     - Notes
   * - MLS001
     - CVE exploitation attempt (``cve:CVE``)
     - critical
     - 70
     - Any hit on a CVE-tagged module
   * - MLS002
     - FTP brute-force (``protocol:ftp AND action:"Login failed"``)
     - high
     - 30
     - ≥5 failures / 5 min
   * - MLS003 – MLS007
     - Successful logins, post-exploitation commands, multi-protocol activity, …
     - varies
     - varies
     - See ``rules/`` for the full set
   * - MLS008
     - SSH brute-force (``protocol:ssh AND action:Failed``)
     - high
     - 40
     - ≥3 failures / 1 min
   * - MLS009 – MLS011
     - Modbus reads/writes, Telnet anomalies, …
     - varies
     - varies
     - See ``rules/`` for the full set
   * - MLS012
     - Nmap scan (``protocol:http AND nmap``)
     - low
     - 5
     - User-agent based recon detection

The complete set of rules — including exact MQL queries, thresholds and scores — is the source of truth in the ``rules/`` directory and is also exposed by the API at ``GET /api/rules``.

How Scoring Works
-----------------

1. ``rule_engine.py`` loads every YAML file in ``rules/`` (configurable via ``MELISSAE_RULES_DIR``).
2. For each enabled rule whose ``schedule`` is due, it pulls the logs of the last ``lookback`` window, runs the ``mql`` query against them and groups the matches by ``group_by``.
3. Every group with at least ``threshold`` matches produces an **alert** in MongoDB (``alerts`` collection) carrying ``rule_id``, ``severity``, ``score``, ``ip``, time range and matching log references.
4. ``threatIntel.py`` aggregates alerts (rolling 90-day window) per IP into the ``threats`` collection. The verdict score is the sum of distinct rule scores, capped at 100; the verdict label follows the table above.
5. The dashboard consumes ``threats`` (Threat Intelligence, Map) and ``alerts`` (Alerts page) to drive its views.

This design makes detection logic **transparent and auditable**: every score increment is traceable to a specific rule, and operators can enable/disable, retune or extend rules without touching engine code.

.. _mql:

Melissae Query Language (MQL)
-----------------------------

MQL is the small DSL used both by the dashboard search bar and by the ``mql`` field of each rule. Supported features:

- Field-scoped terms — ``protocol:ssh``, ``action:"Login failed"``, ``ip:1.2.3.4``, ``cve:CVE-2026-24061``, ``user:root``, ``user-agent:nmap``, ``path:/admin``, ``hour:14``, ``date:2026-05-09``, ``agent:my-agent``.
- Free-text terms — bare words match against any field.
- Boolean operators — ``AND`` / ``OR`` / ``NOT`` (also ``and`` / ``or`` / ``!``), with parenthesized grouping.
- Quoted values — ``"Login failed"`` to match phrases containing spaces.

Examples
^^^^^^^^

.. code-block:: text

   protocol:ssh AND action:Failed
   protocol:ftp AND action:"Login failed"
   protocol:modbus AND action:write
   cve:CVE
   protocol:http AND nmap
   ip:192.168.1.10 AND NOT action:successful

Authoring New Rules
-------------------

To add a new detection:

1. Drop a new ``MLSxxx.yml`` under ``rules/`` with a unique ``id``.
2. Pick an appropriate ``severity``, ``score``, ``threshold`` and ``lookback``.
3. Express the matching condition as an ``mql`` query.
4. Reload the manager (``restart``) — the rule engine picks up the file at next tick.

.. tip::

   Keep ``score`` values proportional to confidence: high-confidence single-event detections (CVE exploitation, ICS writes) typically warrant 50–70 points, whereas noisy signals (scans, low-volume failures) should stay in the 5–20 range so they only escalate to *Suspicious* / *Malicious* when combined with other rules.
