Project Structure
=================

.. code-block:: text

   Melissae/
   ├── manager/                          # Manager server
   │   ├── melissae-manager.sh           # Manager interactive CLI
   │   ├── docker-compose.yml            # Manager stack (Mongo + API + Dashboard)
   │   ├── health_poller.py              # Agent health polling daemon
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
   │   │   ├── threatIntel.py            # Threat scoring engine
   │   │   └── purgeLogs.py             # Log/IoC cleanup
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
   │   ├── ftp/                          # FTP honeypot
   │   ├── modbus/                       # Modbus/ICS honeypot
   │   ├── mqtt/                         # MQTT honeypot
   │   ├── telnet/                       # Telnet honeypot
   │   └── cve/                          # CVE-specific modules
   │       └── CVE-2026-24061/
   └── README.md
