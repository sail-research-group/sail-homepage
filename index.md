---
layout: default
title: SAIL
---

<h1>
  Welcome to
  <span class="sail-word sail-logo sail-heading">
    <span class="sail-letter sail-s">S</span><span class="sail-letter sail-a">A</span><span class="sail-letter sail-i">I</span><span class="sail-letter sail-l">L</span>
  </span>
  Research Group @ 
  <span class="kings-brand">King's College London</span>
</h1>

<!-- PICTURE GALLERY -->
<!-- name the pic as YEARMONTHDATE, e.g., 20251125, put in the ./assets/img/gallery/ -->

{% assign gallery_files = site.static_files
     | where_exp: "file", "file.path contains '/assets/img/gallery/'"
     | where_exp: "file", "file.name != 'static.jpg'"
     | sort: "name"
     | reverse %}

<div class="sail-gallery">
  <div class="sail-gallery-static">
    <img
      src="{{ '/assets/img/gallery/static.jpg' | relative_url }}"
      alt="SAIL research static image"
    >
  </div>

  <div class="sail-gallery-rotating">
    <img
      id="sail-rotating-image"
      src="{% if gallery_files.size > 0 %}
             {{ gallery_files[0].path | relative_url }}
           {% else %}
             {{ '/assets/img/gallery/static.jpg' | relative_url }}
           {% endif %}"
      alt="SAIL research gallery"
    >
  </div>
</div>

<script>
  (function() {
    const images = [
      {% for f in gallery_files %}
        "{{ f.path | relative_url }}"{% unless forloop.last %},{% endunless %}
      {% endfor %}
    ];

    const imgEl = document.getElementById('sail-rotating-image');
    let index = 0;

    function showNextImage() {
      if (images.length === 0) return;
      index = (index + 1) % images.length;
      imgEl.src = images[index];
    }

    if (images.length > 0) {
      // already showing images[0] (newest) via the HTML src
      setInterval(showNextImage, 2000);
    }
  })();
</script>


<p class="sail-explainer">
  <span class="sail-word sail-logo">
    <span class="sail-letter sail-s">S</span><span class="sail-letter sail-a">A</span><span class="sail-letter sail-i">I</span><span class="sail-letter sail-l">L</span>
  </span>
  stands for
  <span class="sail-word">
    <span class="sail-letter sail-s">S</span>ystem
  </span>
  and
  <span class="sail-word">
    <span class="sail-letter sail-a">A</span>rchitecture
  </span>
  for
  <span class="sail-word">
    <span class="sail-letter sail-i">I</span>ntelligent
  </span>
  <span class="sail-word">
    <span class="sail-letter sail-l">L</span>iving
  </span>.
</p>

SAIL Research Group is led by **[Haiyu Mao](https://hybol1993.github.io/)**.

We are part of the **[Department of Engineering](https://www.kcl.ac.uk/engineering)** at **[King's College London](https://www.kcl.ac.uk/)**.

**Our mission:** We co-design software and hardware to power data-intensive applications for a healthier, simpler everyday life.

**Our Key Research Directions:**
- Computer Architecture and System
- Software and Hardware Co-Design
- Data-centric Architectures: Processing In Memory (PIM), In-Storage Processing (ISP), …
- Acceleration of Data-Intensive Applications for Healthier and Simpler Life: AI, Bioinformatics, …
- Emerging Memory and Storage Technologies 
- Reliable Architecture and System


<!-- News block -->
<h2>News</h2>

<div class="news-list">
  {% assign news = site.data.news | sort: 'date' | reverse %}
  {% for item in news limit:5 %}
    <article class="news-item">
      <div class="news-date">
        {{ item.date | date: "%Y-%m-%d" }}
      </div>
      <div class="news-title">
        {% if item.url %}
          <a href="{{ item.url }}" target="_blank" rel="noopener">
            {{ item.title }}
          </a>
        {% else %}
          {{ item.title }}
        {% endif %}
      </div>
      {% if item.summary %}
        <div class="news-summary">
          {{ item.summary }}
        </div>
      {% endif %}
    </article>
  {% endfor %}
</div>