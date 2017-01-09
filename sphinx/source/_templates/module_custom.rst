:mod:`{{ fullname }}`
======={{ underline }}

.. automodule:: {{ fullname }}

   {% block functions %}
   {% if functions %}
   Functions
   ---------
   .. autosummary::
      :toctree:generated/
      :template:func_custom.rst
      
   {# to include private functions, use *all_functions* below #}
   {% for item in functions %}
      {{ item }}
   {%- endfor %}

   .. toctree::
       :maxdepth: 1
       :hidden:

   {% for item in functions %}
       generated/{{ fullname }}.{{ item }}
   {%- endfor %}
      
   {% endif %}
   {% endblock %}

   {% block classes %}
   {% if classes %}
   Classes
   -------
   .. autosummary::
      :toctree:generated/
      :template:class_custom.rst

   {% for item in classes %}
      {{ item }}
   {%- endfor %}

   .. toctree::
       :maxdepth: 1
       :hidden:

   {% for item in classes %}
       generated/{{ fullname }}.{{ item }}
   {%- endfor %}

   {% endif %}
   {% endblock %}

   {% block exceptions %}
   {% if exceptions %}
   Exceptions
   ----------
   .. autosummary::
      :toctree:

   {% for item in exceptions %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}
