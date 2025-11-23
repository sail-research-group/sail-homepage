---
layout: default
title: Home
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
      src="{{ '/assets/img/gallery/slide1.png' | relative_url }}"
      alt="SAIL research gallery"
    >
  </div>
</div>

<script>
  (function() {
    // List of rotating images (add/remove as you like)
    const images = [
      "{{ '/assets/img/gallery/slide1.png' | relative_url }}",
      "{{ '/assets/img/gallery/slide2.jpg' | relative_url }}"
    ];

    const imgEl = document.getElementById('sail-rotating-image');
    let index = 0;

    function showNextImage() {
      index = (index + 1) % images.length;
      imgEl.src = images[index];
    }

    // Change image every 2000 ms (2 seconds)
    setInterval(showNextImage, 2000);
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

Our Key Research Directions:
- Computer Architecture and System
- Software and Hardware Co-Design
- Data-centric Architectures: Processing In Memory (PIM), In-Storage Processing (ISP), …
- Acceleration of Data-Intensive Applications for Healthier and Simpler Life: AI, Bioinformatics, …
- Emerging Memory and Storage Technologies 
- Reliable Architecture and System

