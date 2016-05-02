# vim: set encoding=utf-8
from unittest import TestCase

from fec_regparser.preprocs import RepeatedEmphasis
from regparser.test_utils.xml_builder import XMLBuilder


class RepeatedEmphasisTests(TestCase):
    """
    We want to change e.g.:

        <P>(d) <E T="03">[Term]. [Term]</E> [text]</P>

    to:

        <P>(d) <E T="03">[Term]</E>. <E T="03">[Term]</E> [text]</P>
    """
    @staticmethod
    def _emphasis_from(paragraph_text):
        """Setup for several tests"""
        with XMLBuilder("PART") as ctx:
            with ctx.REGTEXT(ID="RT1"):
                with ctx.SECTION():
                    ctx.SECTNO(u"§ 100.2")
                    ctx.SUBJECT("Election (52 U.S.C. 30101(1)).")
                    ctx.child_from_string('<P>{}</P>'.format(paragraph_text))
        xml = ctx.xml
        RepeatedEmphasis().transform(xml)
        return xml.xpath("//E")

    def test_repeated_emphasis_transform(self):
        runoff = u"%s %s %s" % (u'(d) <E T="03">Runoff election. Runoff',
                                u'election</E> means the election which meets',
                                u'either of the following conditions:')
        e_elements = self._emphasis_from(runoff)

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
        e_elements = self._emphasis_from(runoff)

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
        e_elements = self._emphasis_from(runoff)

        self.assertEquals(len(e_elements), 1)
        self.assertEquals(e_elements[0].text,
                          "Runoff election Runoff election")
        tail = u"%s %s" % (u" means the election which meets either",
                           u"of the following conditions:")
        self.assertEquals(e_elements[0].tail, tail)
