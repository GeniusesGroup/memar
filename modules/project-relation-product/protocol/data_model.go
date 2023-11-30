/* For license and copyright information please see the LEGAL file in the code repository */

package prpp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	prp "org/modules/product/protocol"
	pp "org/modules/project/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProjectID() pp.ProjectUUID
	ProductID() prp.ProductUUID
	Status() Status
	// TODO::: type or label??

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
