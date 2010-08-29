<div class="nav">
	<ul>
		<li>
                    {% ifequal current_page 'home'}
                    <div class="current">
                    {% else %}
                    </div>
                    {% endifequal %}
                        <a id="home" href="/home"></a>
                    </div>
                </li>
		<li><a id="bio" href="/bio"></a></li>
		<li><a id="events" href="/events"></a></li>
		<li><a id="contacts" href="/contacts"></a></li>
		<li><a id="links" href="/links"></a></li>
	</ul>
</div>
