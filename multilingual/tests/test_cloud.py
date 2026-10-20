import unittest
from unittest.mock import patch
from multilingual.cloud import Cloud

class Snapshot:
    def __init__(self,value):self.value=value;self.exists=value is not None
    def to_dict(self):return self.value

class Reference:
    def __init__(self,db,path):self.db,self.path=db,path
    def get(self,transaction=None):return Snapshot(self.db.rows.get(self.path))
    def update(self,value):self.db.rows[self.path].update(value)

class Collection:
    def __init__(self,db,name):self.db,self.name=db,name
    def document(self,name):return Reference(self.db,self.name+'/'+name)

class Transaction:
    def set(self,ref,value):ref.db.rows[ref.path]=value

class Database:
    def __init__(self):self.rows={}
    def collection(self,name):return Collection(self,name)
    def transaction(self):return Transaction()

class Firestore:
    SERVER_TIMESTAMP='server timestamp'
    @staticmethod
    def transactional(function):return function

class CloudBudgetTests(unittest.TestCase):
    def setUp(self):
        import datetime
        self.month=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m')
        self.cloud=Cloud.__new__(Cloud);self.cloud.db=Database();self.cloud.firestore=Firestore
        self.cloud.db.rows['dommydom_budget_baselines/'+self.month]={'verified':True,'translation_microusd':0}

    def test_successful_request_is_cached(self):
        calls=[]
        for _ in range(2):self.assertEqual(self.cloud.execute('request',20,lambda:calls.append(1) or 'hola'),'hola')
        self.assertEqual(calls,[1])
        self.assertEqual(self.cloud.db.rows['dommydom_spend/'+self.month+'-translation']['reserved_microusd'],20)

    def test_uncertain_request_never_repeats(self):
        calls=[]
        def fail():calls.append(1);raise TimeoutError()
        with self.assertRaises(TimeoutError):self.cloud.execute('request',20,fail)
        with self.assertRaisesRegex(RuntimeError,'already reserved'):self.cloud.execute('request',20,fail)
        self.assertEqual(calls,[1])

    def test_baseline_and_limit_checked_before_paid_operation(self):
        self.cloud.db.rows['dommydom_budget_baselines/'+self.month]['translation_microusd']=20_000_000
        calls=[]
        with self.assertRaisesRegex(RuntimeError,'Monthly translation limit'):self.cloud.execute('request',1,lambda:calls.append(1))
        self.assertFalse(calls)
        del self.cloud.db.rows['dommydom_budget_baselines/'+self.month]
        with self.assertRaisesRegex(RuntimeError,'baseline'):self.cloud.execute('request',1,lambda:calls.append(1))
        self.assertFalse(calls)

    def test_voice_is_disabled_without_separate_spending_authorization(self):
        with patch.dict('os.environ',{},clear=True):
            with self.assertRaisesRegex(RuntimeError,'Voice spending'):self.cloud.execute('voice',1,lambda:'audio',True,'voice')

    def test_warning_is_persisted(self):
        self.cloud.db.rows['dommydom_budget_baselines/'+self.month]['translation_microusd']=14_999_999
        self.cloud.execute('request',1,lambda:'hola')
        self.assertIn('dommydom_budget_warnings/'+self.month,self.cloud.db.rows)
