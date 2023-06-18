/* For license and copyright information please see the LEGAL file in the code repository */

package dop

import (
	"libgo/protocol"

	dp "org/modules/department/protocol"
	blp "org/modules/estate-building-location/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	DepartmentID() dp.DepartmentUUID              //
	BuildingLocationID() blp.BuildingLocationUUID //
	// TODO::: Label or type: IT-Office, ...
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

