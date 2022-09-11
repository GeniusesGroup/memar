/* For license and copyright information please see the LEGAL file in the code repository */

package org

// `index-hash:"RecordID[pair,OwnerID,daily],OwnerID[not-exist]"`
// `index-hash:"QuiddityID[daily,not-exist]"` // Who belong to! Just org can be first owner!

type ProductInventoryAnalytic interface {
	Day()

	ProductID()
	BuildingLocationID() [16]byte // building-location domain
	Amount()
}
