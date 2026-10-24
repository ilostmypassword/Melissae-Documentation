AI Threat Analyst (Inspektor)
=============================

**Inspektor** is the optional AI threat analyst embedded in the manager. It is a
`LangChain <https://www.langchain.com/>`_ agent backed by `AWS Bedrock
<https://aws.amazon.com/bedrock/>`_ that investigates the live honeypot data
through read-only tools and either answers questions in a built-in chat or
produces a full **threat briefing** exportable to PDF.

Inspektor runs **on demand** only, there is no background polling. It acts on a
single request from the dashboard, calls its tools against MongoDB, reasons over
the evidence, and returns Markdown. Every answer is grounded strictly in data it
actually retrieves; it never writes to the database and never invents indicators.

.. note::

   Inspektor is **disabled by default**. It requires AWS Bedrock credentials with
   model access and is enabled through the manager CLI ``inspektor`` command. See
   :ref:`enabling-inspektor` below. Until it is configured, the dashboard shows a
   short setup guide on the Inspektor page instead of the chat, and the Briefing
   card on the home page stays hidden.

----

How It Works
------------

Inspektor is served as a small Flask service listening on port ``8088`` on the
**internal Docker network only**. It is never exposed externally — the dashboard
reaches it exclusively through the manager API proxy under ``/api/inspektor/*``.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Manager API endpoint
     - Purpose
   * - ``GET /api/inspektor/status``
     - Return ``{enabled, ready, configured}``. ``configured`` is true when the
       container has both ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY`` set.
   * - ``GET /api/inspektor/report``
     - Return the latest stored threat briefing (from the ``inspektor_report`` collection).
   * - ``POST /api/inspektor/generate``
     - Trigger a fresh on-demand briefing, store it, and return the Markdown.
   * - ``POST /api/inspektor/chat``
     - Send a conversational turn ``{message, history}`` and receive ``{reply}``.

When Inspektor is disabled or unreachable, these proxy routes return a clean
``503`` so the dashboard degrades gracefully.

Prompts & Skills
----------------

Inspektor's behaviour is defined in **Markdown**, not in Python, which keeps it
easy to audit and tune:

.. code-block:: text

   prompts/system.md  ──indexes──▶  skills/*.md  ──point to──▶  tool calls

- **System prompt** (``prompts/system.md``) — carries the full Melissae framework
  context (architecture, data model, scoring and verdicts, the catalog of the 14
  detection rules), the security rules, and a compact **skill index**.
- **Skills** (``skills/*.md``) — one short procedure per task. Skills are **loaded
  on demand**: only a one-line index sits in the base prompt, and Inspektor pulls
  the full procedure with its ``get_skill`` tool when a request matches. This keeps
  each analysis focused and the context small.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Skill
     - Used when
   * - ``threat-briefing``
     - The operator asks for a report, briefing or overall summary of the network.
   * - ``ip-investigation``
     - A single attacker or IP address needs a deep dive.
   * - ``attacker-ranking``
     - Attackers must be compared or ranked (top / worst offenders).
   * - ``alert-triage``
     - The operator asks what is firing right now, about recent alerts, or wants a
       rule hit explained (e.g. MLS009).
   * - ``log-hunting``
     - Pivoting on a specific indicator across the raw logs, including activity
       beyond the tracked threats.
   * - ``agent-health``
     - Questions about the sensor fleet — agents, coverage and gaps.
   * - ``campaign-correlation``
     - Several IPs seem to work together (botnet, same actor, shared tooling).
   * - ``mitre-mapping``
     - ATT&CK techniques observed and coverage gaps.
   * - ``ioc-blocklist``
     - Build a blocklist: IPs to ban, with an export-ready output.
   * - ``ics-iot-watch``
     - Modbus, MQTT and Telnet botnet activity, ICS tampering.

Tools
-----

Inspektor only has **read-only** access to MongoDB. Its tools mirror the same data
the dashboard consumes: global statistics, a raw-log overview (the ground-truth
superset of all observed sources, including those not yet scored), threat lists
and per-IP details, killchain timelines, recent alerts, log search, and agent
health — plus the ``get_skill`` loader that fetches a skill procedure on demand.
The nine tools are ``get_global_stats``, ``list_threats``, ``get_threat``,
``get_killchain``, ``get_recent_alerts``, ``search_logs``, ``get_agents``,
``get_log_overview`` and ``get_skill``.

.. _enabling-inspektor:

Enabling Inspektor
------------------

Inspektor ships as an optional container guarded by the Docker Compose profile
``inspektor``. Enable, reconfigure or disable it at any time from the manager CLI:

.. code-block:: text

   manager [3 active] > inspektor

The command walks you through the configuration:

.. code-block:: text

   [?] Enable Inspektor AI analyst? [y/N] y
   AWS Access Key ID: ...
   AWS Secret Access Key: ...
   AWS Session Token (optional, press Enter to skip):
   AWS Region [us-east-1]:
   Bedrock Model ID [anthropic.claude-3-5-sonnet-20240620-v1:0]:

Credentials are written to the manager ``.env`` file (``chmod 600``) together with
``COMPOSE_PROFILES=inspektor``, and the ``melissae_inspektor`` container is built
and started. Answering ``N`` removes the profile and stops the container.

.. warning::

   The AWS credentials are stored on the manager host in the ``.env`` file. Use a
   dedicated IAM principal scoped to ``bedrock:InvokeModel`` for the chosen model,
   and keep the file readable only by the deploying user.

Configuration
-------------

Runtime settings live in ``manager/inspektor/config.yml``:

.. code-block:: yaml

   mongo:
     uri: "mongodb://melissae_mongo:27017"
     db: "melissae"

   bedrock:
     region: "us-east-1"
     model_id: "anthropic.claude-3-5-sonnet-20240620-v1:0"
     temperature: 0.2
     max_tokens: 2048

   inspektor:
     killchain_limit: 200

The AWS region, model id and credentials provided through the CLI are injected as
environment variables (``AWS_REGION``, ``BEDROCK_MODEL_ID``, ``AWS_ACCESS_KEY_ID``,
``AWS_SECRET_ACCESS_KEY``, ``AWS_SESSION_TOKEN``) and take precedence over the file.

.. note::

   The Bedrock model must be enabled in your AWS account and reachable from the
   selected region. Recent Anthropic models cannot be invoked on-demand with their
   bare model ID: use the **inference profile** ID, which carries a region prefix
   (for example ``us.anthropic.<model>-<date>-v1:0``). Re-run the ``inspektor``
   command to change the model; values in ``.env`` override ``config.yml``.

Troubleshooting
---------------

When a chat turn fails, the dashboard only shows the generic message *"Inspektor
could not process this request"*. The actual cause is in the container logs
(look for the ``Chat turn failed:`` line):

.. code-block:: bash

   docker logs melissae_inspektor --tail 30

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Error in the logs
     - Cause and fix
   * - ``AccessDeniedException … is not available for this account``
     - Model access has not been granted in AWS Bedrock for this account/region, or
       the model ID does not exist. Request access or choose another model.
   * - ``ValidationException … on-demand throughput isn't supported``
     - The model requires an inference profile. Use the region-prefixed ID
       (for example ``us.anthropic.…``).

Neither agents nor logs are required for Inspektor to answer: these errors come
from the Bedrock side (model access or model ID), not from the data.

Using Inspektor
---------------

Once enabled, Inspektor is available from the **Inspektor** page of the dashboard.
The sidebar entry is always visible; while Inspektor is not configured, the page
shows a three-step setup guide (run the ``inspektor`` command, enter your AWS
Bedrock credentials, click **Check again**) instead of the chat.

- **Chat** — ask about attackers, alerts, kill-chains or the overall network state
  and get grounded, technical answers. Inspektor runs only when you ask; you can
  leave the page while it thinks and you will be notified when it answers. Every
  reply ships with a collapsible **Thinking** panel that lists each reasoning
  step, the tool that was called, its input arguments and the (truncated) output
  Inspektor observed, so its conclusions remain fully auditable.
- **Generate report** — produce a full threat briefing over the whole honeypot
  network, surfaced on the dashboard home (only once Inspektor is configured) and
    **exportable to PDF**.
