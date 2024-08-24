/* For license and copyright information please see the LEGAL file in the code repository */

package prtp

import (
	"memar/protocol"

	ltp "org/modules/label-table/protocol"
	pp "org/modules/project/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID pp.ProjectUUID, tableID ltp.TableUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID pp.ProjectUUID, tableID ltp.TableUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
