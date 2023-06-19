/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	pbp "org/modules/production-batch/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel is the structure of production line.
type DataModel interface {
	ProductionBatchID() pbp.ProductionBatchUUID //
	TimeType() TimeType                         //
	ActionTime() protocol.Time                  //
	SaveTime() protocol.Time                    //
	RequestID() urp.UserRequestUUID             //
}

type TimeType uint8

const (
	TimeType_Unset TimeType = iota

	TimeType_Start
	TimeType_End
	TimeType_ManualStart
	TimeType_ManualEnd
)
