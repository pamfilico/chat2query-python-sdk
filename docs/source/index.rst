Chat2Query Python SDK
=====================

Build conversational experiences that translate natural language into SQL with
Chat2Query. This SDK gives Python developers a typed, friendly interface to the
Chat2Query platform, letting you:

* Authenticate with the same application API keys used by your team
* Manage databases, chats, and messages programmatically
* Generate SQL through Chat2Query’s AI pipeline and inspect execution metadata

Installation
------------

Most teams install the SDK either into an existing virtual environment or
through Poetry. Pick whichever matches your workflow:

**Pip**

.. code-block:: bash

   python -m pip install chat2query-python-sdk

**Poetry**

.. code-block:: bash

   poetry add chat2query-python-sdk

Quick Start
-----------

.. code-block:: python

   from chat2query import Chat2QueryService

   service = Chat2QueryService(
       api_key="c2q-...your-application-key...",
       base_url="http://localhost:5000",  # or https://chat2query.com
   )

   # List databases
   for db in service.databases.list():
       print(db["id"], db["name"])

   # Create a chat and ask a question
   chat = service.chats.create(database_id=db["id"], name="SDK Demo")
   answers = service.messages.ask(chat_id=chat["id"], prompt="Show top customers")
   print(answers[0]["response"])

Workflow Overview
-----------------

1. **Connect** using an application API key. The SDK validates the key on init.
2. **Organize** resources with `service.databases` and `service.chats`.
3. **Converse** through `service.messages`: ask questions, regenerate answers,
   and review API specs or usage.
4. **Ship**: automate insights, power customer dashboards, or embed SQL tooling
   within your own product.

Resource Guides
---------------

.. toctree::
   :maxdepth: 2
   :caption: API Reference
   :glob:

   api/*


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
