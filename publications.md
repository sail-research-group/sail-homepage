---
layout: default
title: Publications
permalink: /publications/
---

# Publications

<section class="pubs">
  {%- assign groups = site.data.publications | group_by: "year" | sort: "name" | reverse -%}

  {%- for year_group in groups -%}
    <h2 class="pub-year" id="y{{ year_group.name }}">{{ year_group.name }}</h2>
    <div class="pub-list">
      {%- for p in year_group.items -%}
        <article class="pub-item">
          <div class="pub-venue">
            {{ p.venue }}
          </div>
          <h3 class="pub-title">
            {{ p.title }}
          </h3>
          <div class="pub-authors">
            {{ p.authors }}
          </div>
          <div class="pub-links">
            {%- if p.pdf -%}
              <a class="pub-btn" href="{{ p.pdf | relative_url }}" target="_blank" rel="noopener">PDF</a>
            {%- endif -%}

            {%- if p.slides -%}
              <a class="pub-btn" href="{{ p.slides | relative_url }}" target="_blank" rel="noopener">Slides</a>
            {%- endif -%}

            {%- if p.poster -%}
              <a class="pub-btn" href="{{ p.poster | relative_url }}" target="_blank" rel="noopener">Poster</a>
            {%- endif -%}

            {%- if p.video -%}
              <a class="pub-btn" href="{{ p.video }}" target="_blank" rel="noopener">Talk</a>
            {%- endif -%}

            {%- if p.code -%}
              <a class="pub-btn" href="{{ p.code }}" target="_blank" rel="noopener">Code</a>
            {%- endif -%}

            {%- if p.doi -%}
              <a class="pub-btn" href="https://doi.org/{{ p.doi }}" target="_blank" rel="noopener">DOI</a>
            {%- endif -%}
          </div>
        </article>
      {%- endfor -%}
    </div>
  {%- endfor -%}
</section>