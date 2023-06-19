/* For license and copyright information please see the LEGAL file in the code repository */

/*
- Some product as material need or pend on other production, .e.g. car needs engine, ...
*/
package org

import (
	"libgo/protocol"

	pp "org/modules/production/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	ProductionID() pp.ProductionUUID //
	RelationID() pp.ProductionUUID   //
	// TODO::: other fields? Status()?
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
