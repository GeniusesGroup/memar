/* For license and copyright information please see the LEGAL file in the code repository */

package arp

// Audit logging is the process of documenting activity within the software systems used across your organization.
// Audit logs record the occurrence of an event, the time at which it occurred, the responsible user or service,
// and the impacted entity. All of the devices in your network, your cloud services,
// and your applications emit logs that may be used for auditing purposes.
type AuditLogging interface {
	RequestID() RequestUUID
}
