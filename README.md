# Splunk Custom Webhook Technical Add-on

A powerful Splunk Technical Add-on that extends Splunk's native webhook functionality with support for custom headers and flexible payload customization.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

Splunk's native webhook alert action provides basic HTTP POST functionality but lacks critical capabilities needed for modern API integrations. This Technical Add-on addresses those gaps by offering:

- **Custom HTTP Headers** - Add authorization headers, content-type specifications, and other required headers
- **Flexible Payload Configuration** - Define the exact JSON or XML structure your API expects
- **Enhanced Logging** - Comprehensive logging for debugging and monitoring webhook execution
- **Enterprise-Ready** - Production-tested alert action for mission-critical deployments

### Use Cases

This TA is ideal for integrating Splunk with:

- Incident Management Platforms (PagerDuty, Opsgenie, VictorOps)
- ITSM Systems (ServiceNow, Jira)
- Ticketing Systems
- Custom APIs and webhooks
- Centralized event management systems
- Automated workflow platforms

## Features

✅ **Custom Headers Support** - Add any HTTP headers required by your API endpoint  
✅ **Flexible Payload Definition** - Full control over request body structure  
✅ **Template Variables** - Use Splunk search result fields in headers and payload  
✅ **Comprehensive Logging** - Detailed logs for troubleshooting failed requests  
✅ **Secure HTTPS** - Full support for secure SSL/TLS connections  
✅ **Easy Configuration** - User-friendly UI for alert action setup  
✅ **Community-Driven** - Open source with welcoming contribution guidelines  

## Requirements

- **Splunk Enterprise** 8.0 or higher (recommended 8.2+)
- **Python** 3.x (included with Splunk Enterprise)
- **Network Access** - Outbound HTTPS connectivity to target webhook endpoints
- **Admin Access** - Required to install and configure the TA

## Installation

### Step 1: Download the Add-on

Clone or download this repository to your local machine:

```bash
git clone https://github.com/vgunti1982/Splunk_TA_CustomWebHook.git
```

### Step 2: Deploy to Splunk

**Option A: Manual Installation**

1. Navigate to your Splunk installation directory
2. Copy the `Splunk_TA_CustomWebHook` folder to `$SPLUNK_HOME/etc/apps/`
3. Restart Splunk Enterprise

**Option B: Using Splunk Web**

1. Go to **Settings** → **Apps** → **Manage Apps**
2. Click **Install app from file**
3. Select the downloaded `.tar.gz` file
4. Click **Upload**

### Step 3: Verify Installation

1. Log in to Splunk Web
2. Navigate to **Settings** → **Alerts** → **Alert Actions**
3. Confirm "Custom Webhook" appears in the list of available alert actions

## Configuration

### Creating an Alert with Custom Webhook

1. Create a new search or open an existing saved search
2. Click **Save As** → **Alert**
3. Configure the alert trigger conditions
4. Under **Trigger Actions**, select **Custom Webhook**

### Alert Action Fields

**Webhook URL** *(Required)*
- The target endpoint that will receive the webhook payload
- Example: `https://api.example.com/incidents/create`

**Custom Headers** *(Optional)*
- Add key-value pairs for HTTP headers
- Common examples:
  - `Authorization: Bearer YOUR_API_TOKEN`
  - `X-API-Key: YOUR_KEY`
  - `Content-Type: application/json`

**Request Payload** *(Optional)*
- Define the exact JSON structure to send
- Use `$field_name$` syntax to reference search result fields
- Example:
  ```json
  {
    "title": "$alert_name$",
    "severity": "high",
    "description": "$search_description$",
    "source": "Splunk",
    "timestamp": "$_time$"
  }
  ```

### Template Variables

Available variables you can use in headers and payload:

| Variable | Description |
|----------|-------------|
| `$alert_name$` | Name of the alert |
| `$search_description$` | Description of the saved search |
| `$_time$` | Event timestamp |
| `$host$` | Source host |
| `$source$` | Data source |
| `$sourcetype$` | Source type |
| Custom fields | Any field from your search results |

## Usage

### Example 1: PagerDuty Integration

```
Webhook URL: https://api.pagerduty.com/incidents

Custom Headers:
Authorization: Bearer YOUR_PAGERDUTY_TOKEN
Content-Type: application/json

Payload:
{
  "incident": {
    "type": "incident",
    "title": "$alert_name$",
    "service": {
      "id": "YOUR_SERVICE_ID",
      "type": "service_reference"
    },
    "urgency": "high"
  }
}
```

### Example 2: Custom API Integration

```
Webhook URL: https://internal-api.company.com/alerts/create

Custom Headers:
X-API-Key: YOUR_INTERNAL_API_KEY
Authorization: Bearer $internal_token$

Payload:
{
  "alert_name": "$alert_name$",
  "severity": "critical",
  "affected_host": "$host$",
  "event_time": "$_time$",
  "details": "$search_description$"
}
```

## Troubleshooting

### Viewing Webhook Logs

Webhook execution logs are stored in the Splunk internal index. Query them with:

```spl
index=_internal source="*customwebhook_alert.log"
```

Or directly on the filesystem:

```
Windows: C:\Program Files\Splunk\var\log\splunk\customwebhook_alert.log
Linux: $SPLUNK_HOME/var/log/splunk/customwebhook_alert.log
```

### Common Issues

**Issue: Webhook not triggering**
- Verify the alert trigger conditions are met
- Check Splunk logs for error messages
- Confirm the webhook URL is valid and accessible

**Issue: Authentication failures**
- Validate API credentials and tokens
- Ensure authorization headers are correctly formatted
- Check header names and values for typos

**Issue: Payload format errors**
- Verify JSON syntax is correct
- Test with a JSON validator
- Confirm all referenced fields exist in search results

**Issue: SSL/TLS errors**
- Verify certificate validity on the webhook endpoint
- Check Splunk's SSL configuration
- Ensure firewall allows outbound HTTPS traffic

## Architecture

The TA consists of:

- **Python Script** (`bin/custom_webhook.py`) - Core webhook delivery logic
- **Alert Action Definition** (`default/alert_actions.conf`) - Alert action configuration
- **UI Components** (`appserver/static/`) - Web interface for configuration
- **Metadata** (`metadata/`) - Permissions and access controls

## Security Considerations

- **Sensitive Data** - API keys and tokens in headers are encrypted when saved
- **HTTPS Only** - Always use secure endpoints for sensitive operations
- **Logging** - Be cautious with logs containing sensitive information
- **Validation** - Validate and sanitize all webhook content

## Contributing

We welcome community contributions! To contribute:

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

### Areas for Contribution

- Additional authentication methods (OAuth, JWT)
- Support for custom SSL certificates
- Proxy support
- Retry logic and error handling
- Additional template variables
- Documentation improvements

## References

- [Splunk Custom Alert Actions Documentation](https://dev.splunk.com/enterprise/docs/devtools/customalertactions/)
- [Splunk Alert Actions](https://docs.splunk.com/Documentation/Splunk/latest/Alert/AlertActionsReference)
- [HTTP/REST API Fundamentals](https://restfulapi.net/)

## Support

For issues, questions, or suggestions:

1. Check the troubleshooting section above
2. Review existing GitHub issues
3. Create a new GitHub issue with detailed information
4. Contact the maintainers

## Author

Developed by [vgunti1982](https://github.com/vgunti1982)

## License

This project is provided as-is for community use. Please refer to the LICENSE file for details.

---

**Version:** 1.0  
**Last Updated:** December 2025  
**Status:** Active Development
