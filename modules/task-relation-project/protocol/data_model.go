/* For license and copyright information please see the LEGAL file in the code repository */

package trpp

import (
	"libgo/protocol"

	pp "org/modules/project/protocol"
	tp "org/modules/task/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TaskID() tp.TaskUUID            //
	ProjectID() pp.ProjectUUID      //
	Priority() uint64               //
	Permyriad() protocol.PerMyriad  // 0 means unset e.g. equal to other tasks in the project
	Type() Type                     //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint32

const (
	Type_Unset Type = 0

	Type_Blocking Type = (1 << iota) // stuck
	Type_Move                        // move from other project

	Type_Parent
	Type_
)
