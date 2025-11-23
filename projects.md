---
layout: default
title: Projects
permalink: /projects/
---

# Projects

<div class="projects">
  {% for pr in site.data.projects %}
    <article class="project-card">
      {% if pr.image %}
        <div class="project-image">
          <img src="{{ pr.image | relative_url }}" alt="{{ pr.title }} image">
        </div>
      {% endif %}

      <div class="project-content">
        <h3>{{ pr.title }}</h3>
        {% if pr.status %}
          <p class="badge">{{ pr.status }}</p>
        {% endif %}
        <p>{{ pr.summary }}</p>

        {% if pr.links %}
          <p class="project-links">
          {% for l in pr.links %}
            <a href="{{ l.url }}" target="_blank" rel="noopener">{{ l.label }}</a>{% if forloop.last == false %} · {% endif %}
          {% endfor %}
          </p>
        {% endif %}
      </div>
    </article>
  {% endfor %}
</div>
