/* For license and copyright information please see the LEGAL file in the code repository */

package pp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DataModel is the structure of production line.
// https://www.zenscale.in/planning
type DataModel interface {
	ID() ProductionUUID             //
	StartDate() protocol.Time       //
	EndDate() protocol.Time         //
	Number() uint64                 //
	Status() uint8                  //
	SaveTime() protocol.Time        // Save time
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
