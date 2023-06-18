/* For license and copyright information please see the LEGAL file in the code repository */

package dlp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	dp "org/modules/discount/protocol"
	bp "org/modules/estate-building-location/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID //
	BuildingLocationID() bp.BuildingLocationUUID
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

