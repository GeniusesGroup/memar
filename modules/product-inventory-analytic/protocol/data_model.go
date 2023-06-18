/* For license and copyright information please see the LEGAL file in the code repository */

package piap

// `index-hash:"RecordID[pair,OwnerID,daily],OwnerID[not-exist]"`
// `index-hash:"QuiddityID[daily,not-exist]"` // Who belong to! Just org can be first owner!
import pp "org/modules/product/protocol"

type DataModel interface {
	Day()

	ProductID() pp.ProductUUID
	BuildingLocationID() BuildingLocationUUID //
	Amount()
}
