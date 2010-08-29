<div id="scroll" class="events scroll">
    {% for event in events %}
    <h4>{{event.name}}</h4>
    <table style="margin-left: 40px; margin-bottom: 20px;">
        <col width="80px"></col>
        <tbody>
            <tr>
                <td><b>Where:</b></td>
                <td><a href="" link_to="http://maps.google.com?q={{event.location}}" class="openlink tip" title="View in Google Maps" >{{event.location}}</a></td>
            </tr>
            <tr>
                <td><b>When:</b></td>
                <td>{{event.date}}</td>
                <td></td>
            </tr>
        </tbody>
    </table>
    {% endfor %}
</div>