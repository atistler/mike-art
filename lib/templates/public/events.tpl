<div id="scroll" class="events">
    {% for event in events %}
    <h5>{{event.name}}</h5>
    <table style="margin-left: 40px;">
        <col width="80px"></col>
        <col></col>
        <col width="10%"></col>
        <tbody>
            <tr>
                <td>Where:</td>
                <td>{{event.location}}</td>
                <td>
                    <img style="padding-left:10px;"width="20px" height="20px" title="View Map" class="openlink" href="http://maps.google.com?q={{event.location}}" src="/img/map-icon.png"/>
                </td>
            </tr>
            <tr>
                <td>When:</td>
                <td>{{event.date}}</td>
                <td></td>
            </tr>
        </tbody>
    </table>
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
