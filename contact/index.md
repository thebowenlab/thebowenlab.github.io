---
title: Contact
nav:
  order: 5
  tooltip: Email, address, and location
---

# {% include icon.html icon="fa-regular fa-envelope" %}Contact

{% include section.html background="images/background.png" dark=true %}

<div class="contact-hero-grid">
  <div>
    We are located at the University of Washington's South Lake Union Campus.

    <br><br>

    <strong>Lab Mailing Address:</strong>
    <br>Anna Bowen
    <br>750 Republican Street
    <br>F741
    <br>Seattle, WA 98109

    <br><br>

    <div class="contact-buttons-left">
      {% include button.html type="email" text="abowen5@uw.edu" link="abowen5@uw.edu" %}
      {% include button.html type="phone" text="(206) 897-9898" link="+1-206-897-9898" %}
      {% include button.html type="address" tooltip="Our location on Google Maps for easy navigation" link="https://maps.app.goo.gl/GrezeT3XjjsAWVxr5" %}
    </div>
  </div>

  <div>
    {% include figure.html image="images/SLU.jpg" caption="South Lake Union Campus" %}
  </div>
</div>

{% include section.html %}
{% include section.html %}
{% capture col1 %}

{%
  include figure.html
  image="images/SLU_lake.webp"
  caption="South Lake Union"
%}

{% endcapture %}

{% capture col2 %}

{%
  include figure.html
  image="images/SLU.jpg"
  caption="South Lake Union Campus"
%}

{% endcapture %}

{% capture col3 %}

{%
  include figure.html
  image="images/SLU_space-needle.webp"
  caption="Space Needle"
%}

{% endcapture %}

{% include cols.html col1=col1 col2=col2 col3=col3%}



