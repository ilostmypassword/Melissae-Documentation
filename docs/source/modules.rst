Modules
=======

The choice of modular, containerized deployment means that contributors can easily develop new modules. There are currently 6 native honeypot modules, 1 CVE module, and 3 system services.

.. note::

   **Port conflict rule**: Modules that bind the same host port cannot be deployed together. For example, ``telnet`` and ``cve-2026-24061`` both use port 23 — the CLI will reject conflicting combinations.

Summary
-------

.. list-table::
   :header-rows: 1
   :widths: 10 30 15 15 30

   * - Type
     - Service / Container
     - Port(s)
     - Exposure
     - Notes
   * - Honeypot
     - melissae_proxy, melissae_apache1, melissae_apache2
     - 80
     - Public
     - Web stack via Nginx + Apache
   * - Honeypot
     - melissae_ssh
     - 22
     - Public
     - Weak creds by design
   * - Honeypot
     - melissae_ftp
     - 21
     - Public
     - Weak creds by design
   * - Honeypot
     - melissae_modbus
     - 502
     - Public
     - PLC emulation
   * - Honeypot
     - melissae_mqtt
     - 1883
     - Public
     - Mosquitto
   * - Honeypot
     - melissae_telnet
     - 23
     - Public
     - Weak creds by design
   * - CVE
     - melissae_cve_2026_24061
     - 23
     - Public
     - CVE-2026-24061 Telnet auth bypass
   * - System
     - melissae_mongo
     - 127.0.0.1:27017
     - Manager only
     - Data store
   * - System
     - melissae_api
     - 127.0.0.1:5000
     - Manager only
     - Flask API
   * - System
     - melissae_dashboard
     - 0.0.0.0:443, 0.0.0.0:8443
     - HTTPS + basic auth
     - Dashboard (:443) + mTLS ingestion (:8443)
   * - System
     - melissae_agent (daemon)
     - 8444
     - Agent only
     - Health endpoint

Web
---

.. list-table::
   :header-rows: 1
   :widths: 20 30 30

   * - Type
     - Image
     - Container Name
   * - Proxy
     - nginx:latest
     - melissae_proxy
   * - Web Server
     - httpd:2.4-alpine
     - melissae_apache1
   * - Web Server
     - httpd:2.4-alpine
     - melissae_apache2

**Log format:**

.. code-block:: json

   [
     {
       "protocol": "http",
       "date": "2025-04-16",
       "hour": "11:47:08",
       "ip": "192.168.X.X",
       "action": "GET",
       "path": "/",
       "user-agent": "Mozilla/5.0"
     }
   ]

**Usage:**

- By default, Melissae provides a basic configuration for both proxy and web server containers, located in ``modules/web/conf``.
- Add the files you need for the website to be exposed via honeypot in ``modules/web/server``.

SSH
---

.. list-table::
   :header-rows: 1
   :widths: 20 30 30

   * - Type
     - Image
     - Container Name
   * - SSH Server
     - ubuntu:latest + openssh
     - melissae_ssh

**Log format:**

.. code-block:: json

   [
     {
       "protocol": "ssh",
       "date": "2025-04-16",
       "hour": "11:48:09",
       "ip": "192.168.X.X",
       "action": "Login failed with invalid user",
       "user": "test"
     }
   ]

**Usage:**

- Modify module credentials in ``modules/ssh/Dockerfile`` (default: ``user:admin``).

FTP
---

.. list-table::
   :header-rows: 1
   :widths: 20 30 30

   * - Type
     - Image
     - Container Name
   * - FTP Server
     - fauria/vsftpd
     - melissae_ftp

**Log format:**

.. code-block:: json

   [
     {
       "protocol": "ftp",
       "date": "2025-04-16",
       "hour": "11:48:37",
       "ip": "192.168.X.X",
       "action": "Login failed",
       "user": "test"
     }
   ]

**Usage:**

- The shared repository with the FTP container is ``modules/ftp/server``.
- Modify module credentials in ``agent/docker-compose.yml`` (default: ``ftpuser:ftppass``).

Modbus
------

.. list-table::
   :header-rows: 1
   :widths: 20 30 30

   * - Type
     - Image
     - Container Name
   * - Modbus TCP Server
     - python:3.11-slim
     - melissae_modbus

**Log format:**

.. code-block:: json

   [
     {
       "protocol": "modbus",
       "date": "2025-05-30",
       "hour": "10:38:23",
       "ip": "192.168.X.X",
       "action": "Read request - Read Holding Registers"
     },
     {
       "protocol": "modbus",
       "date": "2025-05-30",
       "hour": "10:41:22",
       "ip": "192.168.X.X",
       "action": "Write attempt - Write Multiple Registers"
     }
   ]

**Features:**

