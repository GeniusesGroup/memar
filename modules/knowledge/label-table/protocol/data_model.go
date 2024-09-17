/* For license and copyright information please see the LEGAL file in the code repository */

package ltp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	lp "org/modules/label/protocol"
)

// LabelTable indicate the domain record data fields.
// Table or boards is visual aid to help users access tasks in GUI e.g.Table(TODO, DOING, DONE)
// TODO::: base on label or status or both??
type LabelTable interface {
	TableID() TableUUID
	Labels() []lp.LabelUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
