/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProjectRelationProject indicate the domain record data fields.
type ProjectRelationProject interface {
	ProjectID() ProjectUUID            //
	OtherID() ProjectUUID              //
	Priority() uint64                  //
	Type() ProjectRelationProject_Type //
	Time() protocol.Time               // Save time
	RequestID() urp.UserRequestUUID    //
}

type ProjectRelationProject_Type uint8

// Blocking
