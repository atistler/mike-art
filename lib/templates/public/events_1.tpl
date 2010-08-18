<div id="scroll" class="events">
    {% for event in events %}
    <h4>{{event.name}}</h4>
    <dl>
        <dt>Where:</dt>
        <dd>
            <div>{{event.location}}
                <img title="View Map" class="openlink" href="http://maps.google.com?q={{event.location}}" width=25px height=25px src="/img/map-icon.png"/>
            </div>
        </dd>
        <dt>When:</dt>
        <dd>{{event.date}}</dd>
    </dl>
    {% endfor %}
</div>
<div id="track_event">
    <div id="thumb_event"></div>
</div>

<script type="text/javascript">
var scr = new ScrollBar('scroll', 'track_event', 'thumb_event');
        new Drag('scroll', {
                'modifiers': {y: 'height', x: false},
                onDrag: function(){
                        scr.update();
                }
        });
</script>
