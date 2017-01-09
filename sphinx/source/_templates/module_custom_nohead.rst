.. automodule:: {{ fullname }}

   {% block functions %}
   {% if functions %}
   Functions
   ---------
   .. autosummary::
      :toctree:

   {% for item in functions %}
      {{ item }}
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
