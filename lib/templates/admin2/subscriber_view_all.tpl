<div class="subscriber_view_all">
	<div style="margin-left: 100px">
		<form name="export" action="/admin2/subscriber/" method="get">
			<input type="submit" name="export" value="Export as Text"></input>
		</form>
	</div>
	<div>
		<table class="edit" cellspacing="0" cellpadding="3">
			<thead>
				<tr>
					<th colspan="4">
						Mailing List Subscribers	
					</th>
				</tr>
				<tr>
					<th width="30%">First Name</th>
					<th width="30%">Last Name</th>
					<th width="30%">Email</th>
					<th width="20%">Action</th>
				</tr>
			</thead>
			<tbody>
				{% if subscribers %}
					{% for subscriber in subscribers %}
					<tr>
						<td>{{subscriber.fname}}</td>
						<td>{{subscriber.lname}}</td>
						<td>{{subscriber.email}}</td>
						<td>
							<form action="/admin2/subscriber/" method="post">
								<input type="hidden" name="delete" value="{{subscriber.key}}"/>
								<input type="submit" value="Delete"/>
							</form>
						</td>
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
