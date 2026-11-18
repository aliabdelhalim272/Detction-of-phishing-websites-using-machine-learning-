import unittest
from unittest.mock import patch
import pandas as pd
from src.features import FEATURE_NAMES, extract_url_features, hostname_group
from src.data.preparation import prepare_rows


class PreparationTests(unittest.TestCase):
    def test_https_is_scheme_not_substring(self):
        with patch('socket.getaddrinfo',side_effect=AssertionError('No network allowed')):
            f=extract_url_features('http://example.com/?next=https://other.com')
        self.assertEqual(f['has_https'],0)
        self.assertEqual(extract_url_features('HTTPS://example.com')['has_https'],1)
        self.assertEqual(tuple(f),FEATURE_NAMES)

    def test_ports_userinfo_unicode_ipv6(self):
        self.assertEqual(hostname_group('https://user@Example.com:8443/a'),'example.com')
        f=extract_url_features('http://[2001:db8::1]:8080/a')
        self.assertEqual((f['hostname_is_ip'],f['has_explicit_port']),(1,1))
        self.assertEqual(hostname_group('https://örnek.com'),'xn--rnek-4qa.com')
        self.assertEqual(extract_url_features('https://example.com/?a=%20&&b=1')['count_query_parameters'],2)

    def test_reject_invalid(self):
        for value in ['',None,'example.com','file:///a','https://a:','https://a:0',
                      'https://a:99999','https://bad_host.com','https://a\n.com','https://a\\b.com']:
            with self.subTest(value=value),self.assertRaises(ValueError): extract_url_features(value)

    def frames(self):
        raw=pd.DataFrame({'URL':['http://a.com','http://a.com','https://b.com','http://c.com','bad-url'],
                          'label':[0,0,1,0,1],'old_measurement':[12,99,13,14,1]})
        manifest=pd.DataFrame({'source_row':range(5),'partition':['train','train','validation','test','test']})
        return raw,manifest

    def test_lineage_quarantine_and_parity(self):
        raw,m=self.frames();before=raw.copy(deep=True)
        result=prepare_rows(raw,m)
        pd.testing.assert_frame_equal(raw,before)
        self.assertEqual(result['X'].index.tolist(),[0,2,3])
        self.assertEqual(result['y'].is_phishing.tolist(),[1,0,1])
        self.assertEqual(result['mapping'].loc[1,'representative_source_row'],0)
        self.assertEqual(result['quarantine'].source_row.tolist(),[4])
        self.assertEqual(result['metadata'].partition.tolist(),['train','validation','test'])
        for row in result['X'].index:
            self.assertEqual(result['X'].loc[row].to_dict(),extract_url_features(raw.loc[row,'URL']))

    def test_conflicts_stop(self):
        raw,m=self.frames();raw.loc[1,'label']=1
        with self.assertRaisesRegex(ValueError,'Conflicting targets'):prepare_rows(raw,m)

    def test_url_and_host_overlap_stop(self):
        raw,m=self.frames();m.loc[1,'partition']='validation'
        with self.assertRaisesRegex(ValueError,'URL crosses'):prepare_rows(raw,m)
        raw,m=self.frames();raw.loc[2,'URL']='https://a.com/different'
        with self.assertRaisesRegex(ValueError,'hostname crosses'):prepare_rows(raw,m)


if __name__=='__main__':unittest.main()
