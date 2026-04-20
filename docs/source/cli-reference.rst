CLI Reference
=============

Both CLIs use an interactive console. Enter the directory and run the script.

Manager CLI
-----------

.. code-block:: bash

   cd manager/
   ./melissae-manager.sh
   manager [3 active] >

.. list-table::
   :header-rows: 1
   :widths: 15 30 55

   * - Category
     - Command
     - Description
   * - **Core**
     - ``status``
     - Show manager services status
   * -
     - ``start``
     - Start manager services
   * -
     - ``stop``
     - Stop manager services
   * -
     - ``restart``
     - Restart manager services
   * -
     - ``build``
     - Rebuild manager containers
   * - **Agents**
     - ``enroll <name> <host>``
     - Generate enrollment token for new agent
   * -
     - ``agents``
     - List registered agents with health status
   * -
     - ``agent-exec <name> <action> [mod]``
     - Remote: start/stop/restart/status on agent via mTLS
   * -
     - ``revoke <name>``
     - Revoke agent certificate and unregister
   * -
     - ``agent-logs <name> [n]``
     - Show logs from a specific agent
   * - **Certificates**
     - ``certs list``
     - List all issued certificates with expiry
   * -
     - ``certs renew <name>``
     - Renew an agent certificate
   * - **Modules**
     - ``modules``
     - List available honeypot module types
   * - **Monitoring**
     - ``stats``
     - Show attack statistics
   * -
     - ``threats``
     - Show top threat IPs with scores
   * -
     - ``events [count]``
     - Show recent events (default: 20)
   * - **Management**
     - ``install``
     - Install manager and initialize PKI
   * -
     - ``destroy``
     - Stop and remove all containers
   * - **Shell**
     - ``clear``, ``banner``, ``version``, ``exit``
     - Console utilities

Agent CLI
---------

.. code-block:: bash

   cd agent/
   ./melissae-agent.sh
   agent:my-agent [6 active] >

.. list-table::
   :header-rows: 1
   :widths: 15 30 55

   * - Category
     - Command
     - Description
   * - **Core**
     - ``status``
     - Show all containers + daemon status
   * -
     - ``start [module|all]``
     - Start honeypots + agent daemon
   * -
     - ``stop [module|all]``
     - Stop modules
   * -
     - ``restart``
     - Restart all services
   * -
     - ``build``
     - Rebuild containers
   * - **Modules**
     - ``list``
     - List available modules with status
   * -
     - ``enable <module>``
     - Enable a module in configuration
   * -
     - ``disable <module>``
     - Disable a module in configuration
   * - **Monitoring**
     - ``buffer``
     - Show SQLite buffer status (pending, size)
   * -
     - ``test-connection``
     - Test mTLS connectivity to manager
   * -
     - ``logs <module> [n]``
     - Show local raw logs for a module
   * -
     - ``daemon-log [n]``
     - Show agent daemon log
   * - **Management**
     - ``install <url> <token>``
     - Install agent and enroll with manager
   * - **Shell**
     - ``clear``, ``banner``, ``version``, ``exit``
     - Console utilities
