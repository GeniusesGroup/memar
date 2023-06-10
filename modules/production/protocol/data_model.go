/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type ProductionUUID = protocol.UUID

// Production is the structure of production line.
// https://www.zenscale.in/planning
type Production interface {
	ID() ProductionUUID             //
	StartDate() protocol.Time       //
	EndDate() protocol.Time         //
	Number() uint64                 //
	Status() uint8                  //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

//Created
//ManagerApprove
//WarehouseApprove
//ActiveWithApprove
//ActiveWithoutApprove
//ActiveWithOrderer
//Inactive
//Normal
//Reject
//Void
