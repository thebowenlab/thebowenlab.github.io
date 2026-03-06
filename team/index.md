---
title: Team
nav:
  order: 3
  tooltip: About our team
---

# {% include icon.html icon="fa-solid fa-users" %}Team

We're lucky to be part of the University of Washington network, enabling rich collaborations with experts in neural computation, machine learning, physiology, medicine, pharmacology, and biochemistry.  

{% include section.html %}

{% include list.html data="members" component="portrait" filter="role == 'pi'" %}
{% include list.html data="members" component="portrait" filter="role != 'pi'" %}

{% include section.html background="images/background.png" dark=true %}

{% include section.html %}

{% capture content %}

{% include figure.html image="images/seasonal/spring/cherry_bud.jpeg"  %}
{% include figure.html image="images/seasonal/spring/cherry_quad_1.jpeg" %}
{% include figure.html image="images/seasonal/spring/cherry_double.jpeg" %}

{% endcapture %}

{% include grid.html style="square" content=content %}
