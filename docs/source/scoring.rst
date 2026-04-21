Scoring
=======

Scale & Verdicts
-----------------

Scores use a **continuous 0–100 scale** with additive weighted signals and log-scaling for volume-dependent indicators.

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
     - Compromise, post-exploitation, ICS tampering

Scoring Signals
---------------

The following signals accumulate additively. The total is capped at 100.

.. list-table::
   :header-rows: 1
   :widths: 35 40 15 10

   * - Signal
     - Trigger
     - Max pts
     - Scaling
   * - HTTP activity
     - Any HTTP requests
     - 20
     - log₂
   * - MQTT activity
     - Any MQTT events
     - 15
     - log₂
   * - Sensitive HTTP paths
     - Probes to ``/wp-admin``, ``/.env``, ``/.git``, ``/admin``, etc.
     - 35
     - per unique path
   * - HTTP burst
     - ≥20 hits in a 5-minute window
     - 25
     - linear
   * - Auth failures (low)
     - 1–4 failures across SSH/FTP/Telnet
     - 32
     - 8 pts each
   * - Auth failures (brute-force)
     - ≥5 failures across SSH/FTP/Telnet
     - 35
     - linear (capped)
   * - SSH burst
     - ≥5 SSH attempts in 5 min
     - 20
     - linear (capped)
   * - FTP burst
     - ≥5 FTP attempts in 5 min
     - 20
     - linear (capped)
   * - Telnet burst
     - ≥5 Telnet attempts in 5 min
     - 20
     - linear (capped)
   * - Telnet activity
     - Any Telnet events (deprecated protocol)
     - 15
     - fixed
   * - Successful Telnet login
     - Possible CVE exploitation
     - 45
     - fixed
   * - CVE exploitation confirmed
     - ``cve`` field present in log entry
     - 50
     - fixed
   * - Successful SSH login
     - —
     - 40
     - fixed
   * - Successful FTP login
     - —
     - 35
     - fixed
   * - FTP file transfers
     - Upload or download detected
     - 25
     - linear (capped)
   * - Post-compromise commands
     - ``sudo``, ``wget``, ``curl``, ``nc``, ``nmap``, etc. over SSH
     - 45
     - linear (capped)
   * - Modbus read operations
     - —
     - 25
     - linear (capped)
   * - Modbus write operations
     - —
     - 50
     - linear (capped)
   * - Multi-protocol activity
     - ≥3 distinct protocols observed
     - 15
     - fixed
   * - Multiple services compromised
     - SSH+FTP or Telnet+SSH/FTP successful logins
     - 20
     - fixed
   * - ICS tampering with credentials
     - Modbus write + SSH or FTP successful login
     - 25
     - fixed

.. note::

   Scores accumulate across all signals but are capped at **100**. A single high-value signal (e.g. CVE exploitation + successful Telnet login = 95 pts) can push an IP directly to Malicious without needing volume.

Confidence
----------

Confidence is a weighted combination of 5 factors (0.10 – 1.00):

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Factor
     - Weight
     - Based on
   * - Volume
     - 20%
     - Log-scaled event count
   * - Signal diversity
     - 25%
     - Number of distinct scoring reasons
   * - Protocol breadth
     - 10%
     - Number of protocols seen
   * - Time spread
     - 15%
     - Observation duration (up to 24h)
   * - Indicator certainty
     - 30%
     - High-confidence signals (login, post-exploit, ICS writes, telnet CVE exploitation)
