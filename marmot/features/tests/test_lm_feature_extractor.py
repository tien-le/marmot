#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import os
from marmot.features.lm_feature_extractor import LMFeatureExtractor


# test a class which extracts source and target token count features, and the source/target token count ratio
class TokenCountFeatureExtractorTests(unittest.TestCase):

    def setUp(self):
        module_path = os.path.dirname(os.path.realpath(__file__))
        self.module_path = module_path
        self.lm3Extractor = LMFeatureExtractor(os.path.join(module_path, 'test_data/training.txt'))
        self.lm5Extractor = LMFeatureExtractor(os.path.join(module_path, 'test_data/training.txt'), order=5)


    def test_get_features(self):
        # { 'token': <token>, index: <idx>, 'source': [<source toks>]', 'target': [<target toks>], 'tag': <tag>}
        (left3, right3) = self.lm3Extractor.get_features( {'token':'a', 'index':2, 'source':[u'c',u'\'',u'est',u'un',u'garçon'], 'target':[u'this',u'is',u'a',u'boy',u'.'], 'tag':'G'})
        (left5, right5) = self.lm3Extractor.get_features( {'token':'a', 'index':2, 'source':[u'c',u'\'',u'est',u'un',u'garçon'], 'target':[u'this',u'is',u'a',u'boy',u'.'], 'tag':'G'})
        # TODO: this is not a test
        print left3, right3, left5, right5
#        self.assertEqual(len(vector), 3)
        #self.assertEqual(vector[0], 5.0)
        #self.assertEqual(vector[1], 5.0)
        #self.assertEqual(vector[2], 1.0)


if __name__ == '__main__':
    unittest.main()