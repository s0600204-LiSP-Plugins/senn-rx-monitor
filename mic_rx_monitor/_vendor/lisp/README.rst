
The files in this folder are taken/adapted from similarly named files within Linux Show Player.

----

Differences to upstream:

* ``lisp.backend.audio_utils``

  - All but the ``iec_scale()`` function removed

* ``lisp.core.clock``

  - Does not define any instances of the class

* ``lisp.core.signal``

  - Has ``async_function`` from ``lisp.core.decorators`` merged
  - Has ``weak_call_proxy`` from ``lisp.core.util`` merged

* ``lisp.ui.widgets.__init__``

  - Reduced to only include the class we vendor
