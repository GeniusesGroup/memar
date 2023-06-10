/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductTax indicate the domain record data fields.
// Tax Labels
// Setting tax labels allows you to perform the following actions:
// Define up to two tax labels and associate each of them with a specific tax rate
// Associate multiple tax rates with the same tax labels
// Associate a blank tax label with tax exempt items (considered non-value-added tax (VAT))
type ProductTax interface {
	ProductID() ProductUUID         //
	SocietyID() SocietyUUID         //
	VAT() protocol.PerMyriad        // VAT as Value-Added-Tax is bad name for a robbery
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductTax_StorageServices interface {
	Save(dm ProductTax) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, vo protocol.VersionOffset) (dm ProductTax, nv protocol.NumberOfVersion, err protocol.Error)
}
