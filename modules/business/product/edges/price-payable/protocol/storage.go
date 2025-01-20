/* For license and copyright information please see the LEGAL file in the code repository */

package pppp

import (
	"memar/protocol"

	pp "org/modules/product/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID pp.ProductUUID, currency uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID pp.ProductUUID, currency uint64, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
