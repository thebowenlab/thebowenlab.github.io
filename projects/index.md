---
title: Projects
nav:
  order: 2
  tooltip: Software, datasets, and more
---

# {% include icon.html icon="fa-solid fa-wrench" %}Projects

{% include section.html background="images/background.png" dark=true %}

We hypothesize that the brain contributes to blood glucose regulation in a **predictive** way -- integrating external cues (appearance/smell/taste of food), nutrient sensing, and knowledge of the body’s own actions and energy use to act as a proactive glycemic controller.

Project round-up:
* Mapping disease-coupled changes in glucose forecasting and sensory encoding using wide-scale Neuropixels recordings and cue-based learning tasks in mice 
* Functional delineation of physiological and behavioral outputs using Neuropixels Opto-based manipulations in glucose-forecasting networks   
* Developing multi-modal deep learning models to jointly encode neural activity, behavior, and physiological state
* Creating and training model pipelines and user interfaces to model behavior at-scale 

{% include tags.html tags="publication, resource, collaboration" %}

{% include search-info.html %}

## Featured

{% include list.html component="card" data="projects" filter="group == 'featured'" %}


**Approach** To study how the brain supports glycemic control, we combine state-of-the-art systems neuroscience approaches in mice, including large-scale neural recordings with Neuropixels probes, continuous glucose monitoring, computational analysis, and self-supervised behavioral analysis.

We first identify brain networks that forecast blood glucose levels and examine how these networks also represent other sensory and behavioral variables, such as taste. We then test how these network coding properties change in disease models. Our goal is to build a spatiotemporal map of how disease affects glycemic control networks and to identify therapeutic strategies that help restore healthier patterns of brain activity.
{% include section.html %}
## More

{% include list.html component="card" data="projects" filter="!group" style="small" %}
{% include section.html %}
