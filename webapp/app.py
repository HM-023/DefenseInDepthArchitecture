"""Offline, first-match zone policy reasoning. Does not send network traffic."""
import uuid
from webapp.runtime import Store, integer, now, text, serve
EXAMPLE={'name':'Segmented enterprise policy','zones':['internet','dmz','users','management','logging'],
'rules':[{'id':'P-01','source':'internet','destination':'dmz','protocol':'tcp','port':443,'action':'allow'},
 {'id':'P-02','source':'users','destination':'dmz','protocol':'tcp','port':443,'action':'allow'},
 {'id':'P-03','source':'management','destination':'any','protocol':'tcp','port':22,'action':'allow'},
 {'id':'P-04','source':'any','destination':'logging','protocol':'udp','port':514,'action':'allow'}],
'tests':[{'source':'internet','destination':'management','protocol':'tcp','port':22,'expected':'deny'},
 {'source':'internet','destination':'dmz','protocol':'tcp','port':443,'expected':'allow'},
 {'source':'users','destination':'management','protocol':'tcp','port':3389,'expected':'deny'}],
'matrix_protocol':'tcp','matrix_port':443}

def normalize(policy):
    if not isinstance(policy,dict):raise ValueError('Expected an object')
    name=text(policy.get('name'),'Policy name',100);zones=policy.get('zones')
    if not isinstance(zones,list) or not 2<=len(zones)<=20:raise ValueError('Provide 2 to 20 zones')
    zones=[text(z,'Zone name',32) for z in zones]
    if len(set(zones))!=len(zones) or 'any' in zones:raise ValueError('Zone names must be unique; any is reserved')
    rules=policy.get('rules',[]);tests=policy.get('tests',[])
    if not isinstance(rules,list) or len(rules)>250:raise ValueError('At most 250 rules are supported')
    if not isinstance(tests,list) or len(tests)>250:raise ValueError('At most 250 policy tests are supported')
    def flow(item,rule=False):
        if not isinstance(item,dict):raise ValueError('Rules and tests must be objects')
        source=item.get('source');destination=item.get('destination');protocol=item.get('protocol','tcp')
        allowed=zones+(['any'] if rule else [])
        if source not in allowed or destination not in allowed:raise ValueError('Unknown source or destination zone')
        if protocol not in (['tcp','udp','any'] if rule else ['tcp','udp']):raise ValueError('Protocol must be tcp or udp; rules may use any')
        port=item.get('port','any' if rule else 443)
        port='any' if rule and port=='any' else integer(port,'Port',1,65535)
        return {'source':source,'destination':destination,'protocol':protocol,'port':port}
    result=[];ids=set()
    for r in rules:
        item=flow(r,True);item['id']=text(r.get('id'),'Rule ID',40)
        if item['id'] in ids:raise ValueError('Rule IDs must be unique')
        ids.add(item['id']);item['action']=r.get('action')
        if item['action'] not in ['allow','deny']:raise ValueError('Rule action must be allow or deny')
        result.append(item)
    checks=[]
    for t in tests:
        item=flow(t);item['expected']=t.get('expected')
        if item['expected'] not in ['allow','deny']:raise ValueError('Test expected action must be allow or deny')
        checks.append(item)
    protocol=policy.get('matrix_protocol','tcp')
    if protocol not in ['tcp','udp']:raise ValueError('Matrix protocol must be tcp or udp')
    return {'name':name,'zones':zones,'rules':result,'tests':checks,'matrix_protocol':protocol,'matrix_port':integer(policy.get('matrix_port',443),'Matrix port',1,65535)}

def covers(a,b):return all(a[k]=='any' or a[k]==b[k] for k in ['source','destination','protocol','port'])
def decide(rules,flow):
    for rule in rules:
        if covers(rule,flow):return {'action':rule['action'],'rule':rule['id']}
    return {'action':'deny','rule':'implicit-default-deny'}

def analyze(raw):
    p=normalize(raw);warnings=[];rules=p['rules']
    for i,r in enumerate(rules):
        shadow=next((prior for prior in rules[:i] if covers(prior,r)),None)
        if shadow:warnings.append({'type':'shadowed','rule':r['id'],'message':f'Unreachable: earlier rule {shadow["id"]} covers this rule.'})
        if r['action']=='allow' and r['source']=='any' and r['destination']=='any':warnings.append({'type':'broad-allow','rule':r['id'],'message':'Any-to-any allow expands trust across every modeled zone.'})
        if r['action']=='allow' and r['source'] in ['internet','any'] and r['destination'] in ['management','any'] and r['port'] in [22,3389,'any']:
            warnings.append({'type':'management-exposure','rule':r['id'],'message':'This allow rule may expose management access from the internet zone; inspect effective decisions.'})
    tests=[]
    for t in p['tests']:
        decision=decide(rules,t);tests.append({**t,**decision,'passed':decision['action']==t['expected']})
    matrix=[]
    for source in p['zones']:
        for dest in p['zones']:
            if source==dest:continue
            flow={'source':source,'destination':dest,'protocol':p['matrix_protocol'],'port':p['matrix_port']}
            matrix.append({**flow,**decide(rules,flow)})
    return {'id':str(uuid.uuid4()),'created':now(),'name':p['name'],'source':p,'warnings':warnings,'tests':tests,'matrix':matrix,
      'passed':sum(t['passed'] for t in tests),'failed':sum(not t['passed'] for t in tests),
      'allowed_flows':sum(m['action']=='allow' for m in matrix),'default_action':'deny',
      'boundary':'Logical first-match policy analysis only. No firewall deployment, packet simulation or network verification.'}

class Workspace:
    def __init__(self,directory):self.store=Store(directory)
    def state(self):return {'kind':'defense','title':'Security Policy Studio','subtitle':'Explain inter-zone access, catch shadowed rules and run explicit allow/deny assertions.','category':'SECURITY ARCHITECTURE','example':EXAMPLE,'analyses':self.store.all('analysis')}
    def action(self,body):
        action=body.get('action')
        if action=='analyze':return self.store.save('analysis',analyze(body.get('policy',{})))
        if action=='delete':self.store.delete('analysis',body.get('id'));return {'ok':True}
        raise ValueError('Unknown action')

if __name__=='__main__':serve(Workspace,8103)
