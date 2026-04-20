Getting Started
===============

Manager Installation
--------------------

Clone the repository on the **manager server**:

.. code-block:: bash

   git clone https://github.com/ilostmypassword/Melissae.git
   cd Melissae/manager/
   chmod +x melissae-manager.sh

Enter the interactive console and run ``install``:

.. danger::

   Your SSH port will be modified and given to you at the end of the installation script. Note it carefully.

.. code-block:: bash

   ./melissae-manager.sh
   manager [0 active] > install

The installer will:

1. Install prerequisites (Docker, OpenSSL, python3-pymongo, apache2-utils)
2. Initialize the PKI (CA + manager certificate)
3. Prompt for dashboard basic-auth credentials
4. Configure cron jobs (threatIntel, purgeLogs, healthPoller)
5. Randomize the SSH admin port

Add your user to the Docker group, then reconnect:

.. code-block:: bash

   sudo usermod -aG docker $USER

Start the manager services:

.. code-block:: text

   manager [0 active] > start

Agent Enrollment
----------------

On the **manager**, generate an enrollment token for the new agent:

.. code-block:: text

   manager [3 active] > enroll my-agent 192.168.1.50

This generates a one-time token (valid 10 minutes) and prints the command to run on the agent.

On the **agent server**, clone the repo and run the enrollment:

.. code-block:: bash

   git clone https://github.com/ilostmypassword/Melissae.git
   cd Melissae/agent/
   chmod +x melissae-agent.sh
   ./melissae-agent.sh
   agent:? [0 active] > install https://192.168.1.10:8443 <token>

The agent will:

1. Install system dependencies and `uv <https://docs.astral.sh/uv/>`_ (Python package manager)
2. Create a Python virtual environment with required packages
3. Install Docker (if not present)
4. Fetch certificates from the manager via the enrollment token
5. Generate the agent configuration
6. Test the mTLS connection
7. Randomize the SSH admin port

Review the module configuration in ``agent/daemon/config.yml``, then start:

.. code-block:: text

   agent:my-agent [0 active] > start

Starting Services
-----------------

**Manager** — always runs MongoDB, API, and Dashboard:

.. code-block:: text

   manager [0 active] > start

**Agent** — runs honeypots + agent daemon:

.. code-block:: text

   agent:my-agent [0 active] > start

Accessing the Dashboard
-----------------------

The dashboard is served over HTTPS on port 443 using the manager's TLS certificate.

.. code-block:: text

   https://<manager-ip>/

Use the basic-auth credentials set during ``install``. Since the certificate is self-signed (internal PKI), your browser will show a security warning — this is expected.
