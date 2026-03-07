---
header: images/rainbow_background_header_1.png
header-dark: true   # optional, if you want the dark treatment
---


We are a neuroscience lab that studies how the brain builds predictions to support homeostasis. 

<p class="home-lead-shift-small">
  As part of a broader scientific collective, we are also developing and open-sourcing foundational datasets and models for detecting, tracking, and sequencing rodent behavior to unify scientific discoveries across experimental conditions.
</p>

<p class="home-lead-shift-medium">
  We are part of the University of Washington's
  <a href="https://uwmdi.org" target="_blank" rel="noopener noreferrer">
    Diabetes Institute
  </a>.
</p>

{% include section.html background="images/background.png" dark=false %}


## Explore

{% capture text %}

Browse our published manuscripts, datasets, and repositories.

{%
  include button.html
  link="research"
  text="See our publications"
  icon="fa-solid fa-arrow-right"
  flip=true
  style="bare"
%}

{% endcapture %}

{%
  include feature.html
  image="images/brainRotationYYcolor.gif"
  link="research"
  title="Our Research"
  text=text
%}

{% capture text %}

Take a look at our ongoing projects -- we're combining state-of-the-art neuroscience and machine learning approaches to map brain networks that predict blood glucose and building tools to sequence rodent behavior.

{%
  include button.html
  link="projects"
  text="Browse our projects"
  icon="fa-solid fa-arrow-right"
  flip=true
  style="bare"
%}

{% endcapture %}

{%
  include feature.html
  image="images/rainbowvid1_pad.gif"
  link="projects"
  title="Our Projects"
  flip=true
  style="bare"
  text=text
%}

{% capture text %}

Get to know our group members -- we're working out of the University of Washington's South Lake Union Campus.

{%
  include button.html
  link="team"
  text="Meet our team"
  icon="fa-solid fa-arrow-right"
  flip=true
  style="bare"
%}

{% endcapture %}

{%
  include feature.html
  image="images/SLU.jpg"
  link="team"
  title="Our Team"
  text=text
%}
