import copy
import tempfile
import unittest
from webapp.app import analyze,normalize,decide,EXAMPLE,Workspace

class PolicyTests(unittest.TestCase):
    def test_reference_assertions_and_default_deny(self):
        p=analyze(EXAMPLE);self.assertEqual(p['failed'],0);self.assertEqual(p['passed'],3)
        self.assertEqual(decide([],{'source':'a','destination':'b','protocol':'tcp','port':22})['action'],'deny')
    def test_first_match_wins_and_shadowed_rule_is_reported(self):
        p=copy.deepcopy(EXAMPLE);p['rules']=[{'id':'deny-all','source':'any','destination':'any','protocol':'any','port':'any','action':'deny'},*p['rules']]
        r=analyze(p);self.assertEqual(r['tests'][1]['action'],'deny');self.assertEqual(len([w for w in r['warnings'] if w['type']=='shadowed']),4)
    def test_broad_management_exposure_is_flagged(self):
        p=copy.deepcopy(EXAMPLE);p['rules'].insert(0,{'id':'wide','source':'any','destination':'any','protocol':'any','port':'any','action':'allow'})
        types={w['type'] for w in analyze(p)['warnings']};self.assertIn('broad-allow',types);self.assertIn('management-exposure',types)
    def test_tcp_and_udp_are_distinct(self):
        p=normalize(EXAMPLE);self.assertEqual(decide(p['rules'],{'source':'internet','destination':'dmz','protocol':'udp','port':443})['action'],'deny')
    def test_rejects_unknown_zone_duplicate_id_and_invalid_port(self):
        for mutation in ['zone','id','port']:
            p=copy.deepcopy(EXAMPLE)
            if mutation=='zone':p['rules'][0]['source']='missing'
            if mutation=='id':p['rules'][1]['id']=p['rules'][0]['id']
            if mutation=='port':p['rules'][0]['port']=70000
            with self.assertRaises(ValueError):analyze(p)
    def test_saved_policy_survives_restart(self):
        with tempfile.TemporaryDirectory() as d:
            p=Workspace(d).action({'action':'analyze','policy':EXAMPLE})
            self.assertEqual(Workspace(d).state()['analyses'][0]['id'],p['id'])
