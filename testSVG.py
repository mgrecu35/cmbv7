import urllib
import urllib2

def latex2svg(latexcode):
    """
    Turn LaTeX string to an SVG formatted string using the online SVGKit
    found at: http://svgkit.sourceforge.net/tests/latex_tests.html
    """
    txdata = urllib.urlencode({"latex": latexcode})
    url = "http://svgkit.sourceforge.net/cgi-bin/latex2svg.py"
    req = urllib2.Request(url, txdata)
    return urllib2.urlopen(req).read()

print(latex2svg("2+2=4"))
print(latex2svg("\\frac{1}{2\\pi}"))
