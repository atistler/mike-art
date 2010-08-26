<div id="gallery" style="margin:0 auto; height:575px; width:800px;"></div>
<script language="javascript" type="text/javascript">
    var so = new SWFObject("/swf/flashgallery.swf", "gallery", "800px", "575px", "8"); // Location of SWF file. You can change gallery width and height here (using pixels or percents).
    so.addParam("quality", "high");
    so.addParam("allowFullScreen", "true");
    so.addParam("wmode", "transparent");
    so.addVariable("content_path",""); // Location of a folder with JPG and PNG files (relative to php script).
    so.addVariable("color_path","/xml/default.xml"); // Location of XML file with settings.
    so.addVariable("script_path","/{{gal_name}}/list"); // Location of PHP script.
    so.write("gallery");
</script>
