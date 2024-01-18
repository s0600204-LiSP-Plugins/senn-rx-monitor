
The files in this folder are taken/adapted from similarly named files within Linux Show Player.

----

Differences to upstream:

* ``lisp.core.clock``

  - Does not define any instances of the class
  - Uses qtpy instead of PyQt5

* ``lisp.core.signal``

  - Has ``async_function`` from ``lisp.core.decorators`` merged
  - Has ``weak_call_proxy`` from ``lisp.core.util`` merged
  - Uses qtpy instead of PyQt5
