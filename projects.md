---
layout: default
title: Projects
permalink: /projects/
---

# Projects

<div class="card-grid">
{% for pr in site.data.projects %}
  <div class="card">
    <h3>{{ pr.title }}</h3>
    {% if pr.status %}<p class="badge">{{ pr.status }}</p>{% endif %}
    <p>{{ pr.summary }}</p>
    {% if pr.links %}
      <p>
      {% for l in pr.links %}
        <a href="{{ l.url }}" target="_blank" rel="noopener">{{ l.label }}</a>{% if forloop.last == false %} · {% endif %}
      {% endfor %}
      </p>
    {% endif %}
  </div>
{% endfor %}
</div>
