/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProjectProductRelation indicate the domain record data fields.
type ProjectGroupRelation interface {
	ProjectID() ProjectUUID                          //
	GroupID() GroupUUID                              //
	ProjectGroupRelation() ProjectGroupRelation_Type //
	Time() protocol.Time                             // Save time
	RequestID() urp.UserRequestUUID                  //
}

type ProjectGroupRelation_StorageServices interface {
	Save(f ProjectGroupRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID, projectID ProjectUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, projectID ProjectUUID, vo protocol.VersionOffset) (f ProjectGroupRelation, nv protocol.NumberOfVersion, err protocol.Error)
}


type ProjectGroupRelation_Type uint8

const (
	ProjectGroupRelation_Type_Unset ProjectGroupRelation_Type = iota
	ProjectGroupRelation_Type_Authorization
)
