/* For license and copyright information please see the LEGAL file in the code repository */

package dop

import (
	"memar/protocol"

	dp "org/modules/department/protocol"
	blp "org/modules/estate-building-location/protocol"
)

type DataModel interface {
	DepartmentID() dp.DepartmentUUID
	BuildingLocationID() blp.BuildingLocationUUID
	// TODO::: Label or type: IT-Office, ...

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
