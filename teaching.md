---
layout: default
title: Teaching
permalink: /teaching/
---

# Teaching

We are a strong advocate for free and open sharing of teaching and research artifacts to democratize education worldwide. Course materials are made available online wherever possible.

<section class="teaching">
  {%- assign groups = site.data.courses | group_by: "semester" -%}
  {%- for group in groups -%}
    <h2 class="teaching-semester">{{ group.name }}</h2>
    <div class="course-list">
      {%- for c in group.items -%}
        <article class="course-item">
          <div class="course-meta">
            {%- if c.code -%}{{ c.code }} &middot; {%- endif -%}
            {{ c.level }}
          </div>
          <h3 class="course-title">
            {%- if c.url and c.url != "" -%}
              <a href="{{ c.url }}">{{ c.title }}</a>
            {%- else -%}
              {{ c.title }}
            {%- endif -%}
          </h3>
        </article>
      {%- endfor -%}
    </div>
  {%- endfor -%}
</section>
