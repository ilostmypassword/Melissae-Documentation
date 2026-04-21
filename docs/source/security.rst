Security
========

Melissae applies defense-in-depth across all components:

.. note::

   Agent and manager certificates have a **1-year validity**. Use ``certs list`` on the manager to check expiry dates and ``certs renew <agent-name>`` to reissue a certificate before it expires. The CA certificate is valid for 10 years.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Layer
     - Measure
   * - **Transport**
     - mTLS (ECDSA P-384) for all agent↔manager traffic; TLS 1.2+ enforced; HSTS on dashboard
   * - **Authentication**
     - mTLS CN verification on ingestion; one-time enrollment tokens (10 min TTL); basic-auth on dashboard
   * - **Input validation**
     - MongoDB ``$``-operator injection blocked; string length limits; IP address format validation; required-field checks
   * - **Rate limiting**
     - Nginx rate limits on ingestion (30 req/min), enrollment (5 req/min), dashboard API (60 req/min), GeoIP (5 req/min)
   * - **Path traversal**
     - Certificate directory validated against PKI base path before file access
   * - **SSRF prevention**
     - GeoIP endpoint rejects private/loopback IPs; input capped at 100 entries; 3s timeout on external calls
   * - **Error handling**
     - Internal errors return generic messages; no stack traces or database details exposed to clients
   * - **Hashing**
     - SHA-256 for log deduplication (agent and manager)
   * - **Headers**
     - ``X-Frame-Options: DENY``, ``X-Content-Type-Options: nosniff``, ``CSP``, ``Permissions-Policy``, ``Referrer-Policy`` on dashboard
   * - **Container hardening**
     - CVE modules run with ``cap_drop: ALL``, read-only filesystem, PID/memory limits, ``no-new-privileges``
   * - **CORS**
     - Origins restricted and configurable via ``CORS_ORIGINS`` environment variable
