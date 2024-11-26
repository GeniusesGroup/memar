/* For license and copyright information please see the LEGAL file in the code repository */

package pap

import (
	"memar/protocol"

	pp "org/modules/project/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID pp.ProjectUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID pp.ProjectUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
