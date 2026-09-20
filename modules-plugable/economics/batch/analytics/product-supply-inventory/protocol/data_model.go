/* For license and copyright information please see the LEGAL file in the code repository */

package piap

// `index-hash:"RecordID[pair,OwnerID,daily],OwnerID[not-exist]"`
// `index-hash:"QuiddityID[daily,not-exist]"` // Who belong to! Just org can be first owner!
import (
	"memar/time/utc"

	product_p "org/modules/economics/product/protocol"
	estate_p "org/modules/rights/estate/protocol"
)

type DataModel interface {
	utc.Field_DayElapsed

	product_p.Field_ProductID
	estate_p.Field_EstateID
	Amount()
}
