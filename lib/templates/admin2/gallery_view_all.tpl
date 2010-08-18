<div class="gallery_view_all">
	<div>
		<form class="form" action="/admin2/gallery/?create=1" method="post">
	        <h2>Create New Gallery</h2>
	        <div class="row">
	            <label class="col1"><span class="required">* </span>Name:</label>
	            <span class="col2"><input type="text" name="name"/></span>
	        </div>
	        <div class="row">
	            <label class="col1"><span class="required">* </span>Description:</label>
	            <span class="col2"><textarea name="desc"></textarea></span>
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
						Galleries
					</th>
				</tr>
				<tr>
					<th width="25%">Name</th>
					<th width="40%">Description</th>
					<th width="15%" colspan="3">Action</th>
				</tr>
			</thead>
			<tbody>
				{% if gals %}
					{% for gal in gals %}
					<tr>
						<form action="/admin2/gallery/" method="post">
						<td>{{gal.name}}</td>
						<td><textarea name="desc">{{gal.desc}}</textarea></td>
						<td>
							<input type="hidden" name="update" value="{{gal.key}}"/>
							<input type="submit" value="Update"/>
						</td>
						</form>
						<td>
							<form action="/admin2/gallery/" method="get">
								<input type="hidden" name="view" value="{{gal.key}}"/>
								<input type="submit" value="View"/>
							</form>
						</td>
						<td>
							<form action="/admin2/gallery/" method="post">
								<input type="hidden" name="delete" value="{{gal.key}}"/>
								<input type="submit" name="delete" value="Delete"/>
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
