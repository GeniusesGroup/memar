/* For license and copyright information please see the LEGAL file in the code repository */

package eblsp

import (
	"libgo/protocol"

	eblp "org/modules/estate-building-location/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	BuildingLocationID() eblp.BuildingLocationUUID //
	Status() Status                                //
	SaveTime() protocol.Time                       //
	RequestID() urp.UserRequestUUID                //
}

type Status qsp.Quiddity_Status

const (
// Status_ = Status(Quiddity_Status_FreeFlag << iota)
)
