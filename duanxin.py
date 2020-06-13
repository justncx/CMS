from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.sms.v20190711 import sms_client, models 
try: 
    cred = credential.Credential("AKID611pNRltsc4FKFQTs40hUCvVwA7noDJF", "ynUyEE37xa5RknqlW2PuBDzUh1BA1kIT") 
    httpProfile = HttpProfile()
    httpProfile.endpoint = "sms.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = sms_client.SmsClient(cred, "", clientProfile) 

    req = models.SendSmsRequest()
    params = '{}'
    req.from_json_string(params)

    resp = client.SendSms(req) 
    print(resp.to_json_string()) 

except TencentCloudSDKException as err: 
    print(err)
