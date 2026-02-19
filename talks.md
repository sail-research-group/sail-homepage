---
layout: default
title: Talks
permalink: /talks/
---

{% assign research_talks = site.data.talks | where: "type", "research" %}
{% assign teaching_talks = site.data.talks | where: "type", "teaching" %}

## Research Talks

<section class="talks">
  {%- assign groups = research_talks | group_by: "year" | sort: "name" | reverse -%}

  {%- for year_group in groups -%}
    <h2 class="talk-year" id="y{{ year_group.name }}">{{ year_group.name }}</h2>
    <div class="talk-list">
      {%- for p in year_group.items -%}
        <article class="talk-item">
          <div class="talk-venue">{{ p.venue }}</div>
          <h3 class="talk-title">{{ p.title }}</h3>
          <div class="talk-meta">
            <div class="talk-presenter">
              {%- assign person = site.data.leader | concat: site.data.phds | concat: site.data.interns | where: "name", p.presenter | first -%}
              {%- if person -%}
                <a href="/people/#{{ p.presenter | slugify }}" class="sail-link">{{ p.presenter }}</a>
              {%- elsif p.presenter_link -%}
                <a href="{{ p.presenter_link }}" target="_blank" rel="noopener" class="external-link">{{ p.presenter }}</a>
              {%- else -%}
                {{ p.presenter }}
              {%- endif -%}
            </div>
            <span class="talk-date">{{ p.date }}</span>
            <span class="talk-location">{{ p.location }}</span>
            {%- if p.video -%}
              <a class="talk-btn" href="{{ p.video }}" target="_blank" rel="noopener">Video</a>
            {%- endif -%}
            {%- if p.description -%}
              <span class="talk-description-inline">{{ p.description }}</span>
            {%- endif -%}
          </div>
        </article>
      {%- endfor -%}
    </div>
  {%- endfor -%}
</section>

## Teaching Talks

<section class="talks">
  {%- assign groups = teaching_talks | group_by: "year" | sort: "name" | reverse -%}

  {%- for year_group in groups -%}
    <h2 class="talk-year" id="y{{ year_group.name }}">{{ year_group.name }}</h2>
    <div class="talk-list">
      {%- for p in year_group.items -%}
        <article class="talk-item">
          <div class="talk-venue">{{ p.venue }}</div>
          <h3 class="talk-title">{{ p.title }}</h3>
          <div class="talk-meta">
            <div class="talk-presenter">
              {%- assign person = site.data.leader | concat: site.data.phds | concat: site.data.interns | where: "name", p.presenter | first -%}
              {%- if person -%}
                <a href="/people/#{{ p.presenter | slugify }}" class="sail-link">{{ p.presenter }}</a>
              {%- elsif p.presenter_link -%}
                <a href="{{ p.presenter_link }}" target="_blank" rel="noopener" class="external-link">{{ p.presenter }}</a>
              {%- else -%}
                {{ p.presenter }}
              {%- endif -%}
            </div>
            <span class="talk-date">{{ p.date }}</span>
            <span class="talk-location">{{ p.location }}</span>
            {%- if p.video -%}
              <a class="talk-btn" href="{{ p.video }}" target="_blank" rel="noopener">Video</a>
            {%- endif -%}
            {%- if p.description -%}
              <span class="talk-description-inline">{{ p.description }}</span>
            {%- endif -%}
          </div>
        </article>
      {%- endfor -%}
    </div>
  {%- endfor -%}
</section>