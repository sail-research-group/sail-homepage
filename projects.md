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
        <h3>
          {{ pr.title }}
          {%- if pr.level -%}
            <span class="badge">{{ pr.level }}</span>
          {%- endif -%}
        </h3>

        {%- if pr.summary -%}
          <p>{{ pr.summary }}</p>
        {%- endif -%}

        {%- comment -%}
        Find a PDF URL: prefer `pr.pdf`, otherwise check `pr.links` for a PDF.
        {%- endcomment -%}
        {%- assign pdf_url = nil -%}
        {%- if pr.pdf -%}
          {%- assign pdf_url = pr.pdf -%}
        {%- elsif pr.links -%}
          {%- for l in pr.links -%}
            {%- if l.url contains ".pdf" or l.label == "PDF" or l.label == "pdf" -%}
              {%- assign pdf_url = l.url -%}
            {%- endif -%}
          {%- endfor -%}
        {%- endif -%}

        {%- if pdf_url -%}
          <p class="project-links"><a href="{{ pdf_url }}" download>Download PDF</a></p>
        {%- endif -%}

        {%- comment -%} Render explicit keywords if provided, otherwise try to match from site.data.keywords {%- endcomment -%}
        <div class="project-keywords">
        {%- if pr.keywords -%}
          {%- for kw in pr.keywords -%}
            <span class="keyword-tag">{{ kw }}</span>
          {%- endfor -%}
        {%- else -%}
          {%- for kw in site.data.keywords -%}
            {%- assign k = kw | downcase -%}
            {%- assign title = pr.title | default: "" | downcase -%}
            {%- assign summary = pr.summary | default: "" | downcase -%}
            {%- if title contains k or summary contains k -%}
              <span class="keyword-tag">{{ kw }}</span>
            {%- endif -%}
          {%- endfor -%}
        {%- endif -%}
        </div>
      </div>
    </article>
  {% endfor %}
</div>
