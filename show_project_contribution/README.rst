Show Project Contribution
=========================
This module allows to define employee payroll contributions on shows.

Configuration
-------------
As ``Payroll / Manager``, under ``Payroll / Configuration / Contribution Types``,
I find the list of contribution types.

.. image:: static/description/contribution_type_list.png

.. image:: static/description/contribution_type_form.png

Under ``Payroll / Configuration / Contribution Bases``, I find the list of contribution bases.

.. image:: static/description/contribution_base_list.png

.. image:: static/description/contribution_base_form.png

As ``Human Resources / Manager``, I can define applicable contribution types for an employee.

.. image:: static/description/employee_form.png

Usage
-----
In the form view of a project of type ``Show``, I can define applicable contribution bases.

.. image:: static/description/show_contribution_bases.png

..

	It is not possible to select multiple contribution bases of the same type.

Then, I click on ``Compute Contribution Bases``.

.. image:: static/description/show_contribution_button.png

Based on the team members of this show, the list of contributions is computed.

.. image:: static/description/show_team_members.png

.. image:: static/description/show_contributions_computed.png

How Contributions Are Computed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For each applicable contribution defined on the show, if the contribution type is defined on
the employee related to a member of the team, this contribution is applied for this member.

The relation between the partner and the employee is done through the field ``Work Address``.

.. image:: static/description/employee_work_address.png

If a member has no related employee, an error message is displayed.

.. image:: static/description/no_related_employee_error.png

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)

More information
----------------
* Meet us at https://bit.ly/numigi-com
