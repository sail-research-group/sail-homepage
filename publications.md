---
layout: default
title: Publications
permalink: /publications/
---

# Publications

<table>
  <thead><tr><th>Year</th><th>Title</th><th>Authors</th><th>Venue</th><th>Links</th></tr></thead>
  <tbody>
  {% assign pubs = site.data.publications | sort: 'year' | reverse %}
  {% for p in pubs %}
    <tr>
      <td>{{ p.year }}</td>
      <td>{{ p.title }}</td>
      <td>{{ p.authors }}</td>
      <td>{{ p.venue }}</td>
      <td>
        {% if p.doi %}<a href="https://doi.org/{{ p.doi }}" target="_blank" rel="noopener">DOI</a>{% endif %}
        {% if p.pdf %} {% if p.doi %} | {% endif %}<a href="{{ p.pdf }}" target="_blank" rel="noopener">PDF</a>{% endif %}
        {% if p.code %} | <a href="{{ p.code }}" target="_blank" rel="noopener">Code</a>{% endif %}
      </td>
    </tr>
  {% endfor %}
  </tbody>
</table>
