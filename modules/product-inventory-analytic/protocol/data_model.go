/* For license and copyright information please see the LEGAL file in the code repository */

package piap

// `index-hash:"RecordID[pair,OwnerID,daily],OwnerID[not-exist]"`
// `index-hash:"QuiddityID[daily,not-exist]"` // Who belong to! Just org can be first owner!
import (
	"libgo/time/utc"

	eblp "org/modules/estate-building-location/protocol"
	pp "org/modules/product/protocol"
)

type DataModel interface {
	Day() utc.DayElapsed

	ProductID() pp.ProductUUID
	BuildingLocationID() eblp.BuildingLocationUUID //
	Amount()
}
