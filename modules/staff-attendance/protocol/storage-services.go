/* For license and copyright information please see the LEGAL file in the code repository */

package sap

import (
	"memar/protocol"

	sp "org/modules/staff/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID sp.StaffUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID sp.StaffUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
