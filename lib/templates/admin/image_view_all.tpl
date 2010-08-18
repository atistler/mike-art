<div class="gallery_view">
    <div>
        <form class="form" action="/admin/image/?create=1" method="post" enctype="multipart/form-data" autocomplete=off>
            <h2>Create New Image</h2>
            <div class="row">
                <label class="col1"><span class="required">* </span>Name:</label>
                <span class="col2"><input type="text" name="name"/></span>
            </div>
            <div class="row">
                <label class="col1"><span class="required">* </span>Description:</label>
                <span class="col2">
                    <textarea name="desc"></textarea>
                </span>
            </div>
            <div class="row">
                <label class="col1"><span class="required">* </span>Priority:</label>
                <span class="col2"><input size=4 maxlength=4 type="text" name="priority" value="0"/></span>
            </div>
            <div class="row">
                <label class="col1"><span class="required">* </span>File:</label>
                <span class="col2"><input type="file" name="img"/></span>
            </div>
            <div class="row">
                <label class="col1"><span class="required">* </span>Gallery:</label>
                <span class="col2">
                    <select name="gallery">
			{% if gals %}
			{% for gal in gals %}
                        <option value="{{gal.key}}">{{gal.name}}</option>
			{% endfor %}
			{% endif %}
                    </select>
                </span>
            </div>
            <div class="row">
                <span class="col1"><input type="submit" name="create" value="Create"/></span>
            </div>
        </form>
    </div>
    <div>
        <table class="edit" cellspacing="0" cellpadding="3">
            <thead>
                <tr>
                    <th colspan="8">
                        Images 
                    </th>
                </tr>
                <tr>
                    <th width="10%">Name</th>
                    <th width="10%">Description</th>
                    <th width="10%">Priority</th>
                    <th width="20%">Thumbnail</th>
                    <th width="15%">Content-Type</th>	
                    <th width="15%">Gallery</th>
                    <th width="10%" colspan="2">Action</th>
                </tr>
            </thead>
            <tbody>
                {% if imgs %}
                {% for img in imgs %}
            <form action="/admin/image/" method="post">
                <tr>
                <input type="hidden" name="id" value="{{img.key}}"/>
                <td><input type="text" name="name" value="{{img.name}}"/></td>
                <td>
                    <textarea name="desc">{{img.desc}}</textarea>
                </td>
                <td><input size=4 maxlength=4 type="text" name="priority" value="{{img.priority}}"/></td>
                <td><img src="/image/?render_thumb={{img.key}}"/></td>
                <td>{{img.contenttype}}</td>
                <td>
                    <select name="gallery">
			{% for gal in gals %}
			{% ifequal gal.key img.gallery.key %}
                        <option value="{{gal.key}}" selected>{{gal.name}}</option>
			{% else %}
                        <option value="{{gal.key}}">{{gal.name}}</option>
			{% endifequal %}
			{% endfor %}
                    </select>
                </td>
                <td>
                    <input type="submit" name="update" value="Update"/>
                </td>
                <td>
                    <input type="submit" name="delete" value="Delete"/>
                </td>
                </tr>
            </form>
            {% endfor %}
            {% else %}
            <tr>
                <td colspan="7" style="text-align:center">None</td>
            </tr>
            {% endif %}
            </tbody>
        </table>
    </div>
</div>
