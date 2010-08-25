<script language="javascript" type="text/javascript">
    var so = new SWFObject("/swf/flashgallery.swf", "gallery", "800", "600", "8"); // Location of SWF file. You can change gallery width and height here (using pixels or percents).
    so.addParam("quality", "high");
    so.addParam("allowFullScreen", "true");
    so.addParam("wmode", "transparent");
    so.addVariable("content_path","/image/"); // Location of a folder with JPG and PNG files (relative to php script).
    so.addVariable("color_path","/swf/default.xml"); // Location of XML file with settings.
    so.addVariable("script_path","/Paintings/list"); // Location of PHP script.
    so.write("gallery");
</script>