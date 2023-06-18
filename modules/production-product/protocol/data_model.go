/* For license and copyright information please see the LEGAL file in the code repository */

package ppp

import (
	"libgo/protocol"

	prp "org/modules/product/protocol"
	pp "org/modules/production/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel is the structure of production line.
type DataModel interface {
	ProductionID() pp.ProductionUUID //
	ProductID() prp.ProductUUID
	Number() uint64
	Status() uint8
	SaveTime() protocol.Time        // Save time
	RequestID() urp.UserRequestUUID //
}

// 0//created 1//ManagerApprove 2//WarehouseApprove 3//ActiveWithApprove 4//ActiveWithoutApprove 5//ActiveWithOrderer 6//Inactive 7//Normal 8//Reject 9//Void