- **Industrial PLC Emulation** — Simulates Siemens S7-1200 and Schneider Electric M340 PLCs.
- **Randomized Device Identifiers** — Generates unique serial numbers and firmware versions on each startup.
- **Protocol Detection** — Logs all Modbus function codes (read/write operations).
- **Threat Escalation** — Write attempts trigger high-severity threat alerts.

**Usage:**

- **Default Profile**: Siemens S7-1200 (modify in ``modules/modbus/Dockerfile`` to use ``schneider`` profile).
- **Port**: Standard Modbus TCP port 502.
- **Device Profiles**:

  - **Siemens** — S7-xxxxxx serials, V3.x-V4.x firmware, 1000 registers.
  - **Schneider** — M340-xxxxx-X serials, V2.x-V3.x firmware, 2000 registers.

MQTT
----

.. list-table::
   :header-rows: 1
   :widths: 20 30 30

   * - Type
     - Image
     - Container Name
   * - Mosquitto Server
     - eclipse-mosquitto:latest
     - melissae_mqtt

**Log format:**

.. code-block:: json

   [
     {
       "protocol": "mqtt",
       "date": "2025-09-12",
       "hour": "08:56:25",
       "ip": "192.168.X.X",
       "action": "Client connected"
     },
     {
       "protocol": "mqtt",
       "date": "2025-09-12",
       "hour": "08:57:17",
       "ip": "192.168.X.X",
       "action": "Subscribe",
       "user": "auto-XX"
     }
   ]

Telnet
------

.. list-table::
   :header-rows: 1
   :widths: 20 30 30

   * - Type
     - Image
     - Container Name
   * - Telnet Server
     - ubuntu:24.04 + inetutils-telnetd
     - melissae_telnet

**Log format:**

.. code-block:: json

   [
     {
       "protocol": "telnet",
       "date": "2026-02-15",
       "hour": "09:12:34",
       "ip": "192.168.X.X",
       "action": "Connection established"
     },
     {
       "protocol": "telnet",
       "date": "2026-02-15",
       "hour": "09:12:41",
       "ip": "192.168.X.X",
       "action": "Login failed",
       "user": "admin"
     },
     {
       "protocol": "telnet",
       "date": "2026-02-15",
       "hour": "09:13:02",
       "ip": "192.168.X.X",
       "action": "Login successful",
       "user": "admin"
     }
   ]

**Usage:**

- Modify credentials in ``modules/telnet/Dockerfile`` (default: ``admin:telnet``).
- Logs are written to ``agent/logs/telnet/auth.log`` (mounted from the container).

CVE Modules
-----------

CVE modules are a dedicated category of honeypots that reproduce **specific, real-world vulnerabilities**. Unlike generic protocol honeypots, they are designed to attract and detect exploitation attempts targeting known CVEs.

Each CVE module lives under ``modules/cve/<CVE-ID>/`` and follows a standard structure:

.. code-block:: text

   modules/cve/CVE-YYYY-XXXXX/
       |-- Dockerfile
       |-- startup.sh
       |-- logs/

Log entries from CVE modules include a ``cve`` field in addition to the standard fields, enabling CVE-specific filtering in the dashboard search engine (e.g. ``cve:CVE-2026-24061``).

CVE-2026-24061 — Telnet Auth Bypass
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Property
     - Value
   * - CVE
     - `CVE-2026-24061 <https://nvd.nist.gov/vuln/detail/CVE-2026-24061>`_
   * - CVSS
     - 9.8 CRITICAL
   * - CWE
     - CWE-88 Improper Neutralization of Argument Delimiters in a Command
   * - Affected
     - GNU Inetutils telnetd ≤ 2.7
   * - Container
     - melissae_cve_2026_24061
   * - Port
     - 23 (Telnet)
   * - Image
     - Ubuntu 24.04 + inetutils-telnetd 2:2.5-3ubuntu4

**Vulnerability**: The ``-f`` flag in GNU inetutils ``telnetd`` allows an attacker to bypass authentication entirely by injecting ``-froot`` as the ``USER`` environment variable during connection. The flag is interpreted by ``login`` as "pre-authenticated", granting immediate root access without credentials.

**Log format:**

.. code-block:: json

   [
     {
       "protocol": "telnet",
       "date": "2026-01-15",
       "hour": "14:32:08",
       "ip": "192.168.X.X",
       "action": "Connection opened",
       "cve": "CVE-2026-24061"
     },
     {
       "protocol": "telnet",
       "date": "2026-01-15",
       "hour": "14:32:12",
       "ip": "192.168.X.X",
       "action": "Root login successful",
       "user": "root",
       "cve": "CVE-2026-24061"
     }
   ]

**Usage:**

- No configuration needed — the module runs with default settings.
