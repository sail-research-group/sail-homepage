---
layout: default
title: Publications
permalink: /publications/
---

{%- assign all_people = site.data.leader -%}
{%- if site.data.phds.size > 0 -%}{%- assign all_people = all_people | concat: site.data.phds -%}{%- endif -%}
{%- if site.data.masters.size > 0 -%}{%- assign all_people = all_people | concat: site.data.masters -%}{%- endif -%}
{%- if site.data.interns.size > 0 -%}{%- assign all_people = all_people | concat: site.data.interns -%}{%- endif -%}
{%- if site.data.visitings.size > 0 -%}{%- assign all_people = all_people | concat: site.data.visitings -%}{%- endif -%}

# Publications

<section class="pub-filters" aria-label="Publication filters">
  <div class="pub-filter-controls">
    <input type="search" id="pub-search" class="pub-search" placeholder="Search by keyword, title, or author…" autocomplete="off">
    <label class="pub-sort-label">
      Sort
      <select id="pub-sort" class="pub-sort">
        <option value="newest">Newest first</option>
        <option value="oldest">Oldest first</option>
        <option value="venue">Venue A–Z</option>
      </select>
    </label>
    <button type="button" id="pub-topic-toggle" class="pub-topic-toggle" aria-expanded="true">
      Keywords <span class="pub-topic-toggle-icon">&#9662;</span>
    </button>
    <button type="button" id="pub-clear" class="pub-clear">Clear</button>
  </div>

  {%- assign keyword_list = site.data.keywords -%}
  {%- if keyword_list.size > 0 -%}
  <div class="pub-keyword-row">
    <span class="pub-keyword-label">Keywords</span>
    <div class="pub-keyword-chips">
      {%- for kw in keyword_list -%}
        <button type="button" class="pub-keyword-chip" data-keyword="{{ kw | downcase }}">{{ kw }}</button>
      {%- endfor -%}
    </div>
  </div>
  {%- endif -%}
</section>

<section class="pubs">
  {%- assign groups = site.data.publications | group_by: "year" | sort: "name" | reverse -%}

  {%- for year_group in groups -%}
    <h2 class="pub-year" id="y{{ year_group.name }}" data-year="{{ year_group.name }}">{{ year_group.name }}</h2>
    <div class="pub-list" data-year="{{ year_group.name }}">
      {%- for p in year_group.items -%}
        <article class="pub-item"
                 data-year="{{ p.year }}"
                 data-venue="{{ p.venue | escape }}"
                 data-type="{{ p.type }}"
                 data-authors="{{ p.authors | escape }}"
                 data-title="{{ p.title | escape }}"
                 data-keywords="{{ p.keywords | join: ',' | downcase }}">
          <h3 class="pub-title"><span class="pub-venue">{{ p.venue }}</span> {{ p.title }}</h3>
          <div class="pub-authors">
            {%- assign authors = p.authors | split: ", " -%}
            {%- for author in authors -%}
              {%- assign person = all_people | where: "name", author | first -%}
              {%- if person -%}
                {%- if person.web -%}
                  <a href="{{ person.web }}" class="sail-link">{{ author }}</a>
                {%- elsif person.url -%}
                  <a href="{{ person.url }}" class="sail-link">{{ author }}</a>
                {%- else -%}
                  <a href="/people/#{{ author | slugify }}" class="sail-link">{{ author }}</a>
                {%- endif -%}
              {%- else -%}
                <span class="external-author">{{ author }}</span>
              {%- endif -%}
              {%- unless forloop.last -%}, {% endunless -%}
            {%- endfor -%}
          </div>
          <div class="pub-actions-row">
            {%- if p.keywords -%}
            <div class="pub-keywords">
              {%- for kw in p.keywords -%}
                <span class="pub-kw-tag">{{ kw }}</span>
              {%- endfor -%}
            </div>
            {%- endif -%}
            <div class="pub-actions">
              {%- if p.abstract -%}
                <button type="button" class="pub-btn pub-abstract-toggle" aria-expanded="false">Abstract <span class="pub-abstract-arrow">&#9662;</span></button>
              {%- endif -%}
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
              {%- if p.bibtex -%}
                <button type="button" class="pub-btn pub-btn-bibtex" data-bibtex="{{ p.bibtex | escape }}">BibTeX</button>
              {%- endif -%}
            </div>
          </div>
          {%- if p.abstract -%}
          <div class="pub-abstract-body">
            <p>{{ p.abstract }}</p>
          </div>
          {%- endif -%}
        </article>
      {%- endfor -%}
    </div>
  {%- endfor -%}

  <p class="pub-empty" hidden>No publications match the current filters.</p>
</section>

<script src="{{ '/assets/js/publications-filter.js' | relative_url }}" defer></script>
