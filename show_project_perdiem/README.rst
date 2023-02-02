Show Project Per Diem
=====================
This module allows to define ``Per Diem`` on shows.

.. contents:: Table of Contents

Configuration
-------------
As ``Project / Manager``, under ``Project / Configuration / Per Diem Types``,
I find the list of per diem types.

.. image:: static/description/perdiem_type_list.png

.. image:: static/description/perdiem_type_form.png

Tour Configuration
------------------
As ``Project / Manager``, I go to a project of type ``Tour``.

I notice a new tab ``Per Diem`` containing a table.

.. image:: static/description/tour_form.png

This table allows to define unit amounts to pay for a given type of per diem.

..

    It is not possible to define multiple lines with the same per diem type.

New field **Notes** is created in "Per Diem" tab.

.. image:: static/description/notes_perdiem_page.png

Usage
-----
As ``Project / Manager``, I go to a project of type ``Show``.

In the tab ``Per Diem``, I notice a table ``Per Diem To Apply``.

.. image:: static/description/show_perdiem_to_apply.png

This table allows to define quantities of each type of per diem that are applicable
for this show.

..

    It is not possible to define multiple lines with the same per diem type.

I click on the button ``Compute Per Diem To Pay``.

.. image:: static/description/show_perdiem_button.png

The table below is filled with lines of per diem to pay, based on the quantities
defined on the show and the unit amounts defined on the tour.

.. image:: static/description/show_perdiem_computed.png

Each per diem is applicable for every member of the show.

.. image:: static/description/show_members.png

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)

More information
----------------
* Meet us at https://bit.ly/numigi-com
