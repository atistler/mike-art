<div class="link_view_all">
	<div>
		<form class="form" action="/admin2/link/?create=1" method="post">
	        <h2>Create New Link</h2>
	        <div class="row">
	            <label class="col1"><span class="required">* </span>Name:</label>
	            <span class="col2"><input type="text" name="name"/></span>
	        </div>
	        <div class="row">
	            <label class="col1"><span class="required">* </span>URL:</label>
	            <span class="col2"><input type="text" name="link"/></span>
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
					<th colspan="5">
						Links
					</th>
				</tr>
				<tr>
					<th width="20%">Name</th>
					<th width="20%">URL</th>
					<th width="20%">Priority</th>
					<th colspan=2 width="40%">Action</th>
				</tr>
			</thead>
			<tbody>
				{% if links %}
					{% for link in links %}
					<tr>
						<form action="/admin2/link/" method="post">
						<td><input type=text name=name value="{{link.name}}"/></td>
						<td><input type=text name=link value="{{link.link}}"/></td>
						<td><input type=text name=priority value="{{link.priority}}"/></td>
						<td>
							<input type="hidden" name="update" value="{{link.key}}"/>
							<input type="submit" value="Update"/>
						</td>
						</form>
						<form action="/admin2/link/" method="post">
						<td>
							<input type="hidden" name="delete" value="{{link.key}}"/>
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
