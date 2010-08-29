<div id="slideshow_description" style="float:right; width: 300px; height:90px; margin-right:50px">
    {{ gal.desc }}
    <br />
    <br />
    <a href="/{{gal_name}}/flash" link_to="/{{gal_name}}/flash" class="openlink">View Flash Slideshow</a>
</div>
<div id="my_slideshow" class="slideshow">
{% comment %}
    {% for img in imgs %}
	{% ifequal forloop.first 1 %}
            <img src="/image/?render={{img.key}}"/>
	{% endifequal %}
    {% endfor %}
{% endcomment %}
</div>
<script type="text/javascript">
	var data = {
	{% for img in imgs %}
		{% if forloop.last %}
  		'/image/?render={{img.key}}': {
    		caption: '{{img.name}}', 
    		thumbnail: '/image/?render_thumb={{img.key}}'
  		}
		{% else %}
  		'/image/?render={{img.key}}': {
    		caption: '{{img.name}}', 
    		thumbnail: '/image/?render_thumb={{img.key}}'
  		},
		{% endif %}
	{% endfor %}
	};
</script>
