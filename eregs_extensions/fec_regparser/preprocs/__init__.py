# vim: set encoding=utf-8
"""Set of transforms we run on notice XML to account for common inaccuracies
in the XML"""
from lxml import etree
from regparser.tree.xml_parser.preprocessors import PreProcessorBase


class RepeatedEmphasis(PreProcessorBase):
    """
    CFR 11 100 contains a number of defined terms that should be marked up as:

        <P>(d) <E T="03">[Term]</E>. <E T="03">[Term]</E> [text]</P>

    but are in fact marked up as:

        <P>(d) <E T="03">[Term]. [Term]</E> [text]</P>

    This preprocessor tries to correct them appropriately.
    """

    def transform(self, xml):
        for el in xml.xpath("//P//E[contains(., '.')]"):
            pair = [_.strip() for _ in el.text.split(".")]

            if len(pair) == 2 and pair[0] == pair[1]:
                el_parent = el.getparent()
                el_index = el_parent.index(el)
                first = etree.Element("E", attrib=el.attrib)
                first.text = "%s." % pair[0]
                first.tail = " "
                second = etree.Element("E", attrib=el.attrib)
                second.text = pair[0]
                second.tail = el.tail

                el_parent.remove(el)
                el_parent.insert(el_index, second)
                el_parent.insert(el_index, first)
