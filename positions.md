---
layout: default
title: Join SAIL
permalink: /positions/
---

{% assign kcl_phd_url = "https://www.kcl.ac.uk/study/postgraduate-research/areas/engineering-phd" %}
{% assign star_ai_url = "https://www.kcl.ac.uk/research/star-ai" %}

<div class="recruit-page">

<section class="recruit-hero">
  <p class="eyebrow">SAIL Recruitment</p>
  <h1>Join SAIL</h1>
  <p class="lead">We welcome enquiries from researchers and students who are excited about computer architecture and systems for AI and data-intensive applications. This includes data-intensive applications, such as AI and bioinformatics applications.</p>
  <p class="lead">SAIL enquiries help us assess fit. Formal applications are submitted through King's College London.</p>
  <div class="hero-actions">
    {% include cta-button.html url="#paths-to-join" label="Make an enquiry" variant="primary" %}
    {% include cta-button.html url=kcl_phd_url label="Apply" variant="secondary" external=true %}
  </div>
</section>

{% include info-banner.html kind="warning" text="Important: Submitting the SAIL form is not a university application." %}

<section class="recruit-section">
  <h2>How joining works</h2>
  <div class="steps-grid">
    <article class="step-card">
      <div class="step-icon" aria-hidden="true">1</div>
      <h3>Enquire with SAIL</h3>
      <p>Share your background, interests, and evidence of strong research alignment.</p>
    </article>
    <article class="step-card">
      <div class="step-icon" aria-hidden="true">2</div>
      <h3>We review and respond</h3>
      <p>We review enquiries promptly and respond when your profile aligns well.</p>
    </article>
    <article class="step-card">
      <div class="step-icon" aria-hidden="true">3</div>
      <h3>Apply through KCL</h3>
      <p>If invited, complete the formal KCL application to move forward.</p>
    </article>
  </div>
</section>

<section id="paths-to-join" class="recruit-section">
  <h2>Paths to join SAIL</h2>
  <div class="recruit-grid">
    {% include recruitment-card.html
      title="PhD"
      body="Enquire first so we can check research alignment and supervision capacity."
      points="Data-centric architecture, PIM/ISP, AI systems, memory/storage reliability"
      enquiry_url="/phd-application/"
      enquiry_label="Enquire (SAIL form)"
      apply_url=kcl_phd_url
      apply_label="Apply"
    %}

    {% include recruitment-card.html
      title="Funded studentships"
      body="Occasional funded calls open during the year."
      points="Availability changes by scheme and cycle"
      apply_url=star_ai_url
      apply_label="More info"
    %}

    {% include recruitment-card.html
      title="Postdocs and fellowships"
      body="We welcome strong fellowship ideas aligned with SAIL priorities."
      points="Share a concise proposal, timeline, and potential funding scheme"
      enquiry_url="/internship-application/"
      enquiry_label="Enquire (SAIL form)"
    %}

    {% include recruitment-card.html
      title="KCL MSc/BSc projects"
      body="For current KCL students seeking research projects or dissertation supervision."
      points="Include modules taken, coding experience, and preferred topic"
      enquiry_url="/internship-application/"
      enquiry_label="Enquire (SAIL form)"
    %}

    {% include recruitment-card.html
      title="Visiting students and scholars"
      body="We can host short-term visits where there is clear research fit and confirmed funding."
      points="Typical duration 3 to 12 months"
      enquiry_url="/internship-application/"
      enquiry_label="Enquire (SAIL form)"
    %}
  </div>
</section>

<section class="recruit-section">
  <h2>Research focus and candidate fit</h2>
  <div class="bullet-columns">
    <article class="bullet-panel">
      <h3>Topics we are currently exploring</h3>
      <ul class="compact-list">
        <li>Data-centric computer architecture and systems</li>
        <li>Processing-in-Memory (PIM) and In-Storage Processing (ISP)</li>
        <li>Software-hardware co-design for AI and bioinformatics</li>
        <li>Reliable and secure memory and storage systems</li>
      </ul>
    </article>
    <article class="bullet-panel">
      <h3>What strengthens an enquiry</h3>
      <ul class="compact-list">
        <li>Strong fundamentals in architecture, systems, or related fields</li>
        <li>Hands-on programming in C/C++ and/or Python</li>
        <li>Specific research interests rather than broad topic labels</li>
        <li>Evidence of research potential: projects, papers, artifacts, or open-source work</li>
      </ul>
    </article>
  </div>
</section>

<section class="recruit-section">
  <h2>Frequently asked questions</h2>
  <div class="faq-list">
    <details>
      <summary>Do I need to apply on KCL as well?</summary>
      <p>Yes. The SAIL form is an enquiry and fit-check route. Formal admissions decisions only happen through the official KCL application process.</p>
    </details>
    <details>
      <summary>What should I include in my enquiry?</summary>
      <p>Share your CV, your current stage (degree or role), 2 to 3 research interests, relevant project links, and why SAIL is a fit.</p>
    </details>
    <details>
      <summary>Can you review my CV before I apply?</summary>
      <p>Yes, we can give brief fit-oriented feedback when capacity allows, but this does not replace the KCL admissions review.</p>
    </details>
    <details>
      <summary>What funding routes are possible?</summary>
      <p>Funding can include self-funded routes, scholarships, or occasional funded calls. Eligibility depends on the scheme and your profile.</p>
    </details>
    <details>
      <summary>How long does it take to hear back?</summary>
      <p>Enquiries are reviewed on a rolling basis. Response time varies with volume, but we aim to reply as promptly as possible for strong fits.</p>
    </details>
  </div>
</section>

</div>
