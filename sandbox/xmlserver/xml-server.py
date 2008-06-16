#!/usr/bin/env python
import urllib
import cgi
import traceback
import StringIO
import BaseHTTPServer
import SimpleHTTPServer
from mwlib import mwapidb
from mwlib import xhtmlwriter
from mwlib import advtree

default_baseurl = "en.wikipedia.org/w"
default_debug = 1
default_imgwidth = 200
imagesrcresolver = "/imageresolver/IMAGENAME"
version = "0.1"

class XMLHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    mwlib.xml-server version %s using xhtmlwriter.py version (%s)
    
    This server offers three services:
    /mwxml/         : returns a XML represnentaion of the parse tree 
    /mwxhtml/       : returns MediaWiki documents as XHTML1.0 transitional
    /imageresolver/ : resolves imagenames to full urls

    Note this service relies on MediaWiki API http://en.wikipedia.org/w/api.php
    So only Mediawikis with an approriate version are supported.

    usage /mwxml/ _____________________________________________________:

    /mwxml/<wiki_base_url>/<article><?option_arg=option_value>
    e.g.
    /mwxml/www.mediawiki.org/w/API
    
    wiki_base_url defaults to %s
    so one can also use /mwxml/Article to access Article from the above site

    usage /mwxhtml/ _____________________________________________________:

    /mwxhtml/<wiki_base_url>/<article><?option_arg=option_value>
    e.g.
    /mwxhtml/www.mediawiki.org/w/API
    
    wiki_base_url defaults to %s
    so one can also use /mwxhtml/Article to access Article from the above site
    
    options (query args):

    debug
    whether verbose debug info is included as XML-comments
    0 or 1, defaults to %d
    
    imageresolver
    img src tags can be set to a redirector service, in order to get them 
    resolved and displayed in browsers.
    value can be any  string, in which every occurence of IMAGENAME is 
    substituted by the image name (e.g. 'Picture1.jpg).
    This defaults to '%s'

    
    usage /imageresolver/ ___________________________________________:   
    
    /imageresolver/<IMAGENAME><?baseurl=url>
    
    baseurl is used to retrieve images

    baseurl defaults to %s
    imgwidth defaults to %d
    
    """ 

    documentation = __doc__ % (version, xhtmlwriter.version, default_baseurl, 
                               default_baseurl, 
                               default_debug, imagesrcresolver, default_baseurl, 
                               default_imgwidth)
       


    def do_GET(self):
        path, query = urllib.splitquery(self.path)
        path = [urllib.unquote_plus(x) for x in path.split("/")]
        query = cgi.parse_qs(query or "")
        print path, query
        app = path[1]
        args = path[2:]
        print args, query
        if app in ("mwxml", "mwxhtml"):
            self._dosafe(self._servXML, args, query, app)
        elif app == "imageresolver":
            self._dosafe(self._resolveImage, args, query, app)
        else:
            self._doc()
        


    def _dosafe(self, method, query, args, app):
        try:
            method(query, args, app)
        except Exception, e:
            s = StringIO.StringIO()
            traceback.print_exc(file=s)
            self._doc(error = s.getvalue())


    def _doc(self, error=""):
        if error:
            response = "An error occurred:\n\n%s\n\n%s" %( error, self.documentation)
            self.send_response(500)
        else:
            self.send_response(200)
            response = self.documentation
        
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


    def _servXML(self, args, query, dialect="mwxml"):
        if not len(args):
            self._doc(error="require articlename")
            return
        unknown = [k for k in query if k not in ("debug", "imageresolver")]
        if unknown:
            return self._doc(error="unknown option %r" % unknown)
        title = args.pop()
        base_url = "http://%s/" % ("/".join(args) or default_baseurl)
        debug = bool(query.setdefault("debug", [default_debug])[0])

        language = "en" # FIXME
        namespace="en.wikipedia.org" # FIXME

        print "_servXML", title, base_url, debug

        db = mwapidb.WikiDB(base_url, license=None)
        db.print_template = None # deactivate print template lookups
        tree = db.getParsedArticle(title, revision=None)
        advtree.buildAdvancedTree(tree)
        if dialect == "mwxhtml":
            dbw = xhtmlwriter.MWXHTMLWriter(language=language, namespace=namespace, 
                                            imagesrcresolver=imagesrcresolver,
                                            debug=debug)
        else:
            assert dialect == "mwxml"
            dbw = xhtmlwriter.MWXMLWriter() # another XML-writer implementation

        dbw.write(tree)
        if debug:
            dbw.writeparsetree(tree)

        response = dbw.asstring()
        
        self.send_response(200)
        self.send_header("Content-type", "text/xml")
        self.send_header("Content-length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)
        
        # shut down the connection
        self.wfile.flush()
        

    def _resolveImage(self, args, query, app=None):
        if not len(args):
            self._doc(error="require imagename")
            return
        unknown = [k for k in query if k not in ("baseurl", "imgwidth")]
        if unknown:
            return self._doc(error="unknown option %r" % unknown)
        title = args.pop()
        base_url = "http://" + query.setdefault("baseurl", [default_baseurl])[0] 
        imgwidth = int(query.setdefault("imgwidth", [default_imgwidth])[0] )

        print "_resolveImage", title, base_url, imgwidth

        db = mwapidb.ImageDB(base_url)
        url = db.getURL(title.decode("utf8"), size=imgwidth)
        if not url:
            self.send_response(404)
            self.end_headers()
        else:
            self.send_response(301)
            self.send_header("Location", url)
            self.end_headers()






def run(port=8000):
    server_address = ('', port)
    httpd = BaseHTTPServer.HTTPServer(server_address, XMLHandler)
    print "listening on port", port
    httpd.serve_forever()


if __name__ == "__main__":
    run()
