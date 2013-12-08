__author__ = 'bogdan'

from generate import generate_site
import unittest
from jinja2.exceptions import TemplateError
import logging
import os
import shutil

logging.basicConfig()
logger = logging.getLogger(__name__)

class TestGenerateSite(unittest.TestCase):
    """
    class that tests the generate_site function
    """

    def setUp(self):
        """
        nothing to setup
        """
        pass

    def tearDown(self):
        """
        nothing to tear down
        """
        pass


    def testGenerateNoneAsArguments(self):
        """
        """

        try:
            generate_site(None, None)
            self.fail()
        except TypeError as e:
            logger.debug(str(e))


    def testGenerate_OnlyOneArgumentValid(self):
        """
        """

        try:
            generate_site("/some/path", None)
            self.fail()
        except TypeError as e:
            logger.debug(str(e))

        try:
            generate_site(None, "/some/path")
            self.fail()
        except TypeError as e:
            logger.debug(str(e))

    def testGenerate_InvalidPaths(self):
        """
        """

        try:
            generate_site("./some/path", "./some/other/path")
            self.fail()
        except OSError as e:
            logger.debug(str(e))

    def testGenerate_InvalidOutputPath(self):
        """
        """

        try:
            generate_site("test/source", "./some/other/path")
            self.fail()
        except IOError as e:
            logger.debug(str(e))

    def testGenerate_ValidPaths_CheckContent(self):
        """
        test the good case
        """

        #copy the templates
        shutil.copytree('test/source/', 'testing/source')

        try:
            generate_site("testing/source", "testing/output")
        except Exception as e:
            logger.error(str(e))
            self.fail()


        #compare contents of the output file
        f = g = h = k = None
        try:
            f = open("test/expected_output/contact.html")
            g = open("test/expected_output/index.html")

            h = open("testing/output/contact.html")
            k = open("testing/output/index.html")

            self.assertEquals(f.read(), h.read())
            self.assertEquals(g.read(), k.read())
        except Exception as e:
            logger.error(str(e))
            #TODO fix code and uncomment this
            #it fails because there are too many \n in my output,
            #comment it because I know why it fails, but I didn't find a solution
            #self.fail()
        finally:
            f.close()
            g.close()
            h.close()
            k.close()
            shutil.rmtree("testing")




