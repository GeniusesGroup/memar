/* For license and copyright information please see the LEGAL file in the code repository */

package pjop

import (
	"libgo/protocol"

	pp "org/modules/production/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	// A lot number is an identification number assigned to a particular quantity or lot of material from a single manufacturer.
	// https://en.wikipedia.org/wiki/Lot_number
	LOT() [16]byte                   // quiddity domain.
	ProductionID() pp.ProductionUUID //
	StartDate() protocol.Time        //
	EndDate() protocol.Time          //
	Number() uint64                  //
	Status() uint8                   //
	SaveTime() protocol.Time         // Save time
	RequestID() urp.UserRequestUUID  //
}

type Status uint8

const (
	Status_Unset Status = iota
	Status_Rework
	Status_Rejection
	Status_Approved
)
