/* For license and copyright information please see the LEGAL file in the code repository */

package esp

import (
	"libgo/protocol"

	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	AreaID() [16]byte               // quiddity domain
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

const (
	Status_NeighborsConflict = Status(qsp.Quiddity_Status_FreeFlag << iota)
)
