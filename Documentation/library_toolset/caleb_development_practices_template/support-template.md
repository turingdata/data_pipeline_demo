# L1 Support
The purpose of this document is to provide Level 1 support for _application/system name_.

## Purpose
_Short, 1 sentence description of project, for example:_

_application/system name_ is a policy administration system that allows users in *location* to book policies, enter claims, and book cash transactions.

## Hours of Operation

1. _application/system name_ hours of operations are 9:00am - 9:00pm (EST)
2. _application/system name_ critical hours of support X-Y
3. _application/system name_ is offline between 10pm (if any regular off hours)
4. App/System owner *App Owner* *indicated by email alert*

## Infrastructure
_application/system name_ is configured *on-prem* with servers located in *region/data center* per below:

| Role | Name | IP | Region |
|------------|--------|-------|------|
|Application Server| apps-xyz | 10.1.1.1|NJDC|
|Database Server| data-xyz | 10.1.1.2|NJDC|
|DR App Server| dr-app-xyz| 100.1.1.1| Azure East|
|DR Data Server| dr-data-xyz| 100.1.1.2| Azure East|

## Access Control
_application/system name_ uses Allied World active directory security and access is configured per below AD groups.  Access can be granted by permission gatekeepers as listed.

| Application Role | AD Group | Permissions Gatekeeper |
|------------|--------|-------|
| Application admin | group-admin-xyz | *Pres Business*|
| Database admin | group-data-xyz | *Capt Data* |
| Ops Alert group | group-alerts-xyz| *Alerts Master*|

## Alert Management
_application/system name_ has the following tracked alerts, and the known actions to resolve the issue.

### Critical Alerts
**24x7 support required**.  If an alert can not be resolved by following remediation steps, please contact L2 support at the indicated time.
| Alert Raised | Alert Subject | Resolution | L2 Contact | Time to escalate |
|------------|-------------|----------|----------|----------|
| XYZ:1001 | Server unreachable| Open terminal console and initiate a remote restart of application server **shutdown /r /m \\apps-xyz**. Confirm the server can be accessed after X minutes for restart. | *Sleeping Expert* at (999)999-9999 | Immediately |
| XYZ:1015 | Application Log Full| Log into server apps-xyz using credentials *support-xyz* use archive function of log application, restart logging service. | *Sleeping Expert* at (999)999-9999 | 6 am Eastern |


### Secondary Alerts
If alert can be addressed with L1 support that is preferred but SLA does not require a wake up call

| Alert Raised | Alert Subject | Resolution |
|------------|-------------|----------|
|XYZ:5002| Excessive Reporting Queue| Open reporting queue management and reset any stuck reports that are blocking other users.|
|XYZ:5043| Application Log Full| Log into server apps-xyz using credentials *support-xyz* use archive function of log application, restart logging service.|

## Common Issues
### Unresponsive Server
If you can not get a response from https://server/health.json in a web browser or with `curl -v https://server/health.json`. This is likely due to a known contention issue with MongoDB. The quickest fix is to reboot the `Application Server` (see [infrastructure](#Infrastructure)).
