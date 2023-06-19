/* For license and copyright information please see the LEGAL file in the code repository */

package pp

import (
	"libgo/protocol"

	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel is the structure of production line.
// https://www.zenscale.in/planning
type DataModel interface {
	ProductionID() ProductionUUID   //
	Type() Type                     //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Unset            Type = 0
	Type_CustomProduction Type = (1 << iota)
	Type_MassProduction
)

type Status qsp.Quiddity_Status

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
