fn_template = """
               <fn-group>
			<fn>
				<p>Funding: $FUNDING$</p>
			</fn>
		</fn-group>
"""

contrib_template = """
				<contrib contrib-type="author">
					<name>
						<surname>$SURNAME$</surname>
						<given-names>$GIVEN_NAME$</given-names>
					</name>
                                        $CONTRIB_AFFS$
				</contrib>
"""


contrib_aff_template = """
					<xref ref-type="aff" rid="aff$AFFILIATION_NUMBER$"><sup>$AFFILIATION_NUMBER$</sup></xref>
"""

aff_template = """
				<aff id="aff$AFFILIATION_NUMBER$">
					<label><sup>$AFFILIATION_NUMBER$</sup></label>
					<institution>$INSTITUTION$</institution>
				</aff>
"""

ref_template = """
			<ref id="b1-Talks_6">
				<element-citation publication-type="book">
					<person-group person-group-type="author">
						<name>
							<surname>Atchison</surname>
							<given-names>D.A.</given-names>
						</name>
						<name>
							<surname>Smith</surname>
							<given-names>G.</given-names>
						</name>
					</person-group><x> </x>
					<year>2000</year>
					<source>Optics of the human eye</source>
					<publisher-loc>Oxford</publisher-loc>
					<publisher-name>Butterworth Heinemann</publisher-name>
				</element-citation>
			</ref>
"""

doi_template = '10.1167/jov.23.8.$ABSTRACT_NUMBER$'

root_template = """
<?xml version="1.0"?><!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "http://jats.nlm.nih.gov/publishing/1.0/JATS-journalpublishing1.dtd">
<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="Optica Fall Vision Meeting Abstract">
	<front>
		<journal-meta>
			<journal-id journal-id-type="hwp">jov</journal-id>
			<journal-id journal-id-type="publisher-id">JOVI</journal-id>
			<journal-title-group>
				<journal-title>Journal of Vision</journal-title>
			</journal-title-group>
			<issn pub-type="epub">1534-7362</issn>
			<publisher>
				<publisher-name>Association for Research in Vision and Ophthalmology</publisher-name>
			</publisher>
		</journal-meta>
		<article-meta>
			<article-id pub-id-type="doi">$DOI$</article-id>
			<article-id pub-id-type="manuscript">Talks_$ABSTRACT_NUMBER$</article-id>
			<article-categories>
				<subj-group subj-group-type="category">
					<subject>$SESSION$</subject>
				</subj-group>
			</article-categories>
			<title-group>
				<article-title>$SESSION$: $TITLE$</article-title>
			</title-group>
			<contrib-group>
                          $CONTRIBUTORS$
                          $AFFILIATIONS$
			</contrib-group>
			<pub-date pub-type="ppub"><month>$MONTH$</month>
				<year>$YEAR$</year>
			</pub-date>
			<pub-date pub-type="epub"><month>$MONTH$</month>
				<year>$YEAR$</year>
			</pub-date>
						<volume>$VOLUME$</volume>
						<issue>$ISSUE$</issue>
						<fpage>$FPAGE$</fpage>
						<lpage>$LPAGE$</lpage>
			<permissions>
				<license license-type="cc-by-nc-nd" xlink:href="http://creativecommons.org/licenses/by-nc-nd/4.0/">
					<license-p>This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.</license-p>
				</license>
			</permissions>
			<abstract>
				<p>$ABSTRACT$</p>
			</abstract>
		</article-meta>
	</front>
	<back>
                $FN_GROUP$
	</back>
</article>
"""
