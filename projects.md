---
layout: default
title: Projects
permalink: /projects/
---

# Projects

<div class="projects">
  {% for pr in site.data.projects %}
    {%- if pr.url and pr.url != "" -%}
      <a href="{{ pr.url }}" class="project-card-link">
    {%- endif -%}

    <article class="project-card">
      <div class="project-card-image">
        <img src="{{ pr.image | default: '/assets/img/gallery/20260806.png' | relative_url }}" alt="{{ pr.title }}">
      </div>

      <div class="project-card-content">
        <h3 class="project-card-title">
          {%- if pr.level -%}
            <span class="project-level">{{ pr.level }}</span>&nbsp;&nbsp;
          {%- endif -%}
          {{ pr.title }}
        </h3>
        {%- if pr.summary -%}
          <p class="project-card-desc">{{ pr.summary }}</p>
        {%- endif -%}

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
          <p class="project-links"><a class="course-highlight-tag project" href="{{ pdf_url }}" download>Download PDF</a></p>
        {%- endif -%}

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

    {%- if pr.url and pr.url != "" -%}
      </a>
    {%- endif -%}
  {% endfor %}
</div>
