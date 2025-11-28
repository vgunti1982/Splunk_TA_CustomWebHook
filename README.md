Many real-world Splunk deployments require sending alerts to third-party applications via Webhooks for centralized event management and to trigger subsequent workflows for alerting or incident handling. Splunk's native Webhook alert action offers this functionality but has significant drawbacks. It restricts users to providing only a URL, which often isn't sufficient for secure HTTPS endpoints that necessitate authorization headers. Additionally, the out-of-the-box action lacks the ability to customize the request payload, a critical requirement for seamless integration with most external APIs.

This application is designed to overcome these two challenges. It provides users with the capability to specify custom headers and define the exact request payload to be sent with their Webhook alerts.

I am sharing the source code of this application so that any Splunk users can make modifications as per their use cases or use it as is. We encourage community contributions and welcome any further modifications.

UI of the Alert Action

![image](https://github.com/user-attachments/assets/8c0f1349-6fea-4d28-a294-8c7aea7fc61d)

Log messages to help troubleshoot if any problem

![image](https://github.com/user-attachments/assets/eb113876-ecea-4982-92d6-d91054f1d1bf)

Query to check logs

index=_internal source="C:\\Program Files\\Splunk\\var\\log\\splunk\\customwebhook_alert.log" 

Splunk documentation : https://dev.splunk.com/enterprise/docs/devtools/customalertactions/

