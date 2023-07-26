/* For license and copyright information please see the LEGAL file in the code repository */

/*
- Some product as material need or pend on other production, .e.g. car needs engine, ...
*/
package org

import (
	"memar/protocol"

	pp "org/modules/production/protocol"
)

type DataModel interface {
	ProductionID() pp.ProductionUUID
	RelationID() pp.ProductionUUID
	Type() Type
	// TODO::: other fields? Status()?

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
