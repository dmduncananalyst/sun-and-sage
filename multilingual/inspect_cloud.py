"""Read-only connection diagnostics. Never enables services or changes quotas."""
import json
import os
from .site import CONFIG, ROOT

def main():
    import google.auth
    from google.auth.transport.requests import AuthorizedSession
    project=os.environ.get('GOOGLE_CLOUD_PROJECT') or CONFIG['google_project_id']
    credentials,_=google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'],quota_project_id=project)
    session=AuthorizedSession(credentials)
    admin=AuthorizedSession(credentials.with_quota_project(None))
    report={'project_id':project,'authenticated':True,'paid_translation_requests_in_diagnostic':0,'quotas_changed':False}
    def get(url):
        client=admin if url.startswith(('https://cloudbilling.googleapis.com/','https://cloudresourcemanager.googleapis.com/')) else session
        response=client.get(url,timeout=30)
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
    quota_url=f'https://serviceusage.googleapis.com/v1beta1/projects/{number}/services/translate.googleapis.com/consumerQuotaMetrics?view=FULL'
    metrics=[];url=quota_url
    while url:
        quotas=get(url)
        report['quota_read_status']=quotas.get('http_status',200)
        metrics.extend(quotas.get('metrics',[]))
        url=quota_url+'&pageToken='+quotas['nextPageToken'] if quotas.get('nextPageToken') else None
    report['daily_translation_quotas']=[{'metric':metric['metric'],'unit':limit.get('unit'),'limits':[bucket.get('effectiveLimit') for bucket in limit.get('quotaBuckets',[])]} for metric in metrics for limit in metric.get('consumerQuotaLimits',[]) if '/d/' in limit.get('unit','')]
    supported=get(f'https://translation.googleapis.com/v3/projects/{project}/locations/global/supportedLanguages')
    available={item['languageCode'] for item in supported.get('languages',[]) if item.get('supportTarget')}
    report['requested_language_support']={lang:lang in available for lang in CONFIG['languages']}
    report['supported_languages_http_status']=supported.get('http_status',200)
    (ROOT/'multilingual/cloud-status.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
