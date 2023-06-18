/* For license and copyright information please see the LEGAL file in the code repository */

package pprp

import (
	"libgo/protocol"

	pp "org/modules/product/protocol"
	qsp "org/modules/quiddity-status/protocol"
	rp "org/modules/role/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel or product operator is to supply a particular service.
// TODO::: role or group??
type DataModel interface {
	ProductID() pp.ProductUUID //
	RoleID() rp.RoleUUID       //
	Status() Status
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

// related UserIDs by RoleID use to get Coordinate(domain)
