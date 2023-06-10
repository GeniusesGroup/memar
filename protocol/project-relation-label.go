/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProjectLabel indicate the domain record data fields.
type ProjectLabel interface {
	ProjectID() ProjectUUID         //
	LabelID() LabelUUID             //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type ProjectLabel_StorageServices interface {
	Save(dm ProjectLabel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID ProjectUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID ProjectUUID, vo protocol.VersionOffset) (dm ProjectLabel, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}

// 	LIST_LabelIDs_BY_ProjectID(projectID ProjectUUID, offset, limit uint64) (labelIDs []LabelUUID, nv protocol.NumberOfVersion, err protocol.Error)
