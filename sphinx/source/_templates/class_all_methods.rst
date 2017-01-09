{{ fullname }}
{{ underline }}
.. currentmodule:: {{ module }}
.. autoclass:: {{ objname }}
   :undoc-members:
{% block methods %}
{% if methods %}
Methods
-------
.. autosummary::
   :toctree:

{% for item in all_methods %}
   ~{{ name }}.{{ item }}
{%- endfor %}
{% endif %}
{% endblock %}

{% block attributes %}
{% if attributes %}
Attributes
----------
.. autosummary::
  :toctree:

{% for item in attributes %}
   ~{{ name }}.{{ item }}
{%- endfor %}
{% endif %}
{% endblock %}