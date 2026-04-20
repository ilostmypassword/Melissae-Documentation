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

.. list-table::
   :header-rows: 1
   :widths: 20 50 15

   * - Category
     - Signals
     - Max Points
   * - Reconnaissance
     - HTTP requests (log-scaled), MQTT events
     - ~20
   * - Scanning
     - Sensitive HTTP paths, HTTP burst (>20/5min)
     - ~35
   * - Auth attacks
     - Brute-force (SSH/FTP/Telnet failures), SSH/FTP/Telnet bursts
     - ~35
   * - Compromise
     - Successful SSH/FTP login, FTP file transfers
     - ~40
   * - CVE exploitation
     - Telnet activity (deprecated protocol), successful Telnet login (CVE exploit)
     - ~60
   * - Post-exploit
     - Sensitive SSH commands (sudo, wget, curl…)
     - ~45
   * - ICS/SCADA
     - Modbus read/write operations
     - ~50
   * - Compounding
     - Multi-protocol activity, multiple services compromised, ICS + credentials, Telnet + other compromises
     - ~25

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
