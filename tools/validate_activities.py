"""Validate content-driven practice; never evaluate code supplied by a catalog."""
from decimal import Decimal

def integer(value, low, high):
    assert type(value) is int and low <= value <= high, 'Inteiro de atividade inválido'

def text(value, limit=2000):
    assert isinstance(value,str) and value.strip() and len(value)<=limit, 'Texto de atividade inválido'

def fields(activity):
    data=activity['fields'];assert 1<=len(data)<=8
    assert len({f['id'] for f in data})==len(data)
    for f in data:
        for key in ['id','label','explanation']:text(f[key])
        text(f['answer'],64)
        if f['kind']=='number':
            assert Decimal(f['answer']).is_finite() and not f.get('choices')
        else:
            assert f['kind']=='choice'
            choices=f['choices'];assert 2<=len(choices)<=6 and len(set(choices))==len(choices)
            for choice in choices:text(choice,1000)
            assert str(int(f['answer']))==f['answer'] and 0<=int(f['answer'])<len(choices)

def cpu_final(a):
    program=a['program'];assert 2<=len(program)<=16
    registers=a['registers'];assert len(registers)==4
    for v in registers:integer(v,0,255)
    pairs=a['memory'];assert len(pairs)<=8 and len({v['address'] for v in pairs})==len(pairs)
    for v in pairs:integer(v['address'],len(program)*4,255);integer(v['value'],0,255)
    memory={v['address']:v['value'] for v in pairs}
    for i in program:
        assert i['op'] in ['LOAD','STORE','ADD','JMP','JZ','HALT']
        for k in ['dst','a','b']:integer(i.get(k,0),0,3)
        integer(i.get('address',0),0,255)
        if i['op'] in ['LOAD','STORE']:assert i['address']>=len(program)*4
        if i['op'] in ['JMP','JZ']:assert i['address']%4==0 and i['address']//4<len(program)
    r=list(registers);pc=0;out=None
    for count in range(65):
        assert pc%4==0 and 0<=pc//4<len(program),'PC fora do programa'
        i=program[pc//4];op=i['op']
        if op=='HALT':return dict(pc=pc,registers=r,memory=memory,output=out,instructions=count+1)
        assert count<64,'O programa precisa terminar em até 64 instruções'
        next_pc=pc+4
        if op=='LOAD':r[i.get('dst',0)]=memory.get(i['address'],0)
        elif op=='STORE':
            value=r[i.get('a',0)]
            if i['address']==241:out=value
            else:memory[i['address']]=value
        elif op=='ADD':r[i.get('dst',0)]=(r[i.get('a',0)]+r[i.get('b',0)])%256
        elif op=='JMP':next_pc=i['address']
        elif op=='JZ' and r[i.get('a',0)]==0:next_pc=i['address']
        pc=next_pc
    raise AssertionError('Programa não terminou')

def state_next(machine,state,inputs):
    integer(state,0,15 if machine=='REGISTER4' else 3 if machine=='COUNTER2' else 1)
    if machine=='COUNTER2':assert inputs==[];return (state+1)%4
    if machine=='REGISTER4':
        assert len(inputs)==2;integer(inputs[0],0,15);integer(inputs[1],0,1)
        return inputs[0] if inputs[1] else state
    assert all(type(i) is int and i in [0,1] for i in inputs)
    if machine=='SR':
        assert len(inputs)==2 and inputs!=[1,1]
        return 1 if inputs[0] else 0 if inputs[1] else state
    if machine=='D':assert len(inputs)==2;return inputs[0] if inputs[1] else state
    assert machine in ['T','TOGGLE'] and len(inputs)==1
    return state^inputs[0]

def validate_activity(a):
    for key in ['id','title','prompt','hint','success']:text(a[key])
    integer(a['revision'],1,1_000_000)
    kind=a['type']
    if kind=='fields':fields(a)
    elif kind=='order':
        assert 3<=len(a['items'])<=8 and len(set(a['items']))==len(a['items'])
        for item in a['items']:text(item,1000)
        assert all(type(v) is int for v in a['correct'])
        assert sorted(a['correct'])==list(range(len(a['items'])))
    elif kind=='bits':
        assert a['width'] in [4,8];integer(a['target'],0,2**a['width']-1)
        assert type(a.get('signed',False)) is bool
    elif kind=='logic':
        sizes={'NOT':1,'AND':2,'OR':2,'XOR':2,'NAND':2,'NOR':2,'NOT_AND':2,'AND_OR':3,'HALF_ADD':2,'FULL_ADD':3,'MUX':3}
        size=sizes[a['gate']];cases=a['cases']
        assert 2<=len(cases)<=8 and len(set(cases))==len(cases)
        assert all(isinstance(c,str) and len(c)==size and set(c)<=set('01') for c in cases)
    elif kind=='state':
        assert 2<=len(a['events'])<=8
        current=a['start']
        for event in a['events']:
            text(event['label']);current=state_next(a['machine'],current,event['inputs'])
    elif kind=='cpu':fields(a);cpu_final(a)
    elif kind=='color':
        assert len(a['target'])==3
        for channel in a['target']:integer(channel,0,255)
    else:raise AssertionError('Tipo de atividade não suportado')

def validate_catalog_activities(catalog):
    ids=[]
    for unit in catalog['units']:
        for lesson in unit['lessons']:
            activity=lesson.get('activity')
            assert not catalog.get('interactivePractice') or activity, 'Toda lição precisa de atividade interativa'
            if activity:validate_activity(activity);ids.append(activity['id'])
    assert len(ids)==len(set(ids)), 'Identificadores de atividade duplicados'
    return len(ids)
