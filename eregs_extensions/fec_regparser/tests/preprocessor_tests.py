# vim: set encoding=utf-8
from unittest import TestCase

from tests.xml_builder import XMLBuilderMixin
from fec_regparser.preprocs import RepeatedEmphasis


class RepeatedEmphasisTests(XMLBuilderMixin, TestCase):
    """
    We want to change e.g.:

        <P>(d) <E T="03">[Term]. [Term]</E> [text]</P>

    to:

        <P>(d) <E T="03">[Term]</E>. <E T="03">[Term]</E> [text]</P>
    """
    def test_repeated_emphasis_transform(self):
        runoff = u"%s %s %s" % (u'(d) <E T="03">Runoff election. Runoff',
                                u'election</E> means the election which meets',
                                u'either of the following conditions:')
        with self.tree.builder("PART") as part:
            with part.REGTEXT(ID="RT1") as regtext:
                with regtext.SECTION() as section:
                    section.SECTNO(u"§ 100.2")
                    section.SUBJECT("Election (52 U.S.C. 30101(1)).")
                    section.P(_xml=runoff)
        xml = self.tree.render_xml()
        RepeatedEmphasis().transform(xml)
        e_elements = xml.xpath("//E")

        self.assertEquals(len(e_elements), 2)
        self.assertEquals(e_elements[0].text, "Runoff election.")
        self.assertEquals(e_elements[0].tail, " ")
        self.assertEquals(e_elements[0].attrib, {"T": "03"})
        self.assertEquals(e_elements[1].text, "Runoff election")
        tail = u"%s %s" % (u" means the election which meets either",
                           u"of the following conditions:")
        self.assertEquals(e_elements[1].tail, tail)
        self.assertEquals(e_elements[1].attrib, {"T": "03"})

    def test_repeated_emphasis_transform_not_duplicate(self):
        """
        This case should not trigger the preprocessor.
        """
        runoff = u"%s %s %s" % (u'(d) <E T="03">Runoff election. Runoff',
                                u'elector</E> means the election which meets',
                                u'either of the following conditions:')
        with self.tree.builder("PART") as part:
            with part.REGTEXT(ID="RT1") as regtext:
                with regtext.SECTION() as section:
                    section.SECTNO(u"§ 100.2")
                    section.SUBJECT("Election (52 U.S.C. 30101(1)).")
                    section.P(_xml=runoff)
        xml = self.tree.render_xml()
        RepeatedEmphasis().transform(xml)
        e_elements = xml.xpath("//E")

        self.assertEquals(len(e_elements), 1)
        self.assertEquals(e_elements[0].text,
                          "Runoff election. Runoff elector")
        tail = u"%s %s" % (u" means the election which meets either",
                           u"of the following conditions:")
        self.assertEquals(e_elements[0].tail, tail)

    def test_repeated_emphasis_transform_no_period(self):
        """
        This case should not trigger the preprocessor.
        """
        runoff = u"%s %s %s" % (u'(d) <E T="03">Runoff election Runoff',
                                u'election</E> means the election which meets',
                                u'either of the following conditions:')
        with self.tree.builder("PART") as part:
            with part.REGTEXT(ID="RT1") as regtext:
                with regtext.SECTION() as section:
                    section.SECTNO(u"§ 100.2")
                    section.SUBJECT("Election (52 U.S.C. 30101(1)).")
                    section.P(_xml=runoff)
        xml = self.tree.render_xml()
        RepeatedEmphasis().transform(xml)
        e_elements = xml.xpath("//E")

        self.assertEquals(len(e_elements), 1)
        self.assertEquals(e_elements[0].text,
                          "Runoff election Runoff election")
        tail = u"%s %s" % (u" means the election which meets either",
                           u"of the following conditions:")
        self.assertEquals(e_elements[0].tail, tail)
