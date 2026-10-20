"""Read-only connection diagnostics. Never enables services or changes quotas."""
import json
import os
from .site import CONFIG

def main():
    import google.auth
    from google.auth.transport.requests import AuthorizedSession
    project=os.environ.get('GOOGLE_CLOUD_PROJECT') or CONFIG['google_project_id']
    credentials,_=google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
    session=AuthorizedSession(credentials)
    report={'project_id':project,'authenticated':True,'paid_translation_requests':0,'quotas_changed':False}
    def get(url):
        response=session.get(url,timeout=30)
        if not response.ok:return {'http_status':response.status_code}
        return response.json()
    info=get(f'https://cloudresourcemanager.googleapis.com/v1/projects/{project}')
    report['project_status']=info.get('lifecycleState',info.get('http_status'))
    number=info.get('projectNumber',project)
    report['services']={}
    for service in ['translate.googleapis.com','speech.googleapis.com','texttospeech.googleapis.com','firestore.googleapis.com','run.googleapis.com','identitytoolkit.googleapis.com']:
        result=get(f'https://serviceusage.googleapis.com/v1/projects/{number}/services/{service}')
        report['services'][service]=result.get('state',result.get('http_status'))
    billing=get(f'https://cloudbilling.googleapis.com/v1/projects/{project}/billingInfo')
    report['billing_enabled']=billing.get('billingEnabled',billing.get('http_status'))
    quotas=get(f'https://serviceusage.googleapis.com/v1beta1/projects/{number}/services/translate.googleapis.com/consumerQuotaMetrics?view=FULL')
    report['quota_read_status']=quotas.get('http_status',200)
    report['translation_quota_metrics']=quotas.get('metrics',[])
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
