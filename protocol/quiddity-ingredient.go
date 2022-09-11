/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// ProductIngredient indicate the domain record data fields.
type ProductIngredient interface {
	ProductID() [16]byte        // product domain
	IngredientID() [16]byte     // product domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type ProductIngredient_StorageServices interface {
	Save(pi ProductIngredient) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (pi ProductIngredient, nv protocol.NumberOfVersion, err protocol.Error)

	FindByIngredient(ingredientID [16]byte, offset, limit uint64) (productIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
