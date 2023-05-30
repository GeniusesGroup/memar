/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// Production is the structure of production line.
type ProductionProduct interface {
	ProductionID() ProductionUUID //
	ProductID() ProductUUID
	Number() uint64
	Status() uint8
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

// 0//created 1//ManagerApprove 2//WarehouseApprove 3//ActiveWithApprove 4//ActiveWithoutApprove 5//ActiveWithOrderer 6//Inactive 7//Normal 8//Reject 9//Void
