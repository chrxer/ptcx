Installation
------------

`Source code <https://github.com/chrxer/ptcx>`_

.. code-block:: bash

   $ python -m pip install ptcx

Usage
-----

.. literalinclude:: usage.txt
    :language: text

Patch configuration
-------------------

| Example ptcx file: `patch/main.py.ptcx <https://github.com/chrxer/ptcx/blob/main/patch/main.py.ptcx>`_
| Extra file to add: `patch/extra.py <https://github.com/chrxer/ptcx/blob/main/patch/extra.py>`_
| Source file to patch: `src/main.py <https://github.com/chrxer/ptcx/blob/main/src/main.py>`_ 

.. literalinclude:: ../patch/main.py.ptcx
    :language: python

Reference
-------------------
.. autoclass:: ptcx.BasePTC
    :members:

.. autofunction:: ptcx.patch.path

.. autofunction:: ptcx.patch.reset