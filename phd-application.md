---
layout: default
title: PhD Enquiry Form
permalink: /phd-application/
---

{% assign kcl_phd_url = "https://www.kcl.ac.uk/study/postgraduate-research/areas/engineering-phd" %}

# PhD Enquiry Form

{% include info-banner.html kind="warning" text="This form is for enquiries only. Formal PhD applications must be submitted via KCL." %}

<p class="inline-actions">
  {% include cta-button.html url=kcl_phd_url label="Apply" variant="primary" external=true %}
  {% include cta-button.html url="/positions/" label="Back to Join SAIL" variant="ghost" %}
</p>

Use this form to introduce your background and research interests before submitting a formal university application.

## What to include in your enquiry

- CV with degree details, grades, and relevant publications/projects
- A short statement of research interests and why SAIL is a good fit
- Links to code, papers, thesis, or technical portfolio (if available)

## Research areas at SAIL

- Data-centric computer architecture and systems
- Processing-in-Memory (PIM) and In-Storage Processing (ISP)
- Software-hardware co-design for AI and bioinformatics
- Reliable and secure memory/storage systems

## PhD enquiry form

{% include info-banner.html kind="info" text="Submitting this form does not submit a KCL application. Use the KCL portal for the official application." %}

<p>
  {% include cta-button.html url=kcl_phd_url label="Apply" variant="secondary" external=true %}
</p>

<iframe data-tally-src="https://tally.so/embed/0Q6D0N?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" loading="lazy" width="100%" height="1328" frameborder="0" marginheight="0" marginwidth="0" title="PhD Application Form"></iframe>
<script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>

---

<div class="form-note">
  <p><strong>Response time:</strong> Enquiries are reviewed on a rolling basis.</p>
  <p>For general enquiries, email <a href="mailto:haiyu.mao@kcl.ac.uk">haiyu.mao@kcl.ac.uk</a>.</p>
  <p><a href="{{ '/positions/' | relative_url }}">← Back to Positions</a></p>
</div>
