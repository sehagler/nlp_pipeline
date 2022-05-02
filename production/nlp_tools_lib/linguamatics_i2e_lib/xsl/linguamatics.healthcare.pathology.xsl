<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  xmlns:ling="http://www.linguamatics.com/2008/highlight" xmlns:xlink="http://www.w3.org/1999/xlink" exclude-result-prefixes="ling xlink">
<xsl:output method='html' version='1.0' encoding='UTF-8' doctype-system="http://www.w3.org/TR/html4/strict.dtd" doctype-public="-//W3C//DTD HTML 4.01//EN" indent='yes'/>

<xsl:template match="/">
	<html>
		<head>
			<title>Healthcare Pathology Report</title>
			<style type="text/css">
				.default_regionname { 
					font-size:0.85em;
					color:#336699;
					margin:0.4em 0;
					list-style:none outside none;
					text-decoration:none;
				}
				
				div.section_header { 
					margin-top: 10px;
					font-weight: bold; 
				}
				div.boxed { 
					border-style: solid;
					border-width: thin;
					border-color: #336699;
				}
				div.floating { 
					text-align: right;
					font-style: italic;
					color: #336699;
				}
				div.boxed + div.boxed {
					border-top: none;
				}
			</style>
			<script type="text/javascript">
				function firefoxFixAnchor()
				{
					if (location.href.indexOf('#') &gt; -1) {
					location.href+='';}
				}
			</script>
		</head>
		<body onLoad="firefoxFixAnchor();">
			<xsl:apply-templates/>
		</body>
	</html>
</xsl:template>

<!-- Classes -->
<!-- Regions -->
<xsl:template match="*">
	<xsl:variable name="margin" select="100 div (count(ancestor::node())+1)" />
	<xsl:variable name="margin_text" select="concat('margin-left:',$margin,'px')"/>
	<xsl:element name="div">
		<xsl:attribute name="style">
			<xsl:value-of select="$margin_text" />
		</xsl:attribute>
		<span class="default_regionname"> <xsl:value-of select="name()" />	<xsl:text>:&#160;</xsl:text></span>
		<xsl:apply-templates/>
	</xsl:element>
</xsl:template>

<xsl:template match="ling:linkage|report|rpt_text|section|section_body|First|Last">
	<xsl:apply-templates/>
</xsl:template>

<xsl:template match="specimen">
	<div class="boxed">
		<xsl:apply-templates/>
		<xsl:apply-templates select="@id"/>
	</div>
</xsl:template>

<xsl:template match="specimen/@id">
	<div class="floating">
		<xsl:text>Specimen(s): </xsl:text>
		<xsl:value-of select="."/>
	</div>
</xsl:template>


<xsl:template match="section_title">
	<div class="section_header">
		<xsl:apply-templates/>
	</div>
</xsl:template>

<xsl:template match="br|p">
	<xsl:copy>
		<xsl:apply-templates/>
	</xsl:copy>
</xsl:template>


<!-- Apply Linguamatics highlighting -->
<xsl:template match="ling:highlight">
	<a>
		<xsl:attribute name="href">#<xsl:value-of select="@next" /></xsl:attribute>
		<xsl:attribute name="name"><xsl:value-of select="@this" /></xsl:attribute>
		<span style="COLOR: black; BACKGROUND-COLOR: {@color};">
			<xsl:apply-templates/>
		</span>
	</a>
</xsl:template>
  
</xsl:stylesheet>
