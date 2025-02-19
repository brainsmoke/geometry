
from xml.sax.saxutils import escape, quoteattr

def header(w=210, h=297):
   print("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="""+ f'"{w:d}mm"' +"""
   height="""+ f'"{h:d}mm"' +"""
   viewBox=""" + f'"0 0 {w:d} {h:d}"' + """
   version="1.1"
   id="svg8"
   inkscape:version="1.0.2 (e86c870879, 2021-01-15)"
   sodipodi:docname="drawing-4.svg">
  <sodipodi:namedview
     id="base"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="0.35"
     inkscape:cx="400"
     inkscape:cy="560"
     inkscape:document-units="mm"
     inkscape:current-layer="layer1"
     inkscape:document-rotation="0"
     showgrid="false" />
  <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1">
""")

def footer():
    print("""</g></svg>""")

def d(points):
    return 'M '+' L '.join(f"{x:f} {y:f}" for x, y in points)+'z'

def start_group(x=None, y=None):
    if None not in (x, y):
        print (f'<g transform="translate({x:f}, {y:f})">')
    else:
        print ('<g>')

def end_group():
    print('</g>')

def path(paths, color="#000000"):
    attr=quoteattr(f'fill:none;stroke:{color};stroke-width:0.264583px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1')
    print (f'<path style={attr} d="' + ' '.join( d(points) for points in paths ) + '" />')

def text(text, x=0, y=0, color="#000000"):
    attr=quoteattr(f'font-size:5pt;line-height:1.25;font-family:sans-serif;text-anchor:middle;text-align:center;fill:{color};fill-opacity:1;')
    text = escape(text)
    print(f'<text xml:space="preserve" style={attr} x="{x:f}" y="{y:f}">{text}</text>')

