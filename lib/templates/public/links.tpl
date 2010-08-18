<div class="links">
<ul style="list-style-type: circle">
{% for link in links %}
	<li style="margin-bottom: 10px;"><a href="{{ link.link }}" title="{{ link.name }}" style="font-size:16px;">{{ link.name }}</a></li>
{% endfor %}
</ul>
</div>
