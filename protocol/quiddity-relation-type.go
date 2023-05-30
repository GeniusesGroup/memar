/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type QuiddityRelationTypeUUID = QuiddityUUID

// QuiddityRelationType store some key/value for a Quiddity to describe it e.g. mobile-cpu, ...
// e.g. MetricUnit: Number, Gram, Liter, Second
type QuiddityRelationType interface {
	TypeID() QuiddityRelationTypeUUID    //
	Status() QuiddityRelationType_Status //
	Time() protocol.Time                 // save time
	RequestID() urp.UserRequestUUID      //
}

type QuiddityRelationType_Status Quiddity_Status

const (
	QuiddityRelationType_Status_Unset QuiddityRelationType_Status = iota
)
