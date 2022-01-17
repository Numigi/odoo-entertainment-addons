Show Project
============

.. contents:: Table of Contents

Context
-------
The module `project_iteration <https://github.com/Numigi/odoo-project-addons/tree/12.0/project_iteration>`_
defines the concept of a parent and a child project (a.k.a. the iteration).

Description
-----------
This module allows to use the ``Projects`` application to manage musical shows and tours.

Tours are represented as parent projects and shows are represented as children (iterations) of a tour.

Usage
-----
I open the form view of a project in creation mode.

I notice a new selection field.
It allows to define the project as either, a tour, a show or a standard project.

.. image:: static/description/project_new.png

Tour
~~~~
First, I create a project of type ``Tour``.

Show
~~~~
I create a project of type ``Show``.

.. image:: static/description/show_create.png

For projects of type ``Show``, the field ``Parent`` is mandatory.
You may only select a parent project of type ``Tour``.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
* Komit (https://komit-consulting.com)

More information
----------------
* Meet us at https://bit.ly/numigi-com
