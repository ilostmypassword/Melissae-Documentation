Project Structure
=================

.. code-block:: text

   Melissae/
   ├── manager/                          # Manager server
   │   ├── melissae-manager.sh           # Manager interactive CLI
   │   ├── docker-compose.yml            # Manager stack (Mongo + API + Dashboard)
   │   ├── api/                          # Flask REST API
   │   │   ├── api.py
   │   │   └── Dockerfile
   │   ├── dashboard/                    # React dashboard + Nginx
   │   │   ├── conf/                     # Nginx configs (dashboard, mTLS ingestion)
   │   │   ├── src/                      # React source (pages, components)
   │   │   ├── public/                   # Static assets
   │   │   ├── Dockerfile
   │   │   ├── package.json
   │   │   └── ...
   │   ├── scripts/                      # Manager-side cron scripts
   │   │   ├── rule_engine.py            # YAML rule evaluator (called by threatIntel)
   │   │   ├── mql.py                    # Melissae Query Language parser
   │   │   ├── threatIntel.py            # Verdict aggregator (runs the rule engine)
   │   │   ├── health_poller.py          # Agent health polling daemon
   │   │   └── purgeLogs.py              # Non-destructive log/threat cleanup (retention-based)
   │   ├── inspektor/                    # Optional AI threat analyst (AWS Bedrock + LangChain)
   │   │   ├── inspektor.py              # On-demand HTTP service (report + chat)
   │   │   ├── tools.py                  # Read-only MongoDB tools + skill loader
   │   │   ├── prompts/                  # System prompt (framework context + skill index)
   │   │   ├── skills/                   # On-demand skill procedures
   │   │   ├── config.yml
   │   │   └── Dockerfile
   │   └── pki/                          # PKI directory (certs gitignored)
   │       └── .gitignore
   ├── agent/                            # Agent
   │   ├── melissae-agent.sh             # Agent interactive CLI
   │   ├── docker-compose.yml            # Agent stack (honeypots + daemon)
   │   └── daemon/                       # Agent daemon
   │       ├── agent_daemon.py           # Push daemon (buffer, mTLS, health endpoint)
   │       ├── log_parser.py             # Log parsing engine
   │       ├── config.yml                # Agent config template
   │       ├── requirements.txt
   │       └── Dockerfile
   ├── modules/                          # Honeypot module definitions
   │   ├── web/                          # HTTP (Nginx proxy + Apache)
   │   ├── ssh/                          # SSH honeypot
   │   ├── ftp/                          # FTP honeypot (custom Debian + vsftpd image)
   │   │   ├── Dockerfile
   │   │   ├── conf/                     # vsftpd.conf
   │   │   └── server/
   │   ├── modbus/                       # Modbus/ICS honeypot
   │   ├── mqtt/                         # MQTT honeypot
   │   ├── telnet/                       # Telnet honeypot
   │   └── cve/                          # CVE-specific modules
   │       └── CVE-2026-24061/
   ├── rules/                            # YAML detection rules (MLS001 … MLS012)
   │   └── MLS0xx.yml
   └── README.md
