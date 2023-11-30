/* For license and copyright information please see the LEGAL file in the code repository */

package prtp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	ltp "org/modules/label-table/protocol"
	pp "org/modules/project/protocol"
)

// DataModel indicate the domain record data fields.
// Table or boards is visual aid to help users access tasks in GUI e.g.Table(TODO, DOING, DONE)
type DataModel interface {
	ProjectID() pp.ProjectUUID
	TableID() ltp.TableUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
