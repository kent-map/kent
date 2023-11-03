<a href="https://www.juncture-digital.org"><img src="https://juncture-digital.github.io/juncture/static/images/ve-button.png"></a>

<param ve-config title="Image usage examples" layout="vertical">

# Using an image from Wikimedia Commons

In this example a Wikimedia Commons image is used to dynamically create an IIIF image using properties defined in the ve-image tag.  In this use the `url` attribute in the ve-image tag should reference the highest-resolution version of the image available from the Wikimedia Commons site.  This is usually found in the `Original file` link.  In addition to the `url` attribute, the attributes `label`, `description`, `attribution`, and `license` may also be specified.  At a minimum the `label` attribute should be defined.
<param ve-image 
    url="https://upload.wikimedia.org/wikipedia/commons/0/06/Lilac-breasted_roller_%28Coracias_caudatus_caudatus%29_Botswana.jpg" 
    label="Lilac-breasted roller"
    description="Lilac-breasted roller (Coracias caudatus caudatus), Chobe National Park, Botswana"
    license="CC BY-SA"
    attribution="Charles J. Sharp (https://www.wikidata.org/wiki/Q54800218)">

In this example a Wikimedia Commons image is again used to dynamically create an IIIF image.  In this example the `manifest` attribute is defined in the ve-image tag.  No other attributes are needed as the Juncture IIIF service is able to automatically retrieve IIIF property values from the Wikimedia Commons web site.  If a custom caption is desired an optional `title` attribute can be used to override the default label in the generated IIIF Manifest.
<param ve-image manifest="https://iiif.juncture-digital.org/wc:Lilac-breasted_roller_(Coracias_caudatus_caudatus)_Botswana.jpg/manifest.json">

In this example the `title` attribute is used to override the auto-generated label attribute in the IIIF manifest.
<param ve-image manifest="https://iiif.juncture-digital.org/wc:Lilac-breasted_roller_(Coracias_caudatus_caudatus)_Botswana.jpg/manifest.json" title="Lilac-breasted roller">

In this example the shortform version of the manifest URL is used.
<param ve-image manifest="wc:Lilac-breasted_roller_(Coracias_caudatus_caudatus)_Botswana.jpg">

# Using a self-hosted image in Github

In this example an image hosted in a Github repository is used to create an IIIF version of the image used in image viewer.  The `url` attribute in the ve-image tag references the file using the Github `raw.githubusercontent.com` URL syntax.  Other IIIF properties are also defined using ve-image attributes.  Recognized attributes are `label`, `description`, `attribution`, and `license`.
<param ve-image 
    url="https://raw.githubusercontent.com/kent-map/images/main/dickens/Hassam.jpg" 
    label="Childe Hassam, Bleak House, Broadstairs, 1889" 
    attribution="Collection of the Canton Museum of Art, Purchased by the Canton Museum of Art, 2017.83">

In this example an image hosted in a Github repository is used to create an IIIF version of the image used in image viewer.
<param ve-image manifest="https://iiif.juncture-digital.org/gh:kent-map/images/dickens/Hassam.jpg/manifest.json">

In this example an image hosted in a Github repository is referenced using a shorthand manifest URL.
<param ve-image manifest="gh:kent-map/images/dickens/Hassam.jpg">