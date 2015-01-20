import cherrypy
import random
import string
from datetime import timedelta

from trashmail.models import Trashmail

class Root(object):

    @cherrypy.expose
    def index(self):
        return """<!DOCTYPE html>
<html lang="fr">
<head>
  <link rel="stylesheet" type="text/css" href="/static/dhtmlxslider.css"></link>
  <script type="text/javascript" src="/static/dhtmlxslider.js"></script>
  <script type="text/javascript">
    var slider1;
    function doOnLoad() {
      slider1 = new dhtmlXSlider({
        parent: "periodSlider",
        linkTo: "period",
        size:   260,
        value:  7,
        min:    1,
        max:    90
      });
    }
    function doOnUnload() {
      if (slider1 != null) {
        slider1.unload();
        slider1 = null;
      }
    }
  </script>
</head>
<body onload="doOnLoad();" onunload="doOnUnload();">
  <form method="post" action="generate">
    <label for="recipient">Email réel: </label>
    <input type="text" name="recipient" />
    <label for="period">
    <br/>
    <div style="position:relative;margin-bottom:10px;">
      <div width="600px" height="283px" style="width:600px;height:280px:position:absolute;top:0px;left:0px;">
        <input type="text" id="period" name="period" style="width:37px;position:absolute;top:0px;left:0px;font-size:12px;">
        <div id="periodSlider" style="position:absolute;top:2px;left:51px;"></div>
      </div>
    </div>
    <br style="margin-top:1em;"/>
    <button type="submit">Give it now!</button>
  </form>
</body>
</html>"""

    @cherrypy.expose
    def generate(self, recipient, period):
        val = Trashmail(fake_recipient=''.join(random.sample(string.ascii_lowercase, 4)),
                        recipient=recipient,
                        period=timedelta(days=int(period)))
        cherrypy.tools.db.session.add(val)
        cherrypy.tools.db.session.commit()
        return "{}@{}".format(val.fake_recipient, cherrypy.request.app.config['/']['mailhost'])
