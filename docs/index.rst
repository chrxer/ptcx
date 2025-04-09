Installation
------------

`Source code <https://github.com/chrxer/ptcx>`_

(requires git cli to be installed)
.. code-block:: bash

   $ python -m pip install ptcx

Usage
-----

.. literalinclude:: usage.txt
    :language: text

Or over python:

.. autofunction:: ptcx.patch.path

.. autofunction:: ptcx.patch.reset

Patch configuration
-------------------

| Example ptcx file: `patch/main.py.ptcx <https://github.com/chrxer/ptcx/blob/main/patch/main.py.ptcx>`_
| Extra file to add: `patch/extra.py <https://github.com/chrxer/ptcx/blob/main/patch/extra.py>`_
| Source file to patch: `src/main.py <https://github.com/chrxer/ptcx/blob/main/src/main.py>`_ 

.. literalinclude:: ../patch/main.py.ptcx
    :language: python

Language support
-----------------
.. list-table::
   :header-rows: 1

   * - Language
     - python package
   * - cpp
     - `tree-sitter-python <https://github.com/tree-sitter/tree-sitter-python>`_
   * - python
     - `tree-sitter-cpp <https://github.com/tree-sitter/tree-sitter-cpp>`_

Reference
-------------------
.. autoclass:: ptcx.BasePTC
    :members:

.. toctree::
    :glob:
    :maxdepth: 2

    reference/*