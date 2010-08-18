<div class="gallery_view">
    <div>
        <form class="form" action="/admin/image/?create=1" method="post" enctype="multipart/form-data" autocomplete=off>
            <h2>Create Image in Gallery</h2>
            <input type="hidden" name="gallery" value="{{gal.key}}"/>
            <div class="row">
                <label class="col1"><span class="required">* </span>Name:</label>
                <span class="col2"><input type="text" name="name"/></span>
            </div>
            <div class="row">
                <label class="col1"><span class="required">* </span>Description:</label>
                <span class="col2"><textarea name="desc"></textarea></span>
            </div>
            <div class="row">
                <label class="col1"><span class="required">* </span>Priority:</label>
                <span class="col2"><input type="text" name="priority" value="0"/></span>
            </div>
            <div class="row">
                <label class="col1"><span class="required">* </span>File:</label>
                <span class="col2"><input type="file" name="img"/></span>
            </div>
            <div class="row">
                <span class="col1"><input type="submit" value="Create"/></span>
            </div>
        </form>
    </div>
    <div>
        <table class="edit" cellspacing="0" cellpadding="3">
            <thead>
                <tr>
                    <th colspan="2">
						Gallery Summary
                    </th>
                <tr>
            </thead>
            <tbody>
                <tr>
                    <td>Key</td>
                    <td>{{gal.key}}</td>
                </tr>
                <tr>
                    <td>Name</td>
                    <td>{{gal.name}}</td>
                </tr>
                <tr>
                    <td>Description</td>
                    <td>{{gal.desc}}</td>
                </tr>
                <tr>
                    <td># of Images</td>
                    <td>{{imgs_count}}</td>
                </tr>
            </tbody>
        </table>
    </div>
    <div>
        <table class="edit" cellspacing="0" cellpadding="3">
            <thead>
                <tr>
                    <th colspan="7">
	                   	Gallery Images 
                    </th>
                </tr>
                <tr>
                    <th width="15%">Name</th>
                    <th width="15%">Description</th>
                    <th width="15%">Priority</th>
                    <th width="20%">Thumbnail</th>
                    <th width="20%">Content-Type</th>	
                    <th width="10%" colspan="2">Action</th>
                </tr>
            </thead>
            <tbody>
                {% if imgs %}
                {% for img in imgs %}
                <tr>
            <form name="image_edit" id="image_edit" action="/admin/image/" method="post">
                <input type="hidden" name="gallery" value="{{gal.key}}"/>
                <input type="hidden" name="id" value="{{img.key}}"/>
                <td><input type="text" name="name" value="{{img.name}}"/></td>
                <td>
                    <textarea name="desc">{{img.desc}}</textarea>
                </td>
                <td><input size=4 maxlength=4 type="text" name="priority" value="{{img.priority}}"/></td>
                <td><img src="/image/?render_thumb={{img.key}}"/></td>
                <td>{{img.contenttype}}</td>
                <td>
                    <input type="submit" name="update" value="Update"/>
                </td>
                <td>
                    <input type="submit" name="delete" value="Delete"/>
                </td>
                <td>
                    <input type="submit" name="migrate" value="Migrate"/>
                </td>
            </form>
            </tr>
            {% endfor %}
            {% else %}
            <tr>
                <td colspan="6" style="text-align:center">None</td>
            </tr>
            {% endif %}
            </tbody>
        </table>
    </div>
</div>



