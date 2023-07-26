/* For license and copyright information please see the LEGAL file in the code repository */

package prpp

import (
	"memar/protocol"

	pp "org/modules/project/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID pp.ProjectUUID, otherID pp.ProjectUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID pp.ProjectUUID, otherID pp.ProjectUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_OtherIDs_BY_ProjectID(projectID pp.ProjectUUID, offset, limit uint64) (OtherIDs []pp.ProjectUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
