/* For license and copyright information please see the LEGAL file in the code repository */

package prgp

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
	pp "org/modules/project/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProjectID() pp.ProjectUUID      //
	GroupID() gp.GroupUUID          //
	ProjectGroupRelation() Type     //
	SaveTime() protocol.Time        // Save time
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_Authorization
)
