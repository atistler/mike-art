<div class="event_view_all">
	<div>
		<form class="form" action="/admin2/event/?create=1" method="post">
	        <h2>Create New Event</h2>
	        <div class="row">
	            <label class="col1"><span class="required">* </span>Name:</label>
	            <span class="col2"><input type="text" name="name"/></span>
	        </div>
	        <div class="row">
	            <label class="col1"><span class="required">* </span>When:</label>
	            <span class="col2"><input type="text" name="date"/></span>
	        </div>
	        <div class="row">
	            <label class="col1"><span class="required">* </span>Where:</label>
	            <span class="col2"><input type="text" name="location"/></span>
	        </div>
	        <div class="row">
	            <label class="col1"><span class="required">* </span>Priority:</label>
	            <span class="col2"><input type="text" name="priority"/></span>
	        </div>
			<div class="row">
				<span class="col1"><input type="submit" name="submit" value="Create"/></span>
			</div>
		</form>
	</div>
	<div>
		<table class="edit" cellspacing="0" cellpadding="3">
			<thead>
				<tr>
					<th colspan="6">
						Events
					</th>
				</tr>
				<tr>
					<th width="20%">Name</th>
					<th width="20%">When</th>
					<th width="20%">Where</th>
					<th width="20%">Priority</th>
					<th colspan=2 width="20%">Action</th>
				</tr>
			</thead>
			<tbody>
				{% if events %}
					{% for event in events %}
					<tr>
						<form action="/admin2/event/" method="post">
						<td><input type=text name=name value="{{event.name}}"/></td>
						<td><input type=text name=date value="{{event.date}}"/></td>
						<td><input type=text name=location value="{{event.location}}"/></td>
						<td><input type=text name=priority value="{{event.priority}}"/></td>
						<td>
							<input type="hidden" name="update" value="{{event.key}}"/>
							<input type="submit" value="Update"/>
						</td>
						<td>
							<input type="hidden" name="delete" value="{{event.key}}"/>
							<input type="submit" value="Delete"/>
						</td>
						</form>
					</tr>
					{% endfor %}
				{% else %}
					<tr>
						<td colspan="4" style="text-align:center">None</td>
					</tr>
				{% endif %}
			</tbody>
		</table>
	</div>
</div>
