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
   :ref:`enabling-inspektor` below.

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
  context (architecture, data model, scoring and verdicts, the catalog of the 12
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
     - The operator asks what is firing right now or about recent alerts.
   * - ``log-hunting``
     - Pivoting on a specific indicator across the raw logs.
   * - ``agent-health``
     - Questions about the sensor fleet — agents, coverage and gaps.

Tools
-----

Inspektor only has **read-only** access to MongoDB. Its tools mirror the same data
the dashboard consumes: global statistics, a raw-log overview (the ground-truth
superset of all observed sources, including those not yet scored), threat lists
and per-IP details, killchain timelines, recent alerts, log search, and agent
health — plus the ``get_skill`` loader that fetches a skill procedure on demand.

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
   selected region. Some models require a region-specific inference profile — pick
   a model and region where ``bedrock:InvokeModel`` is granted.

Using Inspektor
---------------

Once enabled, Inspektor is available from the **Inspektor** page of the dashboard:

- **Chat** — ask about attackers, alerts, kill-chains or the overall network state
  and get grounded, technical answers. Inspektor runs only when you ask; you can
  leave the page while it thinks and you will be notified when it answers. Every
  reply ships with a collapsible **Thinking** panel that lists each reasoning
  step, the tool that was called, its input arguments and the (truncated) output
  Inspektor observed, so its conclusions remain fully auditable.
- **Generate report** — produce a full threat briefing over the whole honeypot
  network, surfaced on the dashboard home and **exportable to PDF**.
