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

{% include section.html background="images/background.jpg" dark=true %}

## Join us

### Undergraduates 
If you're a driven CS student wanting to develop AI models with real-world benefit, or a curious neuroscience or biology student wanting to work with big data and modern methods, reach out about interning in the lab -- we'd love to work with you!

### Postdoctoral scientists
If you'd like to use state-of-the-art computational and neuroscience methods to answer questions with direct translational relevance, we'd love to hear from you! Informal inquiries welcome to abowen5@uw.edu.

{% include section.html %}

{% capture content %}

{% include figure.html image="images/photo.jpg" %}
{% include figure.html image="images/photo.jpg" %}
{% include figure.html image="images/photo.jpg" %}

{% endcapture %}

{% include grid.html style="square" content=content %}
